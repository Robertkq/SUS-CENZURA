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
        
    def __del__(self):
        print("Application stopped")
    
    def load_video_handle(self, file_path):
        print("File path:", file_path)

    def start_processing_handle(self, file_path):
        print("Processing started")
        self.editor.process_video(file_path)
        print("Processing finished")


    def run(self):
        self.ui.run()