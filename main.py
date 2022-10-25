import tkinter as tk
import os
import pytesseract

from PIL import ImageTk, Image
from tkinter import filedialog
from tkinter import messagebox
from time import strftime
from CountingTracking import tracker

WINDOW_SIZE = "300x500"
WINDOW_BACKGROUND = "#181818"
BUTTON_BACKGROUND = "#ffc000"
BUTTON_WIDTH = "12"
PAD_X = 5
PAD_Y = 20
FONT = ("Helvetica", 13)
TESS_CONFIG = r"--psm 6 --oem 3 -l pol"

class ProjectGUI:
    def __init__(self) -> None:
        self.image_path = ""
        self.root = tk.Tk()

        self.root.title("Project")
        self.root.geometry(WINDOW_SIZE)
        self.root.configure(bg=WINDOW_BACKGROUND)

        self.user_name_label = tk.Label(
            self.root, bg=WINDOW_BACKGROUND, fg="white", text=f"Hello, {os.getlogin()}!", font=FONT)
        self.user_name_label.pack(padx=PAD_X, pady=PAD_Y)

        self.browse_button = tk.Button(self.root, bg=BUTTON_BACKGROUND, width=BUTTON_WIDTH,
                                  font=FONT, text="Load image",
                                  command=self.load_image)
        self.browse_button.pack(padx=PAD_X, pady=PAD_Y)

        self.save_text = tk.Button(self.root, bg=BUTTON_BACKGROUND,
                                 width=BUTTON_WIDTH, font=FONT, text="Save as text", command=self.save_as_text)
        self.save_text.pack(padx=PAD_X, pady=PAD_Y)

        self.hand_recognition = tk.Button(self.root, bg=BUTTON_BACKGROUND,
                                 width=BUTTON_WIDTH, font=FONT, text="Hand tracking", command=tracker)
        self.hand_recognition.pack(padx=PAD_X, pady=PAD_Y)

        self.clock_label = tk.Label(self.root, bg=WINDOW_BACKGROUND, fg="white", font=FONT, pady=PAD_Y)
        self.clock_label.pack(expand=True, anchor="s")
        self.clock()

        self.root.protocol("WM_DELETE_WINDOW", self.close_window)
        self.root.mainloop()

    def save_as_text(self):
        if self.image_path == "":
            messagebox.showinfo(title="Error!", message="Provide an image!")
        else:
            text = pytesseract.image_to_string(Image.open(self.image_path), config=TESS_CONFIG)
            text_file = filedialog.asksaveasfilename(
                defaultextension=".*", initialdir="C:/", title="Save File", filetypes=(("Text Files", "*.txt"),))

            if text_file:
                with open(text_file, "w", encoding="utf-8") as f:
                    f.write(text)
                    messagebox.showinfo(title="Info", message="File has been saved successfully!")

    def load_image(self):
        self.root.filename = filedialog.askopenfilename(
            initialdir="C:/",
            title="Select a file",
            filetypes=(
                ("PNG (*.png)", "*.png"),
                ("JPG (*.jpg)", "*.jpg"),
                ("All Files", "*.*"),
            )
        )
        temp_array = self.root.filename.split("/")
        image_name = temp_array[len(temp_array) - 1]
        if self.root.filename:
            messagebox.showinfo(
                title="Info", message=f"File {image_name} has been loaded!")
        self.image_path = self.root.filename

    def close_window(self):
        if messagebox.askyesno(title="Quit", message="Do you want to quit?"):
            self.root.destroy()
    
    def clock(self):
        string = strftime('%H:%M:%S %p')
        self.clock_label.config(text = string)
        self.clock_label.after(1000, self.clock)


ProjectGUI()