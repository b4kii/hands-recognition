from tkinter import *
# from PIL import ImageTK, Image
from tkinter import filedialog

root = Tk()
root.title("Test")

root.filename = filedialog.askopenfilename(
    initialdir="C:/",
    title="Select a file",
    filetypes=(
        ("png files", "*.png"), 
        ("jpg files", "*.jpg"),
        ("all files", "*.*"),
    )
)

root.mainloop()
