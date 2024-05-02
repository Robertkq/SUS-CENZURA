import cv2

class editor:
    def __init__(self):
        pass

    def process_video(self, video_path):
        video = cv2.VideoCapture(video_path)

        if not video.isOpened():
            raise ValueError("Failed to open video file")

        while True:
            ret, frame = video.read()

            if not ret:
                break

            # TODO:processing code here

            # Display the processed frame
            cv2.imshow("Processed Frame", frame)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        # Release the video file and close the window
        video.release()
        cv2.destroyAllWindows()