# Entry point and settings
import tkinter as tk
import os
import json
from tkinter import ttk, filedialog, colorchooser 
from pathlib import Path
from pet_script.pet_class import pet
from pet_script.pet_spritehandler import resize

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

def pick_color(result, button):
    color = colorchooser.askcolor(color="#808080")
    if color[1]:
        result.set(color[1])
        button.config(bg=color[1])
        print(result.get())

def create_pet(pet_container, info_dict):
    new_pet = pet(tk_root, info_dict)
    pet_container.append(new_pet)


def load_pet(pet_container):
    load_path = filedialog.askopenfilename(initialdir=os.getcwd())
    with open(load_path, "r") as load_file:
        info_dict = json.load(load_file)
        print(info_dict)
        create_pet(pet_container, info_dict)
    

def launch_pet(pet_container):
    name = entry_name.get()
    pos_x, pos_y = (int(entry_pos_x.get()),int(entry_pos_y.get()))
    size_x, size_y = (int(entry_size_x.get()),int(entry_size_y.get()))
    chromakey = str(var_chromakey_selection.get())

    info_dict = {
        "name": name,
        "pos_x": pos_x,
        "pos_y": pos_y,
        "size_x": size_x,
        "size_y": size_y,
        "sprites_idle": resize(ani_idle_paths,
                              (size_x, size_y),
                                (name, "idle")),
        "sprites_walk": resize(ani_walk_paths,  
                              (size_x, size_y),
                                (name, "walk")),
        "chroma_key": chromakey,
        "prompt" : f"You are {name} and you are a desktop pet",
    }

    save_path = Path(name) / f"{name}_({size_x}x{size_y}).json"
    with open(save_path, "w", encoding="utf-8") as save_file:
        json.dump(info_dict,save_file, indent=4)
    
    create_pet(pet_container, info_dict)

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

label_ani = ttk.Label(master=frame_ani, text="Animation Frames [PNG or  GIF]", font=bold_font)

# Idle Animation
ani_idle_paths = []
var_ani_idle_selection = tk.StringVar(value="No file selected")

frame_ani_idle = ttk.Frame(master=frame_ani)
label_ani_idle = ttk.Label(master=frame_ani_idle, text="Idle Animation Frame(s):", font=default_font)
label_ani_idle_selection = ttk.Label(master=frame_ani_idle, textvariable=var_ani_idle_selection, font=default_font)
button_ani_idle_select = ttk.Button(master=frame_ani_idle,
                                    command=lambda: pick_file(ani_idle_paths, var_ani_idle_selection),
                                    text="Select Idle Sprites")

label_ani.pack()
label_ani_idle.pack()
label_ani_idle_selection.pack()
button_ani_idle_select.pack()

# Walk Animation
ani_walk_paths = []
var_ani_walk_selection = tk.StringVar(value="No file selected")

frame_ani_walk = ttk.Frame(master=frame_ani)
label_ani_walk = ttk.Label(master=frame_ani_walk, text="Walk Animation Frame(s):", font=default_font)
label_ani_walk_selection = ttk.Label(master=frame_ani_walk, textvariable=var_ani_walk_selection, font=default_font)
button_ani_walk_select = ttk.Button(master=frame_ani_walk,
                                    command=lambda: pick_file(ani_walk_paths, var_ani_walk_selection),
                                    text="Select Walk Sprites")

label_ani.pack()
label_ani_walk.pack()
label_ani_walk_selection.pack()
button_ani_walk_select.pack()

frame_ani_idle.pack(pady=default_padding)
frame_ani_walk.pack(pady=default_padding)
frame_ani.pack(pady=default_padding)

# Chromakey Entry
var_chromakey_selection = tk.StringVar(value="#808080")

frame_chromakey = ttk.Frame(master=tk_root)
label_chromakey = ttk.Label(master=frame_chromakey, text="Outline Color [A color not on the sprite]", font=bold_font)
label_chromakey_selection = ttk.Label(master=frame_chromakey, textvariable=var_chromakey_selection, font=default_font)
button_chromakey = tk.Button(master=frame_chromakey,
                             text="Pick Out Line Color",
                             bg=var_chromakey_selection.get(),
                             command=lambda: pick_color(var_chromakey_selection, button_chromakey))

label_chromakey.pack()
label_chromakey_selection.pack()
button_chromakey.pack(pady=default_padding)
frame_chromakey.pack(pady=default_padding)

# Create pet button
button_create_pet = ttk.Button(tk_root, text="Create Pet!", command=lambda: launch_pet(list_pets))
button_create_pet.pack(pady=10)

# Create pet button
button_load_pet = ttk.Button(tk_root, text="Load Pet!", command=lambda: load_pet(list_pets))
button_load_pet.pack(pady=10)

# Start the Tkinter event loop 
tk_root.mainloop()
