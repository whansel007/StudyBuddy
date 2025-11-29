# Entry point and settings

import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from pet_class import pet
from pet_spritehandler import resize

def pick_file(result: list,
              display=None,
              window_title="Select file",
              file_types=[("GIF","*.gif"),("PNG","*.png"),("All files", "*.*")]):
    paths = filedialog.askopenfilenames(title=window_title, filetypes=file_types)
    if paths:
        result[:] = list(paths)
        if display is not None:
            display.set("\n".join(result))
    else:
        result.clear()
        if display is not None:
            display.set("No files selected")
    print(result)


def launch_pet(pet_container):
    name = entry_name.get()
    pos_x, pos_y = (int(entry_pos_x.get()),int(entry_pos_y.get()))
    size_x, size_y = (int(entry_size_x.get()),int(entry_size_y.get()))


    info_dict = {
        "name": name,
        "pos_x": pos_x,
        "pos_y": pos_y,
        "size_x": size_x,
        "size_y": size_y,
        "spites_idle": resize(ani_idle_paths, 
                              (size_x, size_y),
                                (name, "idle")),
        "spites_walk": resize(ani_walk_paths, 
                              (size_x, size_y),
                                (name, "walk")),
        "state" : "idle",
        "move_x": 0,
        "move_y": 0,
        "frame" : "",
    }
    print(info_dict)
    new_pet = pet(tk_root, info_dict)
    pet_container.append(new_pet)

# List to hold pet instances
list_pets = []

# Main window
tk_root = tk.Tk()
tk_root.title("Settings")
tk_root.geometry("600x600")

# Default configs
default_padding = 6
default_font = ("Comic Sans MS", 10)
bold_font = ("Comic Sans MS", 12, "bold")

# Name Entry
frame_name = ttk.Frame(master=tk_root)

label_name = ttk.Label(master=frame_name, text="Pet name:", font=bold_font)
entry_name = ttk.Entry(master=frame_name, font=default_font)

label_name.pack()
entry_name.pack()
frame_name.pack(pady=default_padding)

# Pos Entry
frame_pos = ttk.Frame(master=tk_root)

label_pos = ttk.Label(master=frame_pos, text="Pet position (x,y):", font=bold_font)
entry_pos_x = ttk.Entry(master=frame_pos, font=default_font)
entry_pos_y = ttk.Entry(master=frame_pos, font=default_font)

label_pos.pack()
entry_pos_x.pack(side="left")
entry_pos_y.pack(side="right")
frame_pos.pack(pady=default_padding)

# Size Entry
frame_size = ttk.Frame(master=tk_root)

label_size = ttk.Label(master=frame_size, text="Pet size (x,y):", font=bold_font)
entry_size_x = ttk.Entry(master=frame_size, font=default_font)
entry_size_y = ttk.Entry(master=frame_size, font=default_font)

label_size.pack()
entry_size_x.pack(side="left")
entry_size_y.pack(side="right")
frame_size.pack(pady=default_padding)

# Animation
frame_ani = ttk.Frame(master=tk_root)

label_ani = ttk.Label(master=frame_ani, text="Animation Frames", font=bold_font)

# Idle Animation
ani_idle_paths = []
var_ani_idle_selection = tk.StringVar(value="No file selected")

frame_ani_idle = ttk.Frame(master=frame_ani)
label_ani_idle = ttk.Label(master=frame_ani_idle, text="Idle Animation Frame(s): \n[PNG or  GIF]", font=default_font)
label_ani_idle_selection = ttk.Label(master=frame_ani_idle, textvariable=var_ani_idle_selection, font=default_font)
button_ani_idle_select = ttk.Button(
    master=frame_ani_idle,
    command=lambda: pick_file(ani_idle_paths, var_ani_idle_selection),
    text="Select Idle Sprites"
)

label_ani.pack()
label_ani_idle.pack()
label_ani_idle_selection.pack()
button_ani_idle_select.pack()

# Walk Animation
ani_walk_paths = []
var_ani_walk_selection = tk.StringVar(value="No file selected")

frame_ani_walk = ttk.Frame(master=frame_ani)
label_ani_walk = ttk.Label(master=frame_ani_walk, text="Walk Animation Frame(s) \n[PNG or  GIF]:", font=default_font)
label_ani_walk_selection = ttk.Label(master=frame_ani_walk, textvariable=var_ani_walk_selection, font=default_font)
button_ani_walk_select = ttk.Button(
    master=frame_ani_walk,
    command=lambda: pick_file(ani_walk_paths, var_ani_walk_selection),
    text="Select Walk Sprites"
)

label_ani.pack()
label_ani_walk.pack()
label_ani_walk_selection.pack()
button_ani_walk_select.pack()

frame_ani_idle.pack(pady=default_padding)
frame_ani_walk.pack(pady=default_padding)
frame_ani.pack(pady=default_padding)

# Create pet button
button_create_pet = ttk.Button(tk_root, text="Create Pet!", command=lambda: launch_pet(list_pets))
button_create_pet.pack(pady=20)

# Start the Tkinter event loop 
tk_root.mainloop()
