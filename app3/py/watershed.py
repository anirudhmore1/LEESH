import cv2
import numpy as np
from matplotlib import pyplot as plt
import json
import math

def SetAreaSeed(rings,base):
    #rings=4
    centerpoint=[0.5,0.5]
    res_arr=[]
    #base=4# at ring 1, there are 4 areas

    for i in range(1,rings+1):
        radius=0.5*i/(rings+1)
        for j in range(0,i*base):
            angle=2*math.pi*j/(i*base)
            x=radius*math.sin(angle)+centerpoint[0]
            y=radius*math.cos(angle)+centerpoint[1]
            res_arr.append([x,y])
    return res_arr

class AreaSegment:
    #https://docs.opencv.org/3.0-beta/doc/py_tutorials/py_imgproc/py_watershed/py_watershed.html
    #watershed
    def __init__(self):
        self.myname = "watershed"

    def GetWatershedPolygon_contours(elevation_arr,img_w,img_h,t_case=0):
        t_gray=np.array(elevation_arr)
        #t_gray=t_arr[:,2]

        #t_case: 0 use highest, 1: use top and buttom
        t_mid=(np.max(t_gray)-np.min(t_gray))/2
        t_min=(np.max(t_gray)+np.min(t_gray))/2

        if t_case==1:
            t_mid=(np.max(t_gray)-np.min(t_gray))/2
            t_min=(np.max(t_gray)+np.min(t_gray))/2
        else:
            t_mid=np.max(t_gray)-np.min(t_gray)
            t_min=np.min(t_gray)


        t_arr_img=np.reshape((t_gray-t_min)*255/t_mid,(img_w,img_h))
        t_arr_img=t_arr_img.astype(int)
        t_arr_img=np.absolute(t_arr_img)
        #t_arr_img=255-t_arr_img
        t_arr_img=np.transpose(t_arr_img)
        t_arr_img=np.flip(t_arr_img)
        t_arr_img=np.flip(t_arr_img,1)

        #cv2.imwrite('bw_img.jpg', t_arr_img)
        #img = cv2.imread('bw_img.jpg')

        gray= np.uint8(t_arr_img)

        img=cv2.cvtColor(gray,cv2.COLOR_GRAY2RGB)
        t_gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
        #plt.imshow(t_gray)
        #plt.show()

        #create a same size image as the source image, and mark the unknown area as 0

        #sure_fg=np.zeros((img_w,img_h),np.int8)
        sure_fg=np.zeros(shape=[img_w,img_h,3],dtype=np.uint8)
        #sure_fg=cv2.create(img_w,img_h,CV_8UC3)
        #mark the centerpoints of front areas (0.25,0.25),(0.25,0.75),(0.75,0.25),(0.75,0.75) as 1,2,3,4
        t_seed=SetAreaSeed(3,5)
        seed_arr=np.array(t_seed)
        for item in seed_arr:
            sure_fg[np.uint8(img_w*item[0]),np.uint8(img_h*item[1])]=[255,255,255]

        kernel = np.ones((3,3),np.uint8)
        sure_fg_large = cv2.dilate(sure_fg,kernel,iterations=4)
        ret, sure_fg = cv2.threshold(sure_fg_large,0.5*sure_fg_large.max(),255,0)

        #plt.imshow(sure_fg)
        #plt.show()


        sure_fg = cv2.cvtColor(sure_fg, cv2.COLOR_BGR2GRAY)
        ret, markers = cv2.connectedComponents(sure_fg)

        markers = cv2.watershed(img,markers)

        img[markers == -1] = [255,0,0]

        # labelling each area, front white 255, background black 0
        img_bw=img
        arr_contours=[]
        for x in range (1,len(t_seed)+1):
            img_bw[:]=[0,0,0]
            img_bw[markers == x]=[255,255,255]
            t_imgray = cv2.cvtColor(img_bw, cv2.COLOR_BGR2GRAY)

            ret, thresh = cv2.threshold(t_imgray, 127, 255, 0)
            #and find contours
            contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
            arr_contours.append(np.array(contours).tolist())

        im_color = cv2.applyColorMap(np.uint8(markers*255/9), cv2.COLORMAP_JET)
        #cv2.imwrite('ws.jpg', im_color)
        #plt.imshow(im_color)
        #plt.show()
        return arr_contours# [  [[[1,2,3]],[[1,2,3]]],     ... ]


    def GetWatershedPolygon_backup(elevation_arr,img_w,img_h,t_case=0):
        t_gray=np.array(elevation_arr)
        #t_gray=t_arr[:,2]

        #t_case: 0 use highest, 1: use top and buttom
        t_mid=(np.max(t_gray)-np.min(t_gray))/2
        t_min=(np.max(t_gray)+np.min(t_gray))/2

        if t_case==1:
            t_mid=(np.max(t_gray)-np.min(t_gray))/2
            t_min=(np.max(t_gray)+np.min(t_gray))/2
        else:
            t_mid=np.max(t_gray)-np.min(t_gray)
            t_min=np.min(t_gray)


        t_arr_img=np.reshape((t_gray-t_min)*255/t_mid,(img_w,img_h))
        t_arr_img=t_arr_img.astype(int)
        t_arr_img=np.absolute(t_arr_img)
        #t_arr_img=255-t_arr_img
        t_arr_img=np.transpose(t_arr_img)
        t_arr_img=np.flip(t_arr_img)
        t_arr_img=np.flip(t_arr_img,1)

        #cv2.imwrite('bw_img.jpg', t_arr_img)
        #img = cv2.imread('bw_img.jpg')

        gray= np.uint8(t_arr_img)

        img=cv2.cvtColor(gray,cv2.COLOR_GRAY2RGB)
        t_gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
        #plt.imshow(t_gray)
        #plt.show()

        #create a same size image as the source image, and mark the unknown area as 0

        #sure_fg=np.zeros((img_w,img_h),np.int8)
        sure_fg=np.zeros(shape=[img_w,img_h,3],dtype=np.uint8)
        #sure_fg=cv2.create(img_w,img_h,CV_8UC3)
        #mark the centerpoints of front areas (0.25,0.25),(0.25,0.75),(0.75,0.25),(0.75,0.75) as 1,2,3,4
        pt_x=5
        pt_y=5
        step_x=1/pt_x
        step_y=1/pt_y
        for x in range(1,pt_x+1):
            t_x=(x-0.5)*step_x*img_w
            for y in range(1,pt_y+1):
                t_y=(y-0.5)*step_y*img_h
                sure_fg[np.uint8(t_x)-1,np.uint8(t_y)-1]=[255,255,255]


        kernel = np.ones((6,6),np.uint8)
        sure_fg_large = cv2.dilate(sure_fg,kernel,iterations=4)
        ret, sure_fg = cv2.threshold(sure_fg_large,0.5*sure_fg_large.max(),255,0)

        #plt.imshow(sure_fg)
        #plt.show()


        sure_fg = cv2.cvtColor(sure_fg, cv2.COLOR_BGR2GRAY);
        ret, markers = cv2.connectedComponents(sure_fg)

        markers = cv2.watershed(img,markers)

        img[markers == -1] = [255,0,0]

        # labelling each area, front white 255, background black 0
        img_bw=img
        arr_contours=[]
        for x in range (1,pt_x*pt_y+1):
            img_bw[:]=[0,0,0]
            img_bw[markers == x]=[255,255,255]
            t_imgray = cv2.cvtColor(img_bw, cv2.COLOR_BGR2GRAY)
            #plt.imshow(t_imgray)
            #plt.show()

            ret, thresh = cv2.threshold(t_imgray, 127, 255, 0)
            #and find contours
            contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
            arr_contours.append(np.array(contours).tolist())

            #print(contours)
            #cv2.drawContours(img, contours, -1, (0,255,0), 1)
            #plt.imshow(img)
            #plt.show()

        im_color = cv2.applyColorMap(np.uint8(markers*255/9), cv2.COLORMAP_JET)
        plt.imshow(im_color)
        plt.show()
        return arr_contours# [  [[[1,2,3]],[[1,2,3]]],     ... ]
    def GetWatershedPolygon_vironoi(elevation_arr,img_w,img_h,t_case=0):
        t_gray=np.array(elevation_arr)
        #t_gray=t_arr[:,2]

        #t_case: 0 use highest, 1: use top and buttom
        t_mid=(np.max(t_gray)-np.min(t_gray))/2
        t_min=(np.max(t_gray)+np.min(t_gray))/2

        if t_case==1:
            t_mid=(np.max(t_gray)-np.min(t_gray))/2
            t_min=(np.max(t_gray)+np.min(t_gray))/2
        else:
            t_mid=np.max(t_gray)-np.min(t_gray)
            t_min=np.min(t_gray)


        t_arr_img=np.reshape((t_gray-t_min)*255/t_mid,(img_w,img_h))
        t_arr_img=t_arr_img.astype(int)
        t_arr_img=np.absolute(t_arr_img)
        #t_arr_img=255-t_arr_img
        t_arr_img=np.transpose(t_arr_img)
        t_arr_img=np.flip(t_arr_img)
        t_arr_img=np.flip(t_arr_img,1)

        #cv2.imwrite('bw_img.jpg', t_arr_img)
        #img = cv2.imread('bw_img.jpg')

        gray= np.uint8(t_arr_img)
        img=cv2.cvtColor(gray,cv2.COLOR_GRAY2RGB)
        #gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

        #create a same size image as the source image, and mark the unknown area as 0

        #sure_fg=np.zeros((img_w,img_h),np.int8)
        sure_fg=np.zeros(shape=[img_w,img_h,3],dtype=np.uint8)
        #sure_fg=cv2.create(img_w,img_h,CV_8UC3)
        #mark the centerpoints of front areas (0.25,0.25),(0.25,0.75),(0.75,0.25),(0.75,0.75) as 1,2,3,4
        pt_x=3
        pt_y=3
        step_x=1/pt_x
        step_y=1/pt_y
        for x in range(1,pt_x+1):
            t_x=(x-0.5)*step_x*img_w
            for y in range(1,pt_y+1):
                t_y=(y-0.5)*step_y*img_h
                sure_fg[np.uint8(t_x)-1,np.uint8(t_y)-1]=[255,255,255]

        kernel = np.ones((6,6),np.uint8)
        sure_fg_large = cv2.dilate(sure_fg,kernel,iterations=4)
        ret, sure_fg = cv2.threshold(sure_fg_large,0.5*sure_fg_large.max(),255,0)

        plt.imshow(sure_fg)
        plt.show()

        # Marker labelling
        sure_fg = cv2.cvtColor(sure_fg, cv2.COLOR_BGR2GRAY);
        ret, markers = cv2.connectedComponents(sure_fg)

        markers = cv2.watershed(img,markers)

        img[markers == -1] = [255,0,0]

        im_color = cv2.applyColorMap(np.uint8(markers*255/9), cv2.COLORMAP_JET)
        plt.imshow(im_color)
        plt.show()
        return img_w#[[1,2,3],[1,2,3]]

    def GetAdaptiveThresholdingPolygon(elevation_arr,img_w,img_h,t_case=0):
        t_gray=np.array(elevation_arr)
        #t_gray=t_arr[:,2]

        #t_case: 0 use highest, 1: use top and buttom
        t_mid=(np.max(t_gray)-np.min(t_gray))/2
        t_min=(np.max(t_gray)+np.min(t_gray))/2

        if t_case==1:
            t_mid=(np.max(t_gray)-np.min(t_gray))/2
            t_min=(np.max(t_gray)+np.min(t_gray))/2
        else:
            t_mid=np.max(t_gray)-np.min(t_gray)
            t_min=np.min(t_gray)


        t_arr_img=np.reshape((t_gray-t_min)*255/t_mid,(img_w,img_h))
        t_arr_img=t_arr_img.astype(int)
        t_arr_img=np.absolute(t_arr_img)
        #t_arr_img=255-t_arr_img
        t_arr_img=np.transpose(t_arr_img)
        t_arr_img=np.flip(t_arr_img)
        t_arr_img=np.flip(t_arr_img,1)

        img= np.uint8(t_arr_img)

        img = cv2.medianBlur(img,5)

        ret,th1 = cv2.threshold(img,127,255,cv2.THRESH_BINARY)

        th2 = cv2.adaptiveThreshold(img,255,cv2.ADAPTIVE_THRESH_MEAN_C,\
                    cv2.THRESH_BINARY,11,2)
        th3 = cv2.adaptiveThreshold(img,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,\
                    cv2.THRESH_BINARY,11,2)

        titles = ['Original Image', 'Global Thresholding (v = 127)',
                    'Adaptive Mean Thresholding', 'Adaptive Gaussian Thresholding']
        images = [img, th1, th2, th3]

        for i in range(4):
            plt.subplot(2,2,i+1),plt.imshow(images[i],'gray')
            plt.title(titles[i])
            plt.xticks([]),plt.yticks([])
        plt.show()
        return img_w#[[1,2,3],[1,2,3]]
