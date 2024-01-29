#!/usr/bin/env python
# coding: utf-8
# Based on restful freamwork
# refer to https://2.python-requests.org//en/latest/user/quickstart/
#
# In[1]:
import requests
import time
import random
#r = requests.get('http://127.0.0.1:8000/gpsdatas/')

# In[4]:
def GetRandomPath(start_log,start_lat,range=0.1):
    t1=random.random()
    t2=random.random()
    tlog=start_log+0.1*(t1-0.4)
    tlat=start_lat+0.1*(t2-0.4)
    return tlog,tlat

def postforcreate():
    start_log=-80
    start_lat=37
    username='tianzi'
    password='tianzi'
    for i in range(0,1):

        tlog,tlat=GetRandomPath(start_log,start_lat,0.1)
        gpsdata='{"stamp":'+ str(i) +',"timestamp":'+str(int(time.time())) +',"lat":'+str(tlat)+',"long":'+str(tlog)+'}'
        # post: create new item
        r = requests.post('http://127.0.0.1:8000/gpsdatas/', auth=(username,password), data = {'deviceid':'max_test_100', 'taskid':'sar_put','gpsdata':gpsdata})

        # use post before patch
        # patch: always update
        #r = requests.patch('http://127.0.0.1:8000/gpsdatas/max_test_100/', auth=(username,password), data = {'deviceid':'max_test_100', 'taskid':'sar_put','gpsdata':gpsdata})
        print(r)
        input("Press Enter to continue...")
    return

def main():
    start_log=-80.3
    start_lat=37.1
    username='tianzi'
    password='tianzi'
    for i in range(0,10):

        tlog,tlat=GetRandomPath(start_log,start_lat,0.1)
        gpsdata='{"stamp":'+ str(i) +',"timestamp":'+str(int(time.time())) +',"lat":'+str(tlat)+',"long":'+str(tlog)+'}'
        # post: create new item
        # r = requests.patch('http://127.0.0.1:8000/gpsdatas/', auth=(username,password), data = {'deviceid':'max_test_100', 'taskid':'sar_put','gpsdata':gpsdata})

        # use post before patch
        # patch: always update
        # max_test_100, drone_test1,drone_test0
        r = requests.patch('http://127.0.0.1:8000/gpsdatas/max_test_100/', auth=(username,password), data = {'deviceid':'max_test_100', 'taskid':'sar_put','gpsdata':gpsdata})
        print(r)
        input("Press Enter to continue...")
#r = requests.post('http://127.0.0.1:8000/gpsdatas/', data = {'deviceid':'test_2nd', 'taskid':'sar001','gpsdata':'{"gps":["stamp":004,"lat":-80,"log":37]}'})
if __name__ == '__main__':
    main()

    #postforcreate()
