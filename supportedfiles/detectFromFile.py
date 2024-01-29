import cv2
import numpy as np

from flask import Response
from flask import Flask
from flask import render_template
import threading
import argparse
import datetime
import imutils
import time
from imutils.video import VideoStream

# https://www.ispyconnect.com/userguide-agent-api.aspx
outputFrame = None
#app = Flask(__name__)
#lock = threading.Lock()
#vs = VideoStream(src='http://localhost:8090/video.mp4?oids=1,2,3&size=320x240').start()

#time.sleep(1.0)

hog = cv2.HOGDescriptor()
hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())

car_data=cv2.CascadeClassifier('cars.xml')


def test():
    global vs,outputFrame, lock,car_data,hog
    total=0
    cap = cv2.VideoCapture('30_min_car.mp4')
    print(cap)
    a=0
    while(True):
        a=a+1
        ret, frame = cap.read()

        #frame = imutils.resize(frame, width=400)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        found = car_data.detectMultiScale(gray, minSize=(20, 20))

        #https://pyimagesearch.com/2015/11/09/pedestrian-detection-opencv/
        amount_found=len(found)
        if amount_found!=0:
            for (x,y,width,height) in found:
                cv2.rectangle(frame, (x, y), (x+height, y+width),(255, 0, 0), 1)

        timestamp = datetime.datetime.now()
        cv2.putText(frame, timestamp.strftime("%A %d %B %Y %I:%M:%S%p"), (10, frame.shape[0] - 10),cv2.FONT_HERSHEY_SIMPLEX, 0.35, (0, 0, 255), 1)
        total += 1

        #cv2.imwrite("test.png",frame)
        cv2.imshow('frame',frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            cv2.destroyAllWindows()
            break

    cap.release()
    cv2.destroyAllWindows()

def detect(img_gray, tVal=25):
    global car_data, hog
    if img_gray is None:
        return None

    # cars.xml
    # cv2.data.haarcascades +'haarcascade_fullbody.xml'
    found = car_data.detectMultiScale(img_gray, minSize=(20, 20))

    body_data=cv2.CascadeClassifier(cv2.data.haarcascades +'haarcascade_fullbody.xml')
    found_body=body_data.detectMultiScale(img_gray,minSize =(20, 20))

    return found, found_body


def detect_motion_v1(frameCount):
    global vs, outputFrame, lock, car_data, hog
    total = 0
    while (True):
        frame = vs.read()
        # frame = imutils.resize(frame, width=400)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        found, found_body = detect(gray)
        amount_found = len(found)
        if amount_found != 0:
            for (x, y, width, height) in found:
                cv2.rectangle(frame, (x, y), (x + height, y + width), (255, 0, 0), 1)

        amount_found = len(found_body)
        if amount_found != 0:
            for (x, y, width, height) in found:
                cv2.rectangle(frame, (x, y), (x + height, y + width), (0, 255, 0), 1)

        # if total > frameCount:
        #    cv2.rectangle(frame, (startX, startY), (endX, endY),(255, 0, 0), 2)
        # cv2.imshow('frame',frame)

        timestamp = datetime.datetime.now()
        cv2.putText(frame, timestamp.strftime("%A %d %B %Y %I:%M:%S%p"), (10, frame.shape[0] - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.35, (0, 0, 255), 1)
        total += 1
        with lock:
            outputFrame = frame.copy()


def detect_motion(frameCount):
    global vs,outputFrame, lock,car_data,hog
    total=0
    while(True):
        frame = vs.read()
        #frame = imutils.resize(frame, width=400)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        found = car_data.detectMultiScale(gray, minSize=(20, 20))
        (rects, weights) = hog.detectMultiScale(gray, winStride=(4, 4), padding=(8, 8), scale=1.05)

        #https://pyimagesearch.com/2015/11/09/pedestrian-detection-opencv/
        amount_found=len(found)
        if amount_found!=0:
            for (x,y,width,height) in found:
                cv2.rectangle(frame, (x, y), (x+height, y+width),(255, 0, 0), 1)

        for (x, y, w, h) in rects:
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 1)

        timestamp = datetime.datetime.now()
        cv2.putText(frame, timestamp.strftime("%A %d %B %Y %I:%M:%S%p"), (10, frame.shape[0] - 10),cv2.FONT_HERSHEY_SIMPLEX, 0.35, (0, 0, 255), 1)
        total += 1
        with lock:
            outputFrame = frame.copy()

def ipcameraserver():
    global vs,outputFrame, lock
    cap = cv2.VideoCapture('http://localhost:8090/video.mp4?oids=1,2,3&size=320x240')
    while(True):
        ret, frame = cap.read()
        #cv2.imshow('frame',frame)
        startX=20
        startY=20

        endX=40
        endY=30

        cv2.rectangle(frame, (startX, startY), (endX, endY),
					(255, 0, 0), 2)
        with lock:
            outputFrame = frame.copy()
        if cv2.waitKey(1) & 0xFF == ord('q'):
            cv2.destroyAllWindows()
            break

    cap.release()
    cv2.destroyAllWindows()
    return


def generate():
	# grab global references to the output frame and lock variables
	global outputFrame, lock
	# loop over frames from the output stream
	while True:
		# wait until the lock is acquired
		with lock:
			# check if the output frame is available, otherwise skip
			# the iteration of the loop
			if outputFrame is None:
				continue
			# encode the frame in JPEG format
			(flag, encodedImage) = cv2.imencode(".jpg", outputFrame)
			# ensure the frame was successfully encoded
			if not flag:
				continue
		# yield the output frame in the byte format
		yield(b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' +
			bytearray(encodedImage) + b'\r\n')


if __name__ == "__main__":
    test()
    #main()
    '''
    ap = argparse.ArgumentParser()
    ap.add_argument("-i", "--ip", type=str, required=True,help="ip address of the device")
    ap.add_argument("-o", "--port", type=int, required=True,help="ephemeral port number of the server (1024 to 65535)")
    ap.add_argument("-f", "--frame-count", type=int, default=32,help="# of frames used to construct the background model")

    #t = threading.Thread(target=detect_motion, args=(args["frame_count"],))
    t = threading.Thread(target=detect_motion, args=("4",))
    t.daemon = True
    t.start()

    #args = vars(ap.parse_args())
    # start the flask app
    #app.run(host=args["ip"], port=args["port"], debug=True,threaded=True, use_reloader=False)
    app.run(host="0.0.0.0", port="8889", debug=True,threaded=True, use_reloader=False)
    '''
