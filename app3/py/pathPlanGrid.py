
import math
import os
import sys
from enum import IntEnum
import cv2

import numpy as np
from scipy.spatial.transform import Rotation as Rot
import matplotlib.pyplot as plt

import datetime
from datetime import datetime

import urllib
import urllib.request as ur
import statistics

try:
    from .grid_map_lib import GridMap
except ImportError:
    raise

from .contourmapanalysis import ContorImageFill,LoadVoronoi,loadContour,CalculationMaxMin,UniformtoImage,project_array,Imageslice
from .contourmapanalysis import *
do_animation = True


class SweepSearcher:
    class SweepDirection(IntEnum):
        UP = 1
        DOWN = -1

    class MovingDirection(IntEnum):
        RIGHT = 1
        LEFT = -1

    def __init__(self,
                 moving_direction, sweep_direction, x_inds_goal_y, goal_y):
        self.moving_direction = moving_direction
        self.sweep_direction = sweep_direction
        self.turing_window = []
        self.update_turning_window()
        self.x_indexes_goal_y = x_inds_goal_y
        self.goal_y = goal_y

    def move_target_grid(self, c_x_index, c_y_index, grid_map):
        n_x_index = self.moving_direction + c_x_index
        n_y_index = c_y_index

        # found safe grid
        if not grid_map.check_occupied_from_xy_index(n_x_index, n_y_index,
                                                     occupied_val=0.25):
            return n_x_index, n_y_index
        else:  # occupied
            next_c_x_index, next_c_y_index = self.find_safe_turning_grid(
                c_x_index, c_y_index, grid_map)
            if (next_c_x_index is None) and (next_c_y_index is None):
                # moving backward
                next_c_x_index = -self.moving_direction + c_x_index
                next_c_y_index = c_y_index
                if grid_map.check_occupied_from_xy_index(next_c_x_index,
                                                         next_c_y_index,occupied_val=0.25):
                    # moved backward, but the grid is occupied by obstacle
                    return None, None
            else:
                # keep moving until end
                while not grid_map.check_occupied_from_xy_index(
                        next_c_x_index + self.moving_direction,
                        next_c_y_index, occupied_val=0.25):
                    next_c_x_index += self.moving_direction
                self.swap_moving_direction()
            return next_c_x_index, next_c_y_index

    def find_safe_turning_grid(self, c_x_index, c_y_index, grid_map):

        for (d_x_ind, d_y_ind) in self.turing_window:

            next_x_ind = d_x_ind + c_x_index
            next_y_ind = d_y_ind + c_y_index

            # found safe grid
            if not grid_map.check_occupied_from_xy_index(next_x_ind,
                                                         next_y_ind,
                                                         occupied_val=0.25):
                return next_x_ind, next_y_ind

        return None, None

    def is_search_done(self, grid_map):
        for ix in self.x_indexes_goal_y:
            if not grid_map.check_occupied_from_xy_index(ix, self.goal_y,
                                                         occupied_val=0.25):
                return False

        # all lower grid is occupied
        return True

    def update_turning_window(self):
        # turning window definition
        # robot can move grid based on it.
        self.turing_window = [
            (self.moving_direction, 0.0),
            (self.moving_direction, self.sweep_direction),
            (0, self.sweep_direction),
            (-self.moving_direction, self.sweep_direction),
        ]

    def swap_moving_direction(self):
        self.moving_direction *= -1
        self.update_turning_window()

    def search_start_grid(self, grid_map):
        x_inds = []
        y_ind = 0
        if self.sweep_direction == self.SweepDirection.DOWN:
            x_inds, y_ind = search_free_grid_index_at_edge_y(
                grid_map, from_upper=True)
        elif self.sweep_direction == self.SweepDirection.UP:
            x_inds, y_ind = search_free_grid_index_at_edge_y(
                grid_map, from_upper=False)

        if self.moving_direction == self.MovingDirection.RIGHT:
            return min(x_inds), y_ind
        elif self.moving_direction == self.MovingDirection.LEFT:
            return max(x_inds), y_ind

        raise ValueError("self.moving direction is invalid ")

def getImage(url_Str):
    req = ur.urlopen(url_Str)
    arr = np.asarray(bytearray(req.read()), dtype=np.uint8)
    img = cv2.imdecode(arr, -1)
    return img

def find_sweep_direction_and_start_position(ox, oy):
    # find sweep_direction
    max_dist = 0.0
    vec = [0.0, 0.0]
    sweep_start_pos = [0.0, 0.0]
    for i in range(len(ox) - 1):
        dx = ox[i + 1] - ox[i]
        dy = oy[i + 1] - oy[i]
        d = np.hypot(dx, dy)

        if d > max_dist:
            max_dist = d
            vec = [dx, dy]
            sweep_start_pos = [ox[i], oy[i]]

    return vec, sweep_start_pos


def convert_grid_coordinate(ox, oy, sweep_vec, sweep_start_position):
    tx = [ix - sweep_start_position[0] for ix in ox]
    ty = [iy - sweep_start_position[1] for iy in oy]
    th = math.atan2(sweep_vec[1], sweep_vec[0])
    rot = Rot.from_euler('z', th).as_matrix()[0:2, 0:2]
    converted_xy = np.stack([tx, ty]).T @ rot

    return converted_xy[:, 0], converted_xy[:, 1]


def convert_global_coordinate(x, y, sweep_vec, sweep_start_position):
    th = math.atan2(sweep_vec[1], sweep_vec[0])
    rot = Rot.from_euler('z', -th).as_matrix()[0:2, 0:2]
    converted_xy = np.stack([x, y]).T @ rot
    rx = [ix + sweep_start_position[0] for ix in converted_xy[:, 0]]
    ry = [iy + sweep_start_position[1] for iy in converted_xy[:, 1]]
    return rx, ry


def search_free_grid_index_at_edge_y(grid_map, from_upper=False):
    y_index = None
    x_indexes = []

    if from_upper:
        x_range = range(grid_map.height)[::-1]
        y_range = range(grid_map.width)[::-1]
    else:
        x_range = range(grid_map.height)
        y_range = range(grid_map.width)

    for iy in x_range:
        for ix in y_range:
            if not grid_map.check_occupied_from_xy_index(ix, iy,0.25):
                y_index = iy
                x_indexes.append(ix)
        if y_index:
            break

    return x_indexes, y_index


def setup_grid_map(ox, oy, resolution, sweep_direction, offset_grid=10):
    width = math.ceil((max(ox) - min(ox)) / resolution) + offset_grid
    height = math.ceil((max(oy) - min(oy)) / resolution) + offset_grid
    center_x = (np.max(ox) + np.min(ox)) / 2.0
    center_y = (np.max(oy) + np.min(oy)) / 2.0

    grid_map = GridMap(width, height, resolution, center_x, center_y)
    #grid_map.print_grid_map_info()
    grid_map.set_value_from_polygon(ox, oy, 1, inside=False)
    grid_map.expand_grid()

    x_inds_goal_y = []
    goal_y = 0
    if sweep_direction == SweepSearcher.SweepDirection.UP:
        x_inds_goal_y, goal_y = search_free_grid_index_at_edge_y(
            grid_map, from_upper=True)
    elif sweep_direction == SweepSearcher.SweepDirection.DOWN:
        x_inds_goal_y, goal_y = search_free_grid_index_at_edge_y(
            grid_map, from_upper=False)

    return grid_map, x_inds_goal_y, goal_y


def sweep_path_search(sweep_searcher, grid_map, grid_search_animation=False):
    # search start grid
    c_x_index, c_y_index = sweep_searcher.search_start_grid(grid_map)

    if not grid_map.set_value_from_xy_index(c_x_index, c_y_index, 0.25):
        print("Cannot find start grid")
        return [], []

    x, y = grid_map.calc_grid_central_xy_position_from_xy_index(c_x_index,
                                                                c_y_index)
    px, py = [x], [y]

    fig, ax = None, None
    if grid_search_animation:
        fig, ax = plt.subplots()
        # for stopping simulation with the esc key.
        fig.canvas.mpl_connect(
            'key_release_event',
            lambda event: [exit(0) if event.key == 'escape' else None])

    while True:
        c_x_index, c_y_index = sweep_searcher.move_target_grid(c_x_index,
                                                               c_y_index,
                                                               grid_map)

        if sweep_searcher.is_search_done(grid_map) or (
                c_x_index is None or c_y_index is None):
            #print("Done")
            break

        x, y = grid_map.calc_grid_central_xy_position_from_xy_index(
            c_x_index, c_y_index)

        px.append(x)
        py.append(y)

        grid_map.set_value_from_xy_index(c_x_index, c_y_index, 0.25)

        if grid_search_animation:
            grid_map.plot_grid_map(ax=ax)
            plt.pause(0.5)

    return px, py


def planning(ox, oy, resolution,
             moving_direction=SweepSearcher.MovingDirection.RIGHT,
             sweeping_direction=SweepSearcher.SweepDirection.UP,
             ):
    sweep_vec, sweep_start_position = find_sweep_direction_and_start_position(ox, oy)
    #print("planning",sweep_vec, sweep_start_position)
    rox, roy = convert_grid_coordinate(ox, oy, sweep_vec,
                                       sweep_start_position)

    grid_map, x_inds_goal_y, goal_y = setup_grid_map(rox, roy, resolution,
                                                     sweeping_direction)

    sweep_searcher = SweepSearcher(moving_direction, sweeping_direction,
                                   x_inds_goal_y, goal_y)

    px, py = sweep_path_search(sweep_searcher, grid_map)

    rx, ry = convert_global_coordinate(px, py, sweep_vec,
                                       sweep_start_position)

    #print("Path length:", len(rx))

    return rx, ry

def planningContinue(ox, oy, resolution,
             moving_direction=SweepSearcher.MovingDirection.RIGHT,
             sweeping_direction=SweepSearcher.SweepDirection.UP,
             startpoint=[0,0],direction=[0.0,0.0]
             ):
    #sweep_vec, sweep_start_position = find_sweep_direction_and_start_position(ox, oy)
    sweep_vec = direction
    sweep_start_position = startpoint
    print("planningContinue",direction, startpoint)
    rox, roy = convert_grid_coordinate(ox, oy, sweep_vec,
                                       sweep_start_position)

    grid_map, x_inds_goal_y, goal_y = setup_grid_map(rox, roy, resolution,
                                                     sweeping_direction)

    sweep_searcher = SweepSearcher(moving_direction, sweeping_direction,
                                   x_inds_goal_y, goal_y)

    px, py = sweep_path_search(sweep_searcher, grid_map)

    rx, ry = convert_global_coordinate(px, py, sweep_vec,
                                       sweep_start_position)

    #print("Path length:", len(rx))

    return rx, ry

def planning_animation(ox, oy, resolution):  # pragma: no cover
    px, py = planning(ox, oy, resolution)

    # animation
    if do_animation:
        for ipx, ipy in zip(px, py):
            plt.cla()
            # for stopping simulation with the esc key.
            plt.gcf().canvas.mpl_connect(
                'key_release_event',
                lambda event: [exit(0) if event.key == 'escape' else None])
            plt.plot(ox, oy, "-xb")
            plt.plot(px, py, "-r")
            plt.plot(ipx, ipy, "or")
            plt.axis("equal")
            plt.grid(True)
            plt.pause(0.01)

        plt.cla()
        plt.plot(ox, oy, "-xb")
        plt.plot(px, py, "-r")
        plt.axis("equal")
        plt.grid(True)
        plt.pause(0.01)
        #plt.close()
    return px, py
def GetXYScaleTB(backImagearr,terrainObj,imgL_h=760,imgL_w=1024):
    #backImagearr=[xmin,xmax,ymin,ymax,width,height]
    backImageObj={}
    backImageObj['xmin']=backImagearr[0]
    backImageObj['xmax']=backImagearr[2]
    backImageObj['ymin']=backImagearr[1]
    backImageObj['ymax']=backImagearr[3]
    backImageObj['width']=backImagearr[4]
    backImageObj['height']=backImagearr[5]
    #print(backImageObj)
    #print(terrainObj)
    # Scale_large_x
    SLX=imgL_w/backImageObj["width"]
    SLY=imgL_h/backImageObj["height"]
    SSX=terrainObj["pixW"]/terrainObj["width"]
    SSY=terrainObj["pixH"]/terrainObj["height"]

    xDist=terrainObj['xmin']-backImageObj['xmin']
    yDist=terrainObj['ymin']-backImageObj['ymin']

    return [SLX,SLY,SSX,SSY,xDist,yDist]

def GetXYTerrain(xIn,yIn,scaleArr,terrainobj):
    xOut=(xIn/scaleArr[0]-scaleArr[4])*scaleArr[2]

    yOut=(yIn/scaleArr[1]-scaleArr[5])*scaleArr[3]
    #print(yOut)
    yOut=terrainobj["pixH"]-yOut

    #print(yOut,terrainobj["pixH"])
    if xOut<0:
        xOut=0
    if xOut>=terrainobj["pixW"]:
        xOut=terrainobj["pixW"]-1
    if yOut<0:
        yOut=0
    if yOut>=terrainobj["pixH"]:
        yOut=terrainobj["pixH"]-1

    return [int(xOut),int(yOut)]
def EqualList(a,b,tlen=4):
    t=[i for i, j in zip(a, b) if i == j]
    #print(t)
    if t[0]==tlen:
        return True
    return False
def GetDensityFromColor(colorArr):
    # the more density the higher scale

    scale=0
    # color png bgra
    everyGreenForester=[99,170,104,255]
    Mixedforest=[201,201,221,255]
    Haypasture=[61,216,219,255]
    Openwater=[160,107,71,255]
    DevelopedHighIntensity=[0,0,170,255]
    Deciduousforest=[48,99,28,255]
    #print(colorArr,everyGreenForester)
    if np.array_equal(colorArr,everyGreenForester):
        scale=1
    elif np.array_equal(colorArr,Deciduousforest):
        scale=2
    elif np.array_equal(colorArr,Mixedforest):
        scale=3
    elif np.array_equal(colorArr,Openwater):
        scale=5
    return scale

def DivideRing(ringin,unitdist=0.0001):
    if len(ringin)<=0:
        return []
    resarr=[]
    for i in range(1,len(ringin)):
        xlen=ringin[i][0]-ringin[i-1][0]
        ylen=ringin[i][1]-ringin[i-1][1]
        totallen=math.sqrt(xlen**2+ylen**2)
        tncount=int(totallen/unitdist)
        xunit=xlen/tncount
        yunit=ylen/tncount
        for j in range(tncount):
            x=ringin[i-1][0]+xunit*j
            y=ringin[i-1][1]+yunit*j
            resarr.append([x,y])
        resarr.append(ringin[i])

    return resarr

def GetPath(contour_arr,terrainobj,vor_arr,index_arr,baseHeight=0, resolution = 0.0005, vorarr_spref='epsg3857',startpt=[],direction=[]):
    #print("428")
    img_h=760
    img_w=1024
    scalePixToHeight=1

    terrainImage=getImage(terrainobj["urlImage"])
    #print("contour_arr",contour_arr)
    #print("vor_arr",vor_arr)
    maxInColumns,minInColumns,discol,disrow = CalculationMaxMin(contour_arr,vor_arr)
    vor_max,vor_min,vor_discol,vor_disrow = CalculationMaxMin(vor_arr,vor_arr)

    wratio=img_w/discol
    hratio=img_h/disrow
    vor_minx_on_img=int((vor_min[0]-minInColumns[0])*wratio)
    vor_miny_on_img=int((vor_min[1]-minInColumns[1])*hratio)
    vor_width_on_img=int(vor_discol*wratio)
    vor_height_on_img=int(vor_disrow*hratio)
    terrain_image_h, terrain_image_w, _ = terrainImage.shape
    #print(terrain_image_h, terrain_image_w)

    terrain_image_ratio_h=terrain_image_h/vor_height_on_img
    terrain_image_ratio_w=terrain_image_w/vor_width_on_img

    posScaleArr=GetXYScaleTB([minInColumns[0],minInColumns[1],maxInColumns[0],maxInColumns[1],discol,disrow],terrainobj)
    imgcontour=UniformtoImage(contour_arr,maxInColumns,minInColumns,discol,disrow,img_h,img_w)
    background=ContorImageFill(imgcontour)
    #cv2.imwrite("background.jpg",background)
    #test polygon
    backgroundXLen=len(background)
    backgroundYLen=len(background[0])

    res_arr=GridSearch(vor_arr[0],resolution,startpt,direction)
    res_arr=DivideRing(res_arr,0.0002)
    res_arr=CleanPath2D(res_arr)
    #imglines=UniformArrtoImage(res_arr,maxInColumns,minInColumns,discol,disrow,img_h,img_w)

    path3D=[]
    t_h=0
    t_scale=0
    res_color=[]
    t_height=0

    tX=0
    tY=0
    item1=[0,0]
    item2=[0,0]

    t_col=[]

    #cv2.imwrite("terrain.jpg", terrainImage)
    for i in range(0,len(res_arr)-1):
        #trans res_arr to imgline
        item1[0]=int((res_arr[i][0]-minInColumns[0])*wratio)
        item1[1]=int((res_arr[i][1]-minInColumns[1])*hratio)

        item2[0]=int((res_arr[i+1][0]-minInColumns[0])*wratio)
        item2[1]=int((res_arr[i+1][1]-minInColumns[1])*hratio)

        tX1=item1[0] if item1[0]<=backgroundXLen-2 else backgroundXLen-2
        tY1=item1[1] if item1[1]<=backgroundYLen-2 else backgroundYLen-2

        tX2=item2[0] if item2[0]<=backgroundXLen-2 else backgroundXLen-2
        tY2=item2[1] if item2[1]<=backgroundYLen-2 else backgroundYLen-2

        #pick four points on the line to determine the color
        totalcol=0
        ncount=5
        xunit=(tX2-tX1)/ncount
        yunit=(tY2-tY1)/ncount
        for j in range (0,ncount):
            tX=tX1+int(xunit*j)
            tY=tY1+int(yunit*j)
            totalcol+=background[tY,tX][1]

        tX=int(0.5*tX1+0.5*tX2)
        tY=int(0.5*tY1+0.5*tY2)

        #t_h=int(background[tY,tX][1]/20)
        t_h=int(totalcol/(10*ncount))
        # terrain information

        t_pos=[int(terrain_image_ratio_w*(tX-vor_minx_on_img)),terrain_image_h-1-int(terrain_image_ratio_h*(tY-vor_miny_on_img))]
        #print(tX,tY,t_pos)
        #terrainImage=cv2.circle(terrainImage, (t_pos[0],t_pos[1]), 2, [0,0,0], 2)

        t_col=terrainImage[t_pos[1],t_pos[0]]
        t_scale=GetDensityFromColor(t_col)
        #print("t_col3:",type(t_col.tolist()))
        res_color.append([t_h-1,t_col.tolist(),t_scale])

        t_height=baseHeight+40*(11-t_h)+5*t_scale
        #t_height=baseHeight+1*255/t_h+5*t_scale
        path3D.append([res_arr[i][0],res_arr[i][1],int(scalePixToHeight*t_height)])

    res_color.append([t_h-1,t_col.tolist(),t_scale])
    #print("here")
    path3D.append([res_arr[len(res_arr)-1][0],res_arr[len(res_arr)-1][1],int(scalePixToHeight*t_height)])
    #print(posScaleArr,terrainobj)
    #print(vor_minx_on_img,vor_miny_on_img,terrain_image_ratio_w,terrain_image_ratio_h)
    #cv2.imwrite("terrain.jpg", terrainImage)
    return path3D,res_color

def Standardization(colorarr):
    res_arr=[]
    print(colorarr)
    mid_arr=map(lambda x:x[0],colorarr)
    print(mid_arr)
    mid_arr=mid_arr.sort()

    mid_index=map(lambda x:mid_arr.index(x[0]),colorarr)
    print(mid_index)
    #{colorvalue}


    return

def GetPathWeightedMap(contour_arr,terrainobj,extent_arr,vor_arr,index_arr,baseHeight=0, resolution = 0.0005, vorarr_spref='epsg3857',startpt=[],direction=[]):
    img_h=760
    img_w=1024
    scalePixToHeight=1

    terrainImage=getImage(terrainobj["urlImage"])
    maxInColumns,minInColumns,discol,disrow = CalculationMaxMin(contour_arr,extent_arr)
    vor_max,vor_min,vor_discol,vor_disrow = CalculationMaxMin(extent_arr,extent_arr)

    wratio=img_w/discol
    hratio=img_h/disrow
    vor_minx_on_img=int((vor_min[0]-minInColumns[0])*wratio)
    vor_miny_on_img=int((vor_min[1]-minInColumns[1])*hratio)
    vor_width_on_img=int(vor_discol*wratio)
    vor_height_on_img=int(vor_disrow*hratio)
    terrain_image_h, terrain_image_w, _ = terrainImage.shape
    #print(terrain_image_h, terrain_image_w)

    terrain_image_ratio_h=terrain_image_h/vor_height_on_img
    terrain_image_ratio_w=terrain_image_w/vor_width_on_img

    posScaleArr=GetXYScaleTB([minInColumns[0],minInColumns[1],maxInColumns[0],maxInColumns[1],discol,disrow],terrainobj)
    imgcontour=UniformtoImage(contour_arr,maxInColumns,minInColumns,discol,disrow,img_h,img_w)

    background=ContorImageFill(imgcontour)

    imgcontour=UniformtoImage(contour_arr,maxInColumns,minInColumns,discol,disrow,img_h,img_w)
    imgvor=UniformtoImage(vor_arr,maxInColumns,minInColumns,discol,disrow,img_h,img_w)
    backgroundWeighted = WeightedMapBackground(imgcontour,imgvor,img_h,img_w)

    #test polygon
    backgroundXLen=len(background)
    backgroundYLen=len(background[0])

    res_arr=GridSearch(extent_arr[0],resolution,startpt,direction)
    res_arr=DivideRing(res_arr,0.0002)
    res_arr=CleanPath2D(res_arr)
    #imglines=UniformArrtoImage(res_arr,maxInColumns,minInColumns,discol,disrow,img_h,img_w)

    path3D=[]
    t_h=0
    t_scale=0
    res_color=[]
    t_height=0

    tX=0
    tY=0
    item1=[0,0]
    item2=[0,0]

    #cv2.imwrite("terrain.jpg", terrainImage)
    for i in range(0,len(res_arr)-1):
        #trans res_arr to imgline
        item1[0]=int((res_arr[i][0]-minInColumns[0])*wratio)
        item1[1]=int((res_arr[i][1]-minInColumns[1])*hratio)

        item2[0]=int((res_arr[i+1][0]-minInColumns[0])*wratio)
        item2[1]=int((res_arr[i+1][1]-minInColumns[1])*hratio)

        tX1=item1[0] if item1[0]<=backgroundXLen-2 else backgroundXLen-2
        tY1=item1[1] if item1[1]<=backgroundYLen-2 else backgroundYLen-2

        tX2=item2[0] if item2[0]<=backgroundXLen-2 else backgroundXLen-2
        tY2=item2[1] if item2[1]<=backgroundYLen-2 else backgroundYLen-2

        #pick four points on the line to determine the color
        totalcol=0
        ncount=5
        xunit=(tX2-tX1)/ncount
        yunit=(tY2-tY1)/ncount
        for j in range (0,ncount):
            tX=tX1+int(xunit*j)
            tY=tY1+int(yunit*j)
            totalcol+=background[tY,tX][1]

        tX=int(0.5*tX1+0.5*tX2)
        tY=int(0.5*tY1+0.5*tY2)

        t_h=int(totalcol/(10*ncount))
        t_pos=[int(terrain_image_ratio_w*(tX-vor_minx_on_img)),terrain_image_h-1-int(terrain_image_ratio_h*(tY-vor_miny_on_img))]
        t_col=terrainImage[t_pos[1],t_pos[0]]
        t_scale=GetDensityFromColor(t_col)
        res_color.append([int(backgroundWeighted[tY,tX][0]),t_col.tolist(),t_scale])
        t_height=baseHeight+40*(11-t_h)+5*t_scale
        path3D.append([res_arr[i][0],res_arr[i][1],int(scalePixToHeight*t_height)])

    res_color.append([int(backgroundWeighted[0,0][0]),t_col.tolist(),t_scale])
    path3D.append([res_arr[len(res_arr)-1][0],res_arr[len(res_arr)-1][1],int(scalePixToHeight*t_height)])
    #print(res_color)
    return path3D,res_color


def UpdateHeight_bak(arrin,height=100,lowbar=-25,highbar=25):
    # unify the height range to height (height-90,height+200)=290, mid height == height
    arrinH=[i[2] for i in arrin]
    hmedian=statistics.median(arrinH)
    adjustVal=0
    if hmedian>height+highbar:
        adjustVal=height+highbar-hmedian
    elif hmedian<height+lowbar:
        adjustVal=height+lowbar-hmedian
    for key,item in enumerate(arrin):
        arrin[key][2]=arrin[key][2]+adjustVal
    '''
    hmin=min(arrinH)
    hmax=max(arrinH)
    scale=(high-low)/(hmax-hmin)
    for key,item in enumerate(arrin):
        arrin[key][2]=(arrin[key][2]-hmin)*scale+hmin
    '''
    return arrin

def UpdateHeight(arrin,lowbar=300,highbar=500):
    arrinH=[i[2] for i in arrin]
    hmin=min(arrinH)
    hmax=max(arrinH)
    #print(hmin,hmax)
    scale=(highbar-lowbar)/(hmax-hmin)
    for key,item in enumerate(arrin):
        arrin[key][2]= lowbar + (arrin[key][2]-hmin)*scale
    return arrin

def MaskSearchedArea(imgfense,imgpasspath,img_h=760,img_w=1024):
    background=np.zeros(shape=[img_h,img_w,3],dtype=np.uint8)
    cv2.fillPoly(background, imgfense, color=(255,255,255))
    #background=cv2.drawContours(background, imgfense, -1, (255,255,255), 1)

    #background=cv2.fillPoly(background, pts=imgpasspath, color=(255,255,255))
    isClosed = False
    color = (255,255,255)
    thickness = 20
    #print(imgpasspath)
    #mask=np.zeros(shape=[img_h,img_w,1],dtype=np.uint8)
    mask = np.zeros(background.shape[:2], dtype="uint8")
    #cv2.circle(mask, (145, 200), 100, 255, -1)
    #masked = cv2.bitwise_and(background, background, mask=mask)
    #cv2.imwrite("masked.jpg", masked)
    #return

    mask=cv2.polylines(mask, imgpasspath, isClosed,255, thickness)
    #cv2.imwrite("image.jpg", mask)

    kernel = np.ones((40, 40), dtype=np.uint8)
    dilate = cv2.dilate(mask, kernel, 1)
    dilate=cv2.drawContours(dilate, imgfense, -1, 255, 38)
    #cv2.imwrite("dilate.jpg", dilate)
    kernel = np.ones((40, 40), dtype=np.uint8)
    erosion = cv2.erode(dilate, kernel, iterations=1)

    kernel2 = np.ones((2, 2), dtype=np.uint8)
    erosion = cv2.dilate(erosion, kernel, 1)
    #cv2.imwrite("erosion.jpg", erosion)
    background[erosion == 255] = [0,0,0]
    #cv2.imwrite("background.jpg", background)

    t_imgray = cv2.cvtColor(background, cv2.COLOR_BGR2GRAY)
    ret, thresh = cv2.threshold(t_imgray, 127, 255, 0)
    #and find contours
    contours, hierarchy = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    #print(hierarchy)
    imgout=np.zeros(shape=[img_h,img_w,3],dtype=np.uint8)
    cv2.drawContours(imgout, contours, -1, (0, 255, 0), 1)
    #cv2.imwrite("imgout.jpg", imgout)
    arr_contours=[]
    arr_contours=np.array(contours).tolist()
    #print(arr_contours)
    #print(arr_contours[0])
    resarr=[]
    for item in arr_contours[0]:
        resarr.append(item[0])
    #print(resarr)
    return resarr

def ProjectImageToLocation(imagearr,img_h,img_w,maxInColumns,minInColumns,discol,disrow):
    imgarr=[]
    wratio=discol/img_w
    hratio=disrow/img_h
    for item in imagearr:
        x=item[0]*wratio+minInColumns[0]
        y=item[1]*hratio+minInColumns[1]
        imgarr.append([x,y])
    #tarr=np.array(tarr).astype(int)
    #print(tarr)
    #imgarr.append(tarr)
    #print(imgarr)
    return imgarr

def GetUpdatedPath(contour_arr,terrainobj,vor_arr,index_arr,baseHeight=0, resolution = 0.0005, vorarr_spref='epsg3857',startpt=[],direction=[],passpath=[]):
    img_h=760
    img_w=1024
    scalePixToHeight=1

    terrainImage=getImage(terrainobj["urlImage"])
    #print("shape",terrainImage.shape)

    maxInColumns,minInColumns,discol,disrow = CalculationMaxMin(contour_arr,vor_arr)

    posScaleArr=GetXYScaleTB([minInColumns[0],minInColumns[1],maxInColumns[0],maxInColumns[1],discol,disrow],terrainobj)
    #print(posScaleArr)

    imgcontour=UniformtoImage(contour_arr,maxInColumns,minInColumns,discol,disrow,img_h,img_w)

    #imgvor=UniformtoImage(vor_arr,maxInColumns,minInColumns,discol,disrow,img_h,img_w)
    #print("317",datetime.now())
    background=ContorImageFill(imgcontour)
    #cv2.imwrite("background.jpg", background)

    imgfense=UniformtoImage([vor_arr[index_arr[0]]],maxInColumns,minInColumns,discol,disrow,img_h,img_w)
    imgpasspath=UniformtoImage([passpath],maxInColumns,minInColumns,discol,disrow,img_h,img_w)
    arr_contours=MaskSearchedArea(imgfense,imgpasspath,img_h,img_w)
    res_fence=ProjectImageToLocation(arr_contours,img_h,img_w,maxInColumns,minInColumns,discol,disrow)

    #print("index_arr",background)
    #print("322",datetime.now())
    backgroundXLen=len(background)
    backgroundYLen=len(background[0])

    res_arr=GridSearch(res_fence,resolution,startpt,direction)
    res_arr=DivideRing(res_arr,0.0001)
    imglines=UniformtoImage([res_arr],maxInColumns,minInColumns,discol,disrow,img_h,img_w)
    mask = cv2.polylines(background, imglines,False,(255,0,0), 1)
    path3D=[]
    t_h_privous=1
    for i in range(0,len(res_arr)):
        item = imglines[0][i]
        tX=item[0] if item[0]<backgroundXLen else backgroundXLen-2
        tY=item[1] if item[1]<backgroundYLen else backgroundYLen-2
        #print(len(background),tX,",",tY)
        t_h=background[tX][tY][1]+1
        if t_h==1:
            t_h=t_h_privous
        t_h_privous=t_h
        t_pos=GetXYTerrain(item[0],item[1],posScaleArr,terrainobj)
        t_col=terrainImage[t_pos[1],t_pos[0]]
        t_scale=GetDensityFromColor(t_col)
        t_height=baseHeight+1*255/t_h+5*t_scale
        path3D.append([res_arr[i][0],res_arr[i][1],int(scalePixToHeight*t_height)])

    return path3D
def Plot3DArrTest(maxInColumns,minInColumns,path3D):

    z = [row[2] for row in path3D]
    x = [row[0] for row in path3D]
    y = [row[1] for row in path3D]

    fig = plt.figure()

    ax = fig.add_subplot(111, projection='3d')

    ax.plot(x,y,z) # plot the point (2,3,4) on the figure

    plt.show()

    return

def GridSearch(boundaryarr,resolution=0.0005,startpoint=[],direction=[]):
    ox=[]
    oy=[]
    for it in boundaryarr:
        ox.append(it[0])
        oy.append(it[1])
    ox.append(boundaryarr[0][0])
    oy.append(boundaryarr[0][1])
    #resx,resy=planning_animation(ox, oy, resolution)
    '''
    if len(startpoint) and len(direction)>0:
        resx,resy=planningContinue(ox, oy, resolution,SweepSearcher.MovingDirection.RIGHT,SweepSearcher.SweepDirection.UP,startpoint,direction)
    else:
        resx,resy=planning(ox, oy, resolution)
    '''

    resx,resy=planning(ox, oy, resolution)
    res_path=[]
    for i in range (0,len(resx)):
        res_path.append([resx[i],resy[i]])
    return res_path

def CleanPath(arrin):
    #print("arrin",len(arrin))
    res_arr=[]
    if len(arrin)>1:
        res_arr.append(arrin[0])
        for i in range(1,len(arrin)):
            if arrin[i][0]!=res_arr[-1][0] or arrin[i][1]!=res_arr[-1][1] or arrin[i][2]!=res_arr[-1][2]:
                res_arr.append(arrin[i])
    else:
        res_arr=arrin

    #print("res_arr",len(res_arr))
    return res_arr

def CleanPath2D(arrin):
    res_arr=[]
    if len(arrin)>1:
        res_arr.append(arrin[0])
        for i in range(1,len(arrin)):
            if arrin[i][0]!=res_arr[-1][0] or arrin[i][1]!=res_arr[-1][1]:
                res_arr.append(arrin[i])
    else:
        res_arr=arrin

    #print("res_arr",len(res_arr))
    return res_arr

#maptype 0:basic, 1: weighted, 2: heatmap
def GetPathFromCell3D(contourarr, terrainobj, extent_arr, vorarr, index_arr,baseHeight=0, resolution = 0.0005, vorarr_spref='epsg3857', maptype=0):
    # contourarr: lost person distribution
    # terrainarr: ground status of density wood or open water or openarea etc.
    # vorarr: grids

    contour_arr=[]
    vor_arr=[]

    for item in contourarr:
        contour_arr.append(np.array(item))
    for item in vorarr:
        if not item:
            vor_arr.append([])
            continue
        if vorarr_spref=='epsg3857':
            vor_arr.append(project_array(np.array(item)))
        else:
            vor_arr.append(np.array(item))

    # res is an array of coordinates, which presents the 3D points of planned path polyline
    res_obj=[]
    res_color=[]
    if maptype==1:
        #print(maptype)
        res_obj,res_color=GetPathWeightedMap(contour_arr,terrainobj,extent_arr,vor_arr,index_arr,baseHeight, resolution, 'epsg3857')
    else:
        #print(maptype)
        res_obj,res_color=GetPath(contour_arr,terrainobj,extent_arr,index_arr,baseHeight, resolution, 'epsg3857')

    return res_obj,res_color


def main():
    #print("start!!")
    id_arr=[8]
    contour_arr=loadContour(10)
    terrain_arr=contour_arr
    vor_arr=LoadVoronoi()

    res_path=GetPathFromCell3D(contour_arr,terrain_arr,vor_arr,id_arr)
    plt.show()
    #print("done!!")

def main_ori():  # pragma: no cover
    #print("start!!")
    resolution = 0.0005#0.0002

    #ox = [-80.55770859,-80.55770763,-80.55731123,-80.55573537,-80.55364948,-80.55257715]
    #oy = [37.2041,37.20423054,37.20516638,37.20643534,37.20663154,37.2041]

    #ox = [-79.34076113,-79.34068847,-79.33980432,-79.33910986,-79.33863014,-79.33793568,-79.33705153,-79.33697887,-79.33887,-79.34076113]
    #oy = [37.67999952,37.68020025,37.68089848,37.68110671,37.68110671,37.68089848,37.68020025,37.67999952,37.67825815,37.67999952]


    id=6
    contour_arr=loadContour(10)
    vor_arr=LoadVoronoi()
    #GetPathFromCell3D(contour_arr,contour_arr,vor_arr,id)
    #print(vor_arr[id])

    ox=[]
    oy=[]
    for it in vor_arr[id]:
        ox.append(it[0])
        oy.append(it[1])
    ox.append(vor_arr[id][0][0])
    oy.append(vor_arr[id][0][1])
    #print(ox,type(ox),oy)
    resx,resy=planning_animation(ox, oy, resolution)

    res_arr=[]
    for i in range (0,len(resx)):
        res_arr.append([resx[i],resy[i]])
    #print(resx,len(resx))
    #print(res_arr,len(res_arr))
    #return

    maxInColumns,minInColumns,discol,disrow = CalculationMaxMin(contour_arr,vor_arr)

    img_h=760
    img_w=1024

    imgcontour=UniformtoImage(contour_arr,maxInColumns,minInColumns,discol,disrow,img_h,img_w)
    imgvor=UniformtoImage(vor_arr,maxInColumns,minInColumns,discol,disrow,img_h,img_w)
    imglines=UniformtoImage([res_arr],maxInColumns,minInColumns,discol,disrow,img_h,img_w)

    #cv2.imshow("imgvor", imgres)
    #cv2.waitKey()


    background=np.zeros(shape=[img_h,img_w,1],dtype=np.uint8)
    item=imgvor[id]
    mask = cv2.fillPoly(background, pts =[item], color=(100))
    mask=cv2.polylines(mask, imglines,False,(255,0,0), 1)

    # get height from contour map


    cv2.imshow("mask", mask)
    #cv2.waitKey()


    if do_animation:
        plt.show()
    #print("done!!")


if __name__ == '__main__':
    main()
