from pubsub import pub
import ui.interface as ui
import threading
import time

class application:
    def __init__(self):
        print("Application started")
        self.ui = ui.windowManager()
        pub.subscribe(self.load_video_handle, 'load_video')
        
    def __del__(self):
        print("Application stopped")
    
    def load_video_handle(self, file_path):
        print("File path:", file_path)


    def run(self):
        self.ui.run()