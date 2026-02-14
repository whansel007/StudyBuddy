# Default creation 
import tkinter as tk
from tkinter import ttk

def create_animation_entry(parent, 
                           label_text:str, 
                           button_command, 
                           default_value:str=None, 
                           default_interval:float = 0.1, 
                           font_default:tuple=None, 
                           font_bold:tuple = None, 
                           default_width:tuple=None):
    """
    Creates a frame for animation selection.
    """
    frame = ttk.Frame(master=parent)
    
    paths = []

    var_selection = tk.StringVar(value="No file selected")

    if default_value:
        paths=default_value
        var_selection=tk.StringVar(value=paths)

    label = ttk.Label(master=frame, text=label_text, font=font_bold)
    label_selection = ttk.Label(master=frame, textvariable=var_selection, font=font_default)
    button_select = tk.Button(master=frame,
                                    command=lambda: button_command(paths, var_selection),
                                    text="Select Sprites",
                                    bg="#19CEE6")

    frame_interval = ttk.Frame(master=frame)
    label_interval = ttk.Label(master=frame_interval, text="Frame interval:", font=font_default)
    entry_interval = ttk.Entry(master=frame_interval, font=font_default, width=default_width)
    entry_interval.insert(0, default_interval)

    label.pack(pady=default_width)
    label_selection.pack(pady=default_width)
    button_select.pack(pady=default_width)

    frame_interval.pack(pady=6)
    label_interval.pack(side="left",pady=default_width)
    entry_interval.pack(side="right",pady=default_width)
    
    return frame, paths, entry_interval

def create_general_entry(parent, label_text:str, num_entries:int=1, default_value:tuple = (),font_bold:tuple=None, font_default:tuple=None, width_value=20):
    """
    Creates a frame with a label and a specified number of entry widgets.
    """
    frame = ttk.Frame(master=parent)
    label = ttk.Label(master=frame, text=label_text, font=font_bold)
    label.pack()

    if num_entries > 1:
        entries = []
        entry_frame = ttk.Frame(master=frame)
        for i in range(num_entries):
            entry = ttk.Entry(master=entry_frame, font=font_default, width=width_value)
            entry.pack(side="left", padx=2)
            entry.insert(0, str(default_value[i]))
            entries.append(entry)
        entry_frame.pack()
    else:
        entry = ttk.Entry(master=frame, font=font_default, width=width_value)
        entry.insert(0, str(default_value))
        entry.pack()
        entries = entry

    return frame, entries

def create_color_entry(parent, label_text:str, button_comand, font_bold:tuple=None, font_default:tuple=None):
    """
    Creates a frame for color selection and changes the color of the button to that color
    """
    frame = ttk.Frame(master=parent)
    label = ttk.Label(master=parent, text=label_text, font=font_bold)

    var_selection = tk.StringVar(value="#808080")
    label_selection = ttk.Label(master=frame, textvariable=var_selection, font=font_default)
    button = tk.Button(master=frame,
                                text="Pick Colour",
                                bg=var_selection.get(),
                                command=lambda: button_comand(var_selection, button))

    label.pack()
    label_selection.pack()
    button.pack(pady=6)

    return frame, var_selection
