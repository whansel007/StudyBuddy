# Entry point and settings
import tkinter as tk
import json
from tkinter import ttk, filedialog
from pathlib import Path
from script.pet.pet_class import pet
from script.helper.sprite_handler import resize
from script.helper.ui_creation import create_general_entry, create_animation_entry, create_color_entry
from script.helper.picker_handler import pick_file,pick_color

# Pet Container
list_pets = []

# Default configs
default_padding = 6
default_width = 5
default_font = ("Comic Sans MS", 10)
default_boldfont = ("Comic Sans MS", 12, "bold")

default_name = "DefaultPet"
default_pos_x = -150
default_pos_y = -150
default_size_x = 125
default_size_y = 125
default_speed_x = 10
default_speed_y = 10
default_idlesprite = str(Path("asset") / "default_idle.gif")
default_walksprite = str(Path("asset") / "default_walk.gif")
default_spriteinterval = 0.1
default_idleinterval = 3
default_treshhold = (5,5)

# Main window
def test(position):
    print(position)
    print("test")

tk_root = tk.Tk()
tk_root.bind("<Button-3>", test)
screensize = (tk_root.winfo_screenwidth(), tk_root.winfo_screenheight())
tk_root.title("Settings")
tk_root.geometry("500x800")

# Name Entry
frame_name, (entry_name) = create_general_entry(tk_root, "Pet name:", default_value=default_name, font_bold= default_boldfont, font_default= default_font)
frame_name.pack(pady=default_padding)

# Pos Entry
frame_pos, (entry_pos_x, entry_pos_y) = create_general_entry(tk_root, "Pet position (x,y):", 2, default_value= (default_pos_x, default_pos_y), font_bold=default_boldfont, font_default=default_font)
frame_pos.pack(pady=default_padding)
label_screensize = ttk.Label(master=frame_pos, text=f"Your screensize : {str(screensize)}", font=default_font)
label_screensize.pack()

# Size Entry
frame_size, (entry_size_x, entry_size_y) = create_general_entry(tk_root, "Pet size (x,y):", 2, default_value=(default_size_x, default_size_y),font_bold=default_boldfont,font_default= default_font)
frame_size.pack(pady=default_padding)

# Speed Entry
frame_speed, (entry_speed_x, entry_speed_y) = create_general_entry(tk_root, "Pet speed (x,y):", 2, default_value=(default_speed_x, default_speed_y), font_bold=default_boldfont, font_default=default_font)
frame_speed.pack(pady=default_padding)

# Animation
frame_ani = ttk.Frame(master=tk_root)
label_ani = ttk.Label(master=frame_ani, text="Animation Frames [GIF or PNG]", font=default_boldfont)
label_ani.pack()

frame_ani_idle, ani_idle_paths, var_ani_idle_selection, entry_ani_idle_interval = create_animation_entry(frame_ani, "Idle Animation Frame(s):", pick_file, default_value=default_idlesprite, default_interval= default_spriteinterval, font_default= default_font, default_width=default_width)
frame_ani_idle.pack(pady=default_padding)

frame_ani_walk, ani_walk_paths, var_ani_walk_selection, entry_ani_walk_interval = create_animation_entry(frame_ani, "Walk Animation Frame(s):", pick_file, default_value=default_walksprite, default_interval=default_spriteinterval, font_default= default_font, default_width=default_width)
frame_ani_idle.pack(pady=default_padding)

frame_ani_walk.pack(pady=default_padding)

frame_ani.pack(pady=default_padding)

# Chromakey Entry
frame_chromakey, var_chromakey_selection = create_color_entry(tk_root, "Outline Color [Color must not already be in sprite]", pick_color, default_boldfont, default_font)
frame_chromakey.pack(pady=default_padding)

# Additional settings button
action_interval = None
action_treshold = None

def open_additionalsettings():
    """
    Open the additional settings window
    """
    # Additional settings window
    window_additionalsettings = tk.Toplevel(tk_root)
    window_additionalsettings.title("Additional Settings")
    window_additionalsettings.geometry("400x400")

    label_warning = tk.Label(master=window_additionalsettings, text="CLOSE THIS BEFORE LAUNCHING PET!")
    label_warning.pack(pady=default_padding)

    def close_additionalsettings():
        print("Duar")
        action_interval = entry_action_interval.get()
        action_treshold = (entry_action_tresholdleft.get(), entry_action_tresholdright.get())

        window_additionalsettings.destroy()

    window_additionalsettings.protocol("WM_DELETE_WINDOW", close_additionalsettings)
    # Action interval entry
    frame_action_interval, (entry_action_interval) = create_general_entry(window_additionalsettings, "Idle action interval (in seconds):", 1, font_bold=default_boldfont, font_default=default_font)
    frame_action_interval.pack(pady=default_padding)

    # Action treshhold entry
    frame_action_treshold, (entry_action_tresholdleft, entry_action_tresholdright) = create_general_entry(window_additionalsettings, "Idle action treshold:", 2, font_bold=default_boldfont, font_default=default_font)
    frame_action_treshold.pack(pady=default_padding)

button_settings = ttk.Button(tk_root, text="Additional Settings...", command=open_additionalsettings)
button_settings.pack(pady=10)

# Create pet and load button
def launch_pet(pet_container:list, info_dict:dict):
    """
    Creates a pet object according to the info_dict, and appends that pet object into the container list
    """
    
    new_pet = pet(tk_root, info_dict)
    pet_container.append(new_pet)
    print(pet_container)

def load_pet(pet_container:list):
    """
    Loads a .json file as the info dict and launches the pet with that info dict
    """
    load_path = filedialog.askopenfilename(initialdir="pets")
    with open(load_path, "r") as load_file:
        info_dict = json.load(load_file)
        print(info_dict)
        launch_pet(pet_container, info_dict)

# In case u screw up, delete the default value I already put in, and launches the pet with an empty entry
def get_with_default(entry:tk.Entry, default_value, value_type:type = int):
    value = entry.get()

    if value:
        return value_type(value)
    else:
        return default_value

def create_pet(pet_container:list):
    """
    Extracts the information from all entries, compiles them into the info dict, saves the info dict as a.json and uses that info dict to launch a pet 
    """
    name = get_with_default(entry_name, default_name, str)

    pos_x = get_with_default(entry_pos_x, default_pos_x)
    pos_y = get_with_default(entry_pos_y, default_pos_y)

    size_x = get_with_default(entry_size_x, default_size_x) 
    size_y = get_with_default(entry_size_y, default_size_y)

    speed_x = get_with_default(entry_speed_x, default_speed_x)
    speed_y = get_with_default(entry_speed_y, default_speed_y)

    sprite_idleinterval = get_with_default(entry_ani_idle_interval, default_spriteinterval, float)
    sprite_walkinterval = get_with_default(entry_ani_walk_interval, default_spriteinterval, float)
    
    chromakey = var_chromakey_selection.get()

    save_path = Path("pets") / name / f"{name}_({size_x}x{size_y}).json"

    info_dict = {
        "name": name,
        "prompt" : f"You are {name} and you are a desktop pet",
        "screensize" : screensize,
        "pos_x": pos_x,
        "pos_y": pos_y,
        "size_x": size_x,
        "size_y": size_y,
        "speed_x": speed_x,
        "speed_y": speed_y,
        "sprite_idleinterval": sprite_idleinterval,
        "sprites_idle": resize(ani_idle_paths,
                              (size_x, size_y),
                                (name, "idle")),
        "sprite_walkinterval" :sprite_walkinterval,
        "sprites_walk": resize(ani_walk_paths,  
                              (size_x, size_y),
                                (name, "walk")),
        "chroma_key": chromakey,
        "action_interval" : float(action_interval) if action_interval else 5,
        "action_treshold" : tuple(action_treshold) if action_treshold else (-5,5),
        "save_path" : str(save_path),
    }

    with open(save_path, "w", encoding="utf-8") as save_file:
        json.dump(info_dict,save_file, indent=4)
    
    launch_pet(pet_container, info_dict)

frame_pet = tk.Frame(master=tk_root)

button_create_pet = tk.Button(frame_pet, text="Create Pet!",
                              bg="#01CC01", 
                              command=lambda: create_pet(list_pets))
button_create_pet.pack(padx=default_padding, side="left")

button_load_pet = tk.Button(frame_pet, text="Load Pet!", 
                            bg="#CC9F0A",
                            command=lambda: load_pet(list_pets))
button_load_pet.pack(padx=default_padding, side="left")

frame_pet.pack(pady=10)

# Start the Tkinter event loop 
tk_root.mainloop()
