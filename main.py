from email.mime import image
import tkinter as tk
import os
import pytesseract
import PIL.Image

from tkinter import filedialog, image_names
from tkinter import messagebox

WINDOW_SIZE = "400x400"
WINDOW_BACKGROUND = "#181818"
BUTTON_BACKGROUND = "#ffc000"
BUTTON_WIDTH = "10"
PAD_X = 5
PAD_Y = 10
FONT = ("Helvetica", 13)
TESS_CONFIG = r"--psm 6 --oem 3 -l pol"

class ProjectGUI:
    def __init__(self) -> None:
        self.image_path = ""
        self.root = tk.Tk()

        self.root.title("Project")
        self.root.geometry(WINDOW_SIZE)
        self.root.configure(bg=WINDOW_BACKGROUND)

        user_name_label = tk.Label(
            self.root, bg=WINDOW_BACKGROUND, fg="white", text=f"Hello, {os.getlogin()}!", font=FONT)
        user_name_label.pack(padx=PAD_X, pady=PAD_Y)

        browse_button = tk.Button(self.root, bg=BUTTON_BACKGROUND, width=BUTTON_WIDTH,
                                  font=FONT, text="Load image",
                                  command=self.load_image)
        browse_button.pack(padx=PAD_X, pady=PAD_Y)

        start_button = tk.Button(self.root, bg=BUTTON_BACKGROUND,
                                 width=BUTTON_WIDTH, font=FONT, text="Save as text", command=self.save_as_text)
        start_button.pack(padx=PAD_X, pady=PAD_Y+50)

        close_button = tk.Button(self.root, bg=BUTTON_BACKGROUND, width=BUTTON_WIDTH,
                                 font=FONT, text="Close", command=self.close_window)
        close_button.pack(padx=PAD_X, pady=PAD_Y)

        self.root.protocol("WM_DELETE_WINDOW", self.close_window)
        self.root.mainloop()

    def save_as_text(self):
        if self.image_path == "":
            messagebox.showinfo(title="Error!", message="Provide an image!")
        else:
            text = pytesseract.image_to_string(PIL.Image.open(self.image_path), config=TESS_CONFIG)
            text_file = filedialog.asksaveasfilename(
                defaultextension=".*", initialdir="C:/", title="Save File", filetypes=(("Text Files", "*.txt"),))

            if text_file:
                with open(text_file, "w", encoding="utf-8") as f:
                    f.write(text)
                    messagebox.showinfo(title="Info", message="File have been saved successfully!")

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
        image_path = self.root.filename
        temp_array = image_path.split("/")
        image_name = temp_array[len(temp_array) - 1]
        if self.root.filename:
            messagebox.showinfo(
                title="Info", message=f"File {image_name} has been loaded!")
        self.image_path = image_path

    def close_window(self):
        if messagebox.askyesno(title="Quit", message="Do you want to quit?"):
            self.root.destroy()


ProjectGUI()