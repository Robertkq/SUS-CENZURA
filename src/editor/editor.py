import cv2 as cv
from pubsub import pub

class editor:
    def __init__(self):
        self.width = 640
        self.height = 480
        pass

    def process_video(self, video_path, settings):
        print("Processing started")
        blur_options_aux = settings['blur_options']
        blur_options = self.name_options(blur_options_aux)
        blur_type = settings['blur_type']
        blur_level = settings['blur_level']

        print(f"Blur options selected   : ", blur_options)
        print(f"Blur type selected      : ", blur_type)
        print(f"Blur level selected     : ", blur_level)
        blur_level *= 10

        models = self.load_models(blur_options)

        print(f"Models loaded: ", models)

        video = cv.VideoCapture(video_path)
        if not video.isOpened():
            raise ValueError("Failed to open video file")
        
        frame_count = int(video.get(cv.CAP_PROP_FRAME_COUNT))
        print(f"Total frames            : ", frame_count)
        

        cascades = []
        for model in models:
            cascades.append(cv.CascadeClassifier(model))

        
        frame_counter = 0
        while True:
            ret, frame = video.read()
            if not ret:
                break

            # Downsize the frame for face detection
            small_frame = cv.resize(frame, (self.width, self.height))

            # Convert the small frame to grayscale
            gray = cv.cvtColor(small_frame, cv.COLOR_BGR2GRAY)

            # Perform face detection on the small frame
            real_faces = []
            for cascade in cascades:
                cv.setNumThreads(4)
                faces = cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30), flags=cv.CASCADE_SCALE_IMAGE)
                # Convert the face coordinates to the original frame size
                real_faces = [(x * frame.shape[1] // self.width, y * frame.shape[0] // self.height, w * frame.shape[1] // self.width, h * frame.shape[0] // self.height) for (x, y, w, h) in faces]
                for (x, y, w, h) in real_faces:
                    roi = frame[y:y+h, x:x+w]
                    blurred_roi = cv.blur(roi, (blur_level, blur_level))
                    frame[y:y+h, x:x+w] = blurred_roi

            if frame_counter % 20 == 0:
                print(f"Processed frame {frame_counter}/{frame_count}")
                rgb_frame = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
                pub.sendMessage('update_frame', frame=rgb_frame)

            
            frame_counter += 1

        video.release()
        print("Processing finished")

    def name_options(self, blur_options):
        blur_options_string = ["Faces", "License"]
        to_return = {}
        for i in range(len(blur_options_string)):
            if i in blur_options:
                to_return[blur_options_string[i]] = blur_options[i]
        return to_return

    def load_models(self, blur_options):
        models = []
        if 'Faces' in blur_options:
            models.append('models\\haarcascade_frontalface_default.xml')
            models.append('models\\haarcascade_profileface.xml')
        if 'License' in blur_options:
            models.append('models\\haarcascade_license_plate_rus_16stages.xml')
        return models