import cv2
import threading
from flask import Flask, Response
import datetime
import time

app = Flask(__name__)
video_file_path = '30_min_car.mp4'
# Open the video file (change 'video.mp4' to the path of your video file)
car_data=cv2.CascadeClassifier('cars.xml')
video_capture= cv2.VideoCapture(video_file_path)
def generate_frames():
    a=0
    video_capture = cv2.VideoCapture(video_file_path)
    if not video_capture.isOpened():
        print("Error: Could not open video file.")
        exit()
    while True:
        success, frame = video_capture.read()
        if not success:
            break
        else:
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            found = car_data.detectMultiScale(gray, minSize=(20, 20))
            amount_found=len(found)
            if amount_found!=0:
                for (x,y,width,height) in found:
                    cv2.rectangle(frame, (x, y), (x+height, y+width),(255, 0, 0), 1)

            timestamp = datetime.datetime.now()
            cv2.putText(frame, timestamp.strftime("%A %d %B %Y %I:%M:%S%p"), (10, frame.shape[0] - 10),cv2.FONT_HERSHEY_SIMPLEX, 0.35, (0, 0, 255), 1)

            _, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/')
def index():
    return "Welcome to the video streaming server!"

@app.route('/video')
def video():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == "__main__":
    t = threading.Thread(target=app.run, args=('127.0.0.1', 5000))
    t.daemon = True
    t.start()
    video_capture.release()
    t.join()
