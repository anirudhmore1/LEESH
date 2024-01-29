import os
import numpy as np
import cv2
from matplotlib import pyplot as plt
import json

from pyproj import Proj, transform
from pyproj import Transformer

def loadArrayFromFile(inrange=10):
    #arr=[]
    all_arr=[]
    maxxy=[]
    minxy=[]
    for i in range(inrange):
        with open(f"temp/Ring_{i}.txt",'r') as f:
            content=f.read()
            #arr=json.dumps(content)
            a=json.loads(content)
            #print(a)
            arr=np.array(a)
            #print(np.shape(arr))

            maxInColumns = np.amax(arr,axis=0)
            minInColumns = np.amin(arr,axis=0)

            maxxy.append(maxInColumns)
            minxy.append(minInColumns)

            all_arr.append(arr)
    all_arr=np.array(all_arr)
    #print(np.shape(all_arr))
    print(maxxy,minxy)
    maxInColumns = np.amax(maxxy,axis=0)
    minInColumns = np.amin(minxy,axis=0)
    #print(maxInColumns,minInColumns)
    discol = maxInColumns[0]-minInColumns[0]
    disrow = maxInColumns[1]-minInColumns[1]
    print(maxInColumns,minInColumns,discol,disrow)

    imgarr=[]
    img_h,img_w=760,1024
    wratio=img_w/discol
    hratio=img_h/disrow
    for iarr in all_arr:
        tarr=[]
        for item in iarr:
            x=(item[0]-minInColumns[0])*wratio
            y=(item[1]-minInColumns[1])*hratio
            tarr.append([x,y])
        tarr=np.array(tarr).astype(int)
        imgarr.append(tarr)
    #imgarr=np.array(imgarr,dtype=np.uint8)
    #print(imgarr[0])
    return imgarr

def LoadVoronoi():
    arr=[]
    with open(f"temp/voronoiori.txt",'r') as f:
        content=f.read()
        a=json.loads(content)
        #tindex=0
        for item in a:
            #print(item)
            a=project_array(np.array(item))
            #tindex=tindex+1
            #print(tindex,a[0])
            arr.append(np.array(a))
    return arr

def loadContour_1(inrange=10):
    #arr=[]
    all_arr=[]
    maxxy=[]
    minxy=[]
    for i in range(inrange):
        with open(f"temp/Ring_{i}.txt",'r') as f:
            content=f.read()
            #arr=json.dumps(content)
            a=json.loads(content)
            #print(a)
            arr=np.array(a)
            #print(np.shape(arr))

            maxInColumns = np.amax(arr,axis=0)
            minInColumns = np.amin(arr,axis=0)

            maxxy.append(maxInColumns)
            minxy.append(minInColumns)

            all_arr.append(arr)
    all_arr=np.array(all_arr)
    #print(np.shape(all_arr))
    print(maxxy,minxy)
    maxInColumns = np.amax(maxxy,axis=0)
    minInColumns = np.amin(minxy,axis=0)
    #print(maxInColumns,minInColumns)
    discol = maxInColumns[0]-minInColumns[0]
    disrow = maxInColumns[1]-minInColumns[1]
    print(maxInColumns,minInColumns,discol,disrow)
    return all_arr,maxInColumns,minInColumns,discol,disrow

def loadContour(inrange=10):
    #arr=[]
    all_arr=[]
    maxxy=[]
    minxy=[]
    for i in range(inrange):
        with open(f"temp/Ring_{i}.txt",'r') as f:
            content=f.read()
            a=json.loads(content)
            arr=np.array(a)
            all_arr.append(arr)
    all_arr=np.array(all_arr)
    return all_arr

def CalculationMaxMin(arr1,arr2):
    maxxy=[]
    minxy=[]
    for arr in arr1:
        maxInColumns = np.amax(arr,axis=0)
        minInColumns = np.amin(arr,axis=0)

        maxxy.append(maxInColumns)
        minxy.append(minInColumns)

    for arr in arr2:
        maxInColumns = np.amax(arr,axis=0)
        minInColumns = np.amin(arr,axis=0)

        maxxy.append(maxInColumns)
        minxy.append(minInColumns)

    #print(np.shape(all_arr))
    print(maxxy,minxy)
    maxInColumns = np.amax(maxxy,axis=0)
    minInColumns = np.amin(minxy,axis=0)
    #print(maxInColumns,minInColumns)
    discol = maxInColumns[0]-minInColumns[0]
    disrow = maxInColumns[1]-minInColumns[1]
    print(maxInColumns,minInColumns,discol,disrow)
    return maxInColumns,minInColumns,discol,disrow

def UniformtoImage(all_arr,maxInColumns,minInColumns,discol,disrow,img_h=760,img_w=1024):
    imgarr=[]
    wratio=img_w/discol
    hratio=img_h/disrow
    for iarr in all_arr:
        #print(minInColumns,iarr)
        tarr=[]
        for item in iarr:
            x=(item[0]-minInColumns[0])*wratio
            y=(item[1]-minInColumns[1])*hratio
            tarr.append([x,y])
        #print(tarr)
        tarr=np.array(tarr).astype(int)
        #print(tarr)
        imgarr.append(tarr)
    return imgarr


def project_array(coordinates, srcp='latlong', dstp='wintri'):
    """
    Project a numpy (n,2) array in projection srcp to projection dstp
    Returns a numpy (n,2) array.
    from wkid: 102100,EPSG:3857  to { wkid: 4326  }, WGS84,epsg:4326
    """
    transformer = Transformer.from_crs("epsg:3857", "epsg:4326")
    fx, fy = transformer.transform(coordinates[:,0], coordinates[:,1])
    '''
    p1 = Proj('epsg:3857')
    p2 = Proj('epsg:4326')
    #print(coordinates[:,0])
    fx, fy = transform(p1, p2, coordinates[:,0], coordinates[:,1])
    '''
    # Re-create (n,2) coordinates
    return np.dstack([fy,fx])[0]

def ContorImageFill(contours,img_h=760,img_w=1024):
    #the first one is the largest
    #img_h,img_w=760,1024
    background=np.zeros(shape=[img_h,img_w,3],dtype=np.uint8)
    #imgcountor=cv2.drawContours(background, contours, -1, (0,255,0), 1)
    #imgcountor=cv2.fillPoly(background, pts =[contours[0]], color=(255,255,255))
    #cv2.imshow("image", imgcountor)
    colorindex=1
    for item in contours:
        colorweigth=colorindex*20
        background=cv2.fillPoly(background, pts =[item], color=(0,colorweigth,0))
        colorindex+=1
    #cv2.imshow("image", background)
    #cv2.waitKey()

    return background

def ContorImageFill_multi(contours,voronoiarr,img_h=760,img_w=1024):
    #the first one is the largest
    #img_h,img_w=760,1024
    background=np.zeros(shape=[img_h,img_w,3],dtype=np.uint8)

    colorindex=1
    for item in contours:
        colorweigth=colorindex*20
        background=cv2.fillPoly(background, pts =[item], color=(0,colorweigth,0))
        colorindex+=1
    background=cv2.drawContours(background, voronoiarr, -1, (0,0,255), 1)
    cv2.imshow("image", background)
    cv2.waitKey()

    return background
def ContorImage(contours1,contours2,img_h=760,img_w=1024):
    background=np.zeros(shape=[img_h,img_w,3],dtype=np.uint8)
    colorindex=1
    background=cv2.drawContours(background, contours1, -1, (0,255,0), 1)
    background=cv2.drawContours(background, contours2, -1, (0,0,255), 1)
    cv2.imshow("image", background)
    cv2.waitKey()

    return

def ContorImageFill_chanel1(contours,img_h=760,img_w=1024):
    #the first one is the largest
    background=np.zeros(shape=[img_h,img_w,1],dtype=np.uint8)
    colorindex=1
    for item in contours:
        colorweigth=colorindex*20
        background=cv2.fillPoly(background, pts =[item], color=(colorweigth))
        colorindex+=1
    #cv2.imshow("image", background)
    #cv2.waitKey()

    return background

def Imageslice(imgcontour,imgvor,img_h=760,img_w=1024):
    resval=[]
    imgcontour=ContorImageFill_chanel1(imgcontour)
    #cv2.imshow("image", imgcontour)
    #cv2.waitKey()

    for item in imgvor:
        #use item as mask
        background=np.zeros(shape=[img_h,img_w,1],dtype=np.uint8)
        mask = cv2.fillPoly(background, pts =[item], color=(1))
        timg=np.multiply(imgcontour,mask)
        totalpixel = np.sum(mask)
        totalval = np.sum(timg)
        resval.append([totalpixel,totalval])
        #cv2.imshow("image2", timg)
        #cv2.waitKey()
    index=0
    #print(resval)
    background=np.zeros(shape=[img_h,img_w,1],dtype=np.uint8)
    for item in imgvor:
        color=int(resval[index][1]/resval[index][0])
        index=index+1
        background = cv2.fillPoly(background, pts =[item], color=(color))
    cv2.imshow("image", background)
    cv2.waitKey()
    return resval

def SegmentWeight(contourarr,vorarr):
    #contour_arr = loadContour(10)
    #vor_arr=LoadVoronoi()
    contour_arr=[]
    vor_arr=[]
    for item in contourarr:
        contour_arr.append(np.array(item))
    for item in vorarr:
        vor_arr.append(np.array(item))
    maxInColumns,minInColumns,discol,disrow = CalculationMaxMin(contour_arr,vor_arr)

    imgcontour=UniformtoImage(contour_arr,maxInColumns,minInColumns,discol,disrow,img_h=760,img_w=1024)
    imgvor=UniformtoImage(vor_arr,maxInColumns,minInColumns,discol,disrow,img_h=760,img_w=1024)
    #ContorImage(imgcontour,imgvor)
    ContorImageFill_multi(imgcontour,imgvor)
    res = Imageslice(imgcontour,imgvor)
    print(res)
    return res


if __name__ == '__main__':
    #imgarr=loadArrayFromFile(10)
    contour_arr = loadContour(10)
    vor_arr=LoadVoronoi()
    maxInColumns,minInColumns,discol,disrow = CalculationMaxMin(contour_arr,vor_arr)

    imgcontour=UniformtoImage(contour_arr,maxInColumns,minInColumns,discol,disrow,img_h=760,img_w=1024)
    imgvor=UniformtoImage(vor_arr,maxInColumns,minInColumns,discol,disrow,img_h=760,img_w=1024)
    #ContorImage(imgcontour,imgvor)
    ContorImageFill_multi(imgcontour,imgvor)
    res = Imageslice(imgcontour,imgvor)
