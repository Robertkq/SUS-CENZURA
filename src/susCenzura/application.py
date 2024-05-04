from pubsub import pub
import ui.interface as ui
import editor.editor as editor
import threading
import time

class application:
    def __init__(self):
        print("Application started")
        self.ui = ui.windowManager()
        self.editor = editor.editor()
        pub.subscribe(self.load_video_handle, 'load_video')
        pub.subscribe(self.start_processing_handle, 'start_processing')
        pub.subscribe(self.update_frame_handle, 'update_frame')
        
    def __del__(self):
        print("Application stopped")
    
    def load_video_handle(self, file_path):
        print("File path:", file_path)

    def start_processing_handle(self, file_path):
        settings = self.ui.get_settings()
        worker = threading.Thread(target=self.editor.process_video, args=(file_path, settings))
        worker.start()

    def update_frame_handle(self, frame):
        self.ui.update_frame(frame)

    def run(self):
        self.ui.run()