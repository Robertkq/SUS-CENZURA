import ui.interface as ui

class application:
    def __init__(self):
        print("Application started")
        self.ui = ui.windowManager()
        
    def __del__(self):
        print("Application stopped")

    def run(self):
        self.ui.run()