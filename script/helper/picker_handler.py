# File and color picker function
import tkinter as tk
from tkinter import filedialog, colorchooser 

def pick_file(result:list,
              display:tk.Button=None,
              window_title:str="Select file",
              file_types:list=[("All files", "*.*"),("GIF","*.gif"),("PNG","*.png")]):
    """
    Edit the result list in place to contain a list of path(s) of the file 
    """
    paths = filedialog.askopenfilenames(title=window_title, filetypes=file_types)
    if paths:
        result[:] = list(paths)
        if display is not None:
            display.set("\n".join(result))
    else:
        result.clear()
        if display is not None:
            display.set("No files selected")

def pick_color(result:list, 
               button:tk.Button=None):
    """
    Edit the result list in place and changes the button display to that color
    """
    color = colorchooser.askcolor(color="#808080")
    if color[1]:
        result.set(color[1])
        if button is not None:
            button.config(bg=color[1])