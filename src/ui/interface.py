import tkinter as tk
from tkinter import filedialog
from pubsub import pub
from PIL import Image, ImageTk

class windowManager:
    def __init__(self):
        print("Window Manager started")
        self.window = self.create_window()
        self.button_frame = self.create_button_frame()
        self.buttons = self.create_buttons()
        self.sub_window = self.create_sub_window()
        self.file_path = ""
        self.video_loaded = False
        self.edit_frame_shown = False
        self.edit_frame_initialized = False
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

        self.edit_button = tk.Button(self.button_frame, text="Edit", command=self.open_edit_frame)
        self.edit_button.pack(side=tk.LEFT, fill=tk.X, expand=True)
        buttons["edit"] = self.edit_button

        return buttons

    def create_sub_window(self):
        self.sub_window = tk.Frame(self.window, bg="grey")
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
            if not self.edit_frame_initialized:
                self.label.config(text="Please select edit options before starting processing")
            else:
                pub.sendMessage('start_processing', file_path=self.file_path)
        else:
            self.label.config(text="No file loaded, load a file to begin processing")

    def open_edit_frame(self):
        if self.edit_frame_shown:
            self.edit_frame_shown = False
            self.edit_frame.place_forget()
        else:
            self.edit_frame_initialized=True
            self.edit_frame = tk.Frame(self.window)
            self.edit_frame.place(x=0, y=25, relwidth=0.1, relheight=1)

            self.edit_frame_shown = True
            self.blur_options_label = tk.Label(self.edit_frame, text="Select objects to blur")
            self.blur_options_label.pack()
            self.blur_options = ["Faces", "License"]
            self.blur_listbox = tk.Listbox(self.edit_frame, selectmode=tk.MULTIPLE, selectbackground='blue', selectforeground='white')
            for option in self.blur_options:
                self.blur_listbox.insert(tk.END, option)
            self.blur_listbox.pack()

            self.blur_type_label = tk.Label(self.edit_frame, text="Blur Type")
            self.blur_type_label.pack()

            self.blur_type_options = ["Normal", "Gaussian", "Motion", "Radial"]
            self.blur_type_var = tk.StringVar(self.edit_frame)
            self.blur_type_var.set(self.blur_type_options[0])  # default value
            self.blur_type_optionmenu = tk.OptionMenu(self.edit_frame, self.blur_type_var, *self.blur_type_options)
            self.blur_type_optionmenu.pack()

            self.blur_level_label = tk.Label(self.edit_frame, text="Blur Level")
            self.blur_level_label.pack()

            self.blur_level_scale = tk.Scale(self.edit_frame, from_=1, to=10, orient=tk.HORIZONTAL)
            self.blur_level_scale.pack()

    def get_settings(self):
        settings = {}
        settings["blur_options"] = self.blur_listbox.curselection()
        settings["blur_type"] = self.blur_type_var.get()
        settings["blur_level"] = self.blur_level_scale.get()
        return settings
        
    def update_frame(self, frame):
        # Convert the frame to an image
        self.original_image = Image.fromarray(frame)

        # Get the current width and height of the main window
        width = self.sub_window.winfo_width()
        height = self.sub_window.winfo_height()

        # Resize the image
        self.resize_image(width, height)

        if self.label is None:
            self.label = tk.Label(self.sub_window, image=self.image)
            self.label.image = self.image
            self.label.pack()
        else:
            self.label.configure(image=self.image)
            self.label.image = self.image

    def resize_image(self, width, height):
        # Resize the original image
        resized_image = self.original_image.resize((width, height))

        # Create a new PhotoImage object
        self.image = ImageTk.PhotoImage(resized_image)