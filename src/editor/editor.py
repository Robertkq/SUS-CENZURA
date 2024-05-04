import cv2 as cv
from pubsub import pub

class editor:
    def __init__(self):
        pass

    def process_video(self, video_path, settings):
        print("Processing started")
        print("Settings: ", settings)
        video = cv.VideoCapture(video_path)
        frame_count = int(video.get(cv.CAP_PROP_FRAME_COUNT))
        
        if not video.isOpened():
            raise ValueError("Failed to open video file")

        # Load the Haar cascade xml file for face detection
        face_cascade = cv.CascadeClassifier('models\\haarcascade_frontalface_default.xml')
        width = 640
        height = 480
        frame_counter = 0
        while True:
            ret, frame = video.read()

            if not ret:
                break

            # Downsize the frame for face detection
            small_frame = cv.resize(frame, (width, height))

            # Convert the small frame to grayscale
            gray = cv.cvtColor(small_frame, cv.COLOR_BGR2GRAY)

            # Perform face detection on the small frame
            cv.setNumThreads(4)
            faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

            # Scale the face coordinates back to the original frame size
            faces = [(x * frame.shape[1] // width, y * frame.shape[0] // height, w * frame.shape[1] // width, h * frame.shape[0] // height) for (x, y, w, h) in faces]

            for (x, y, w, h) in faces:
                pass
                # TODO: add bluring logic here

            if frame_counter % 20 == 0:
                for (x, y, w, h) in faces:
                    cv.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
                print(f"Processing frame {frame_counter}/{frame_count}")
                rgb_frame = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
                pub.sendMessage('update_frame', frame=rgb_frame)

            
            frame_counter += 1

        video.release()
        print("Processing finished")