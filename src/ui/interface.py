import tkinter as tk

class windowManager:
    def __init__(self):
        print("Window Manager started")
        self.window = tk.Tk()
        self.window.title("SUS-CENZURA")

        self.label = tk.Label(self.window, text="Hello, World!")
        self.label.pack()

        self.button = tk.Button(self.window, text="Click Me", command=self.button_click)
        self.button.pack()
        print("Window Manager initialized")

    def __del__(self):
        print("Window Manager stopped")

    def button_click(self):
        self.label.config(text="Button Clicked!")

    def run(self):
        self.window.mainloop()