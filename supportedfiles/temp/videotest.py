import cv2

# Specify the path to your video file
video_file_path = '30_min_car.mp4'

# Open the video file
cap = cv2.VideoCapture(video_file_path)

# Check if the video file opened successfully
if not cap.isOpened():
    print("Error: Could not open video file.")
    exit()

while True:
    # Read a frame from the video file
    ret, frame = cap.read()

    # Check if the frame was read successfully
    if not ret:
        print("Error: Could not read frame.")
        break

    # Display the frame
    cv2.imshow("Video Capture", frame)

    # Break the loop when 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the video file and close the OpenCV window
cap.release()
cv2.destroyAllWindows()
