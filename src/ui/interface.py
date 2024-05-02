import tkinter as tk
from tkinter import filedialog
from pubsub import pub

class windowManager:
    def __init__(self):
        print("Window Manager started")
        self.window = self.create_window()
        self.button_frame = self.create_button_frame()
        self.buttons = self.create_buttons()
        self.sub_window = self.create_sub_window()
        self.file_path = ""
        self.video_loaded = False
        print("Window Manager initialized")

    def create_window(self):
        window = tk.Tk()
        window.title("SUS-CENZURA")
        window.geometry("1280x720")
        return window

    def create_button_frame(self):
        button_frame = tk.Frame(self.window)
        button_frame.pack(side=tk.TOP, fill=tk.X)
        return button_frame

    def create_buttons(self):
        buttons = {}
        self.load_button = tk.Button(self.button_frame, text="Load", command=self.load_video)
        self.load_button.pack(side=tk.LEFT, fill=tk.X, expand=True)
        buttons["load"] = self.load_button

        self.start_button = tk.Button(self.button_frame, text="Start", command=self.start_processing)
        self.start_button.pack(side=tk.LEFT, fill=tk.X, expand=True)
        buttons["start"] = self.start_button

        self.save_button = tk.Button(self.button_frame, text="Save")
        self.save_button.pack(side=tk.LEFT, fill=tk.X, expand=True)
        buttons["save"] = self.save_button

        self.edit_button = tk.Button(self.button_frame, text="Edit")
        self.edit_button.pack(side=tk.LEFT, fill=tk.X, expand=True)
        buttons["edit"] = self.edit_button

        return buttons

    def create_sub_window(self):
        self.sub_window = tk.Frame(self.window, bg="grey", bd=5)
        self.sub_window.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        self.label = tk.Label(self.sub_window, text="Load a file to begin processing")
        self.label.pack()
        return self.sub_window

    def __del__(self):
        print("Window Manager stopped")

    def run(self):
        self.window.mainloop()

    def load_video(self):
        self.file_path = filedialog.askopenfilename(filetypes=[("Video files", "*.mp4 *.avi")])
        if self.file_path:
            self.video_loaded = True
            self.label.config(text="Video loaded, press start to begin processing")
        else:
            self.video_loaded = False
            self.label.config(text="No file selected, load a file to begin processing")

    def start_processing(self):
        if self.video_loaded:
            pub.sendMessage('start_processing', file_path=self.file_path)
            video_loaded = False
        else:
            self.label.config(text="No file loaded, load a file to begin processing")
        