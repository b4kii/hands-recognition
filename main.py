import tkinter as tk
import os
import pytesseract
import cv2

from PIL import ImageTk, Image
from tkinter import filedialog
from tkinter import messagebox
from tkinter.font import Font
from time import strftime

from CountingTracking import tracker

WINDOW_SIZE = "300x500"
WINDOW_BACKGROUND = "#181818"
BUTTON_BACKGROUND = "#ffc000"
BUTTON_WIDTH = "12"
PAD_X = 5
PAD_Y = 20
FONT = ("Segoe Print", 13)
CLOCK_FONT = ("Segoe Script", 12)
TESS_CONFIG = r"--psm 6 --oem 3 -l pol"

class ProjectGUI:
    def __init__(self):
        self.image_path = ""
        self.root = tk.Tk()

        BIG_FONT = Font(
            family="Segoe Print",
            size=32,
            weight="bold",
            slant="roman",
            underline=0
        )

        self.root.title("Project")
        self.root.geometry(WINDOW_SIZE)
        self.root.configure(bg=WINDOW_BACKGROUND)

        self.user_name_label = tk.Label(
            self.root, bg=WINDOW_BACKGROUND, fg="white", text=f"Hello, {os.getlogin()}!", font=BIG_FONT)
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

        self.clock_label = tk.Label(
            self.root, bg=WINDOW_BACKGROUND, fg="white", font=CLOCK_FONT, pady=PAD_Y)
        self.clock_label.pack(expand=True, anchor="s")
        self.clock()

        self.root.protocol("WM_DELETE_WINDOW", self.close_window)
        self.root.mainloop()

    def save_as_text(self):
        if self.image_path == "":
            messagebox.showinfo(title="Error!", message="Provide an image!")
        else:
            text = pytesseract.image_to_string(
                Image.open(self.image_path), config=TESS_CONFIG)
            text_file = filedialog.asksaveasfilename(
                defaultextension=".*", initialdir="C:/", title="Save File", filetypes=(("Text Files", "*.txt"),))

            if text_file:
                with open(text_file, "w", encoding="utf-8") as f:
                    f.write(text)
                    messagebox.showinfo(
                        title="Info", message="File has been saved successfully!")

    def display_boxes(self):
        image = cv2.imread(self.image_path)
        height, width, _ = image.shape

        boxes = pytesseract.image_to_boxes(image, config=TESS_CONFIG)
        for box in boxes.splitlines():
            box = box.split(" ")
            image = cv2.rectangle(image, (int(box[1]), height - int(box[2])), (int(box[3]), height - int(box[4])), (0, 255, 0))

        cv2.imshow("Detected letters", image)
        cv2.waitKey(0)


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
            self.display_boxes()

    def close_window(self):
        if messagebox.askyesno(title="Quit", message="Do you want to quit?"):
            self.root.destroy()

    def clock(self):
        string = strftime('%H:%M:%S %p')
        self.clock_label.config(text=string)
        self.clock_label.after(1000, self.clock)


ProjectGUI()
