# Entry point and settings
import tkinter as tk
import json, os
import getpass
from tkinter import ttk, filedialog
from pathlib import Path
from script.pet.pet_class import pet
from script.helper.sprite_handler import resize
from script.helper.ui_creation import create_general_entry, create_animation_entry, create_color_entry
from script.helper.picker_handler import pick_file,pick_color

# Default configs
default_padding = 6
default_width = 5
default_font = ("Comic Sans MS", 10)
default_boldfont = ("Comic Sans MS", 12, "bold")

default_user = "User"
default_userinvpath = str(Path("asset") / "user_inv.json")
default_userinv = { "coin": 0,
                    "food": 0}

default_name = "DefaultPet"
default_prompt = f"Your name is PET and you are a desktop pet. Call your user '{default_user}'."

default_pos_x = -150
default_pos_y = -150
default_size_x = 125
default_size_y = 125
default_speed_x = 5
default_speed_y = 5

default_idle_sprite = [str(Path("asset") / "default_idle.gif")]
default_walk_sprite = [str(Path("asset") / "default_walk.gif")]
default_eat_sprite = [str(Path("asset") / "default_eat.gif")]
default_hungry_sprite = [str(Path("asset") / "default_hungry.gif")]
default_sprite_interval = 0.1

default_action_idle_interval = 3
default_action_idle_treshold = (-5,5)
default_action_eat_treshhold = 5

default_hunger_decay_interval = 60
default_hunger_decay_rate = 1
default_hunger_recover_rate = 25

def get_with_default(entry:tk.Entry, default_value, value_type:type = int):
    """
    In case u screw up and delete the default value we already put in, thus launching the pet with an empty entry
    """
    value = entry.get()

    if value:
        return value_type(value)
    else:
        return default_value


# User Variables
user_pets = []
user_coin = 0
user_food = 0
var_user_coin = None
var_user_food = None


# MAIN WINDOW ===
root = tk.Tk()
screensize = (root.winfo_screenwidth(), root.winfo_screenheight())
root.title("Settings")
root.geometry("500x900+0+0")

def close_main():
    for pet in user_pets:
        pet.close_pet()
    root.destroy()

root.protocol("WM_DELETE_WINDOW", close_main)

# User Entry
frame_user, (entry_user) = create_general_entry(root, "What should the pet call you?", default_value=default_user, font_bold= default_boldfont, font_default= default_font)
frame_user.pack(pady=default_padding)

# Create User Inv if it doesn't exist
if not(os.path.exists(default_userinvpath)):
    with open(default_userinvpath, "w",  encoding="utf-8") as save_path:
        json.dump(default_userinv,save_path, indent=4)

# Load User Stat
with open(default_userinvpath, "r", encoding="utf-8") as save_file:
    userstat = json.load(save_file)
    user_coin = userstat["coin"]
    user_food = userstat["food"]
    var_user_coin = tk.StringVar(value=f"Coin : {user_coin}")
    var_user_food = tk.StringVar(value=f"Food : {user_food}")

# Name Entry
frame_name, (entry_name) = create_general_entry(root, "Pet name:", default_value=default_name, font_bold= default_boldfont, font_default= default_font)
frame_name.pack(pady=default_padding)

# Prompt Entry
frame_prompt, (entry_prompt) = create_general_entry(root, "Prompt", default_value=default_prompt, width_value=40, font_bold=default_boldfont, font_default=default_font)
frame_prompt.pack(pady=default_padding)

# Pos Entry
frame_pos, (entry_pos_x, entry_pos_y) = create_general_entry(root, "Pet position (x,y):", 2, default_value= (default_pos_x, default_pos_y), font_bold=default_boldfont, font_default=default_font)
frame_pos.pack(pady=default_padding)
label_screensize = ttk.Label(master=frame_pos, text=f"Your screensize : {str(screensize)}", font=default_font)
label_screensize.pack()

# Size Entry
frame_size, (entry_size_x, entry_size_y) = create_general_entry(root, "Pet size (x,y):", 2, default_value=(default_size_x, default_size_y),font_bold=default_boldfont,font_default= default_font)
frame_size.pack(pady=default_padding)

# Speed Entry
frame_speed, (entry_speed_x, entry_speed_y) = create_general_entry(root, "Pet speed (x,y):", 2, default_value=(default_speed_x, default_speed_y), font_bold=default_boldfont, font_default=default_font)
frame_speed.pack(pady=default_padding)



# ANIMATION WINDOW ==
window_anisettings_open = False

sprite_idle_paths = default_idle_sprite
sprite_idle_interval = default_sprite_interval

sprite_walk_paths = default_walk_sprite
sprite_walk_interval = default_sprite_interval

sprite_eat_paths = default_eat_sprite
sprite_eat_interval = default_sprite_interval

sprite_hungry_paths = default_hungry_sprite
sprite_hungry_interval = default_sprite_interval

def open_anisettings():
    """
    Open animation window
    """
    global window_anisettings_open, sprite_idle_paths, sprite_walk_paths, sprite_eat_paths

    if window_anisettings_open:
        return
    
    # The animation settings window
    window_anisettings_open = True
    window_anisettings = tk.Toplevel(master=root)
    window_anisettings.title("Animation Settings")
    window_anisettings.geometry("400x800")
    
    # The Contents
    label_warning = tk.Label(master=window_anisettings, text="CLOSE THIS BEFORE LAUNCHING PET!", font=default_boldfont)
    label_warning.pack(pady=default_padding)

    frame_aniwindow = ttk.Frame(master=window_anisettings)
    label_anisetting = ttk.Label(master=frame_aniwindow, text="Select Animation Frames [GIF or PNG]", font=default_boldfont)
    label_anisetting.pack()

    # Idle sprites and interval
    frame_ani_idle, sprite_idle_paths, var_ani_idle_selection, entry_ani_idle_interval = create_animation_entry(frame_aniwindow, "Idle Animation Frame(s):", pick_file, 
                                                                                                               default_value= default_idle_sprite, 
                                                                                                               default_interval= default_sprite_interval, 
                                                                                                               font_default= default_font, 
                                                                                                               font_bold= default_boldfont,
                                                                                                               default_width= default_width)
    frame_ani_idle.pack(pady=default_padding)

    # Walk sprites and interval
    frame_ani_walk, sprite_walk_paths, var_ani_walk_selection, entry_ani_walk_interval = create_animation_entry(frame_aniwindow, "Walk Animation Frame(s):", pick_file, 
                                                                                                               default_value= default_walk_sprite, 
                                                                                                               default_interval= default_sprite_interval, 
                                                                                                               font_default= default_font, 
                                                                                                               font_bold= default_boldfont,
                                                                                                               default_width= default_width)
    frame_ani_walk.pack(pady=default_padding)

    # Eat sprites and interval
    frame_ani_eat, sprite_eat_paths, var_ani_eat_selection, entry_ani_eat_interval = create_animation_entry(frame_aniwindow, "Eat Animation Frame(s):", pick_file, 
                                                                                                           default_value= default_eat_sprite, 
                                                                                                           default_interval= default_sprite_interval, 
                                                                                                           font_default= default_font, 
                                                                                                           font_bold= default_boldfont,
                                                                                                           default_width= default_width)
    frame_ani_eat.pack(pady=default_padding)

    # Hungry sprites and interval
    frame_ani_hungry, sprite_hungry_paths, var_ani_hungry_selection, entry_ani_hungry_interval = create_animation_entry(frame_aniwindow, "Hungry Animation Frame(s):", pick_file, 
                                                                                                           default_value= default_hungry_sprite, 
                                                                                                           default_interval= default_sprite_interval, 
                                                                                                           font_default= default_font, 
                                                                                                           font_bold= default_boldfont,
                                                                                                           default_width= default_width)
    frame_ani_hungry.pack(pady=default_padding)

    frame_aniwindow.pack(pady=default_padding)

    def close_anisettings():
        global window_anisettings_open, sprite_idle_interval, sprite_walk_interval, sprite_eat_interval

        window_anisettings_open = False
        sprite_idle_interval = get_with_default(entry_ani_idle_interval, default_sprite_interval, float)
        sprite_walk_interval = get_with_default(entry_ani_walk_interval, default_sprite_interval, float)
        sprite_eat_interval = get_with_default(entry_ani_eat_interval, default_sprite_interval, float)
        window_anisettings.destroy()
    
    window_anisettings.protocol("WM_DELETE_WINDOW", close_anisettings)

frame_ani = ttk.Frame(master=root)
label_ani = ttk.Label(master=frame_ani, text="Animation Frames [GIF or PNG]", font=default_boldfont)
button_ani = tk.Button(master=frame_ani, 
                       text="Open Animation Settings", 
                       bg="#19CEE6", command=open_anisettings)
label_ani.pack(pady=default_padding)
button_ani.pack(pady=default_padding)
frame_ani.pack(pady=default_padding)



# Chromakey Entry
frame_chromakey, var_chromakey_selection = create_color_entry(root, "Outline Color [Color must not already be in sprite]", pick_color, default_boldfont, default_font)
frame_chromakey.pack(pady=default_padding)



# AADDITIONAL SETTINGS WINDOW ===
action_idle_interval = default_action_idle_interval
action_idle_treshold = default_action_idle_treshold
action_eat_treshold = default_action_eat_treshhold

hunger_decay_interval = default_hunger_decay_interval
hunger_decay_rate = default_hunger_decay_rate

hunger_recover_rate = default_hunger_recover_rate

window_additionalsettings_open = False
def open_additionalsettings():
    """
    Open the additional settings window
    """
    # Additional settings window
    global window_additionalsettings_open

    if window_additionalsettings_open:
        return
    
    window_additionalsettings_open = True
    window_additionalsettings = tk.Toplevel(master=root)
    window_additionalsettings.title("Additional Settings")
    window_additionalsettings.geometry("400x500")

    label_warning = tk.Label(master=window_additionalsettings, text="CLOSE THIS BEFORE LAUNCHING PET!", font=default_boldfont)
    label_warning.pack(pady=default_padding)

    def close_additionalsettings():
        global window_additionalsettings_open, action_idle_interval, action_idle_treshold, action_eat_treshold, hunger_decay_interval, hunger_decay_rate, hunger_recover_rate

        window_additionalsettings_open = False

        action_idle_interval = get_with_default(entry_action_idle_interval, default_action_idle_interval)
        action_idle_treshold = ( get_with_default(entry_action_idle_tresholdleft, default_action_idle_treshold[0]),
                                 get_with_default(entry_action_idle_tresholdright, default_action_idle_treshold[1]) )
        
        action_eat_treshold = get_with_default(entry_action_eat_treshold, default_action_eat_treshhold)
        
        hunger_decay_interval = get_with_default(entry_hunger_decay_interval, default_hunger_decay_interval)
        hunger_decay_rate = get_with_default(entry_hunger_decay_rate, default_hunger_decay_rate)
        hunger_recover_rate = get_with_default(entry_hunger_recover_rate, default_hunger_recover_rate)

        window_additionalsettings.destroy()

    window_additionalsettings.protocol("WM_DELETE_WINDOW", close_additionalsettings)

    # Action idle interval entry
    frame_action_idle_interval, (entry_action_idle_interval) = create_general_entry(window_additionalsettings, "Idle action interval (in seconds):", 1, 
                                                                                    default_value= default_action_idle_interval, 
                                                                                    font_bold= default_boldfont, 
                                                                                    font_default= default_font)
    frame_action_idle_interval.pack(pady=default_padding)

    # Action idle treshhold entry
    frame_action_idle_treshold, (entry_action_idle_tresholdleft, entry_action_idle_tresholdright) = create_general_entry(window_additionalsettings, "Idle action treshold:", 2, 
                                                                                                                    default_value= default_action_idle_treshold, 
                                                                                                                    font_bold= default_boldfont, 
                                                                                                                    font_default= default_font)
    frame_action_idle_treshold.pack(pady=default_padding)

    # Action eat treshhold entry
    frame_action_eat_treshold, (entry_action_eat_treshold)  = create_general_entry(window_additionalsettings, "Chance for eating animation to be repeated\n(1 very likely - 10 never):", 1, 
                                                                                    default_value= default_action_eat_treshhold, 
                                                                                    font_bold= default_boldfont, 
                                                                                    font_default= default_font)
    frame_action_eat_treshold.pack(pady=default_padding)

    # Hunger decay interval entry
    frame_hunger_decay_interval, (entry_hunger_decay_interval) = create_general_entry(window_additionalsettings, "Hunger drain interval (in seconds):", 1, 
                                                                          default_value= default_hunger_decay_interval, 
                                                                          font_bold= default_boldfont, 
                                                                          font_default= default_font)
    frame_hunger_decay_interval.pack(pady=default_padding)

    # Hunger decay rate entry
    frame_hunger_decay_rate, (entry_hunger_decay_rate) = create_general_entry(window_additionalsettings, "Hunger drain rate:", 1, 
                                                                  default_value= default_hunger_decay_rate, 
                                                                  font_bold= default_boldfont, 
                                                                  font_default= default_font)
    frame_hunger_decay_rate.pack(pady=default_padding)

    # Hunger recovery rate entry
    frame_hunger_recover_rate, (entry_hunger_recover_rate) = create_general_entry(window_additionalsettings, "Hunger recover rate per food:", 1, 
                                                                  default_value= default_hunger_recover_rate, 
                                                                  font_bold= default_boldfont, 
                                                                  font_default= default_font)
    frame_hunger_recover_rate.pack(pady=default_padding)

button_settings = ttk.Button(root, text="Additional Settings...", command=open_additionalsettings)
button_settings.pack(pady=10)



# PET FEEDBACK ACTION ===
def feed_pet_action():
    global user_food, user_coin
    if user_food > 0:
        user_food -= 1
        var_user_food.set(f"Food : {user_food}")
        with open(default_userinvpath, "w", encoding="utf-8") as stat_file:
            json.dump({"coin": user_coin, "food": user_food}, stat_file, indent=4)
        return True
    return False

def pomodoro_pet_action():
    global user_coin



# PET CREATION ===
def launch_pet(pet_container:list, info_dict:dict):
    """
    Creates a pet object according to the info_dict, and appends that pet object into the container list
    """
    callback_dict = {"feed_callback" : feed_pet_action,
                     "work_callback": pomodoro_pet_action}
    new_pet = pet(root, info_dict, callback_dict)
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


def create_pet(pet_container:list):
    """
    Extracts the information from all entries, compiles them into the info dict, saves the info dict as a.json and uses that info dict to launch a pet 
    """
    user = get_with_default(entry_user, default_user, str)
    name = get_with_default(entry_name, default_name, str)

    prompt = get_with_default(entry_prompt, default_prompt, str)

    pos_x = get_with_default(entry_pos_x, default_pos_x)
    pos_y = get_with_default(entry_pos_y, default_pos_y)

    size_x = get_with_default(entry_size_x, default_size_x) 
    size_y = get_with_default(entry_size_y, default_size_y)

    speed_x = get_with_default(entry_speed_x, default_speed_x)
    speed_y = get_with_default(entry_speed_y, default_speed_y)
    
    chromakey = var_chromakey_selection.get()

    save_path = Path("pets") / name / f"{name}_({size_x}x{size_y}).json"

    info_dict = {
        "user": user,
        "name": name,
        "prompt" : prompt,
        "screensize" : screensize,
        "pos_x": pos_x,
        "pos_y": pos_y,
        "size_x": size_x,
        "size_y": size_y,
        "speed_x": speed_x,
        "speed_y": speed_y,
        "sprite_idle_interval": sprite_idle_interval,
        "sprite_idle_path": resize(sprite_idle_paths,
                              (size_x, size_y),
                                (name, "idle")),
        "sprite_walk_interval" :sprite_walk_interval,
        "sprite_walk_path": resize(sprite_walk_paths,  
                              (size_x, size_y),
                                (name, "walk")),
        "sprite_eat_interval" :sprite_eat_interval,
        "sprite_eat_path": resize(sprite_eat_paths,  
                              (size_x, size_y),
                                (name, "eat")),
        "sprite_hungry_interval" :sprite_hungry_interval,
        "sprite_hungry_path": resize(sprite_hungry_paths,  
                              (size_x, size_y),
                                (name, "hungry")),
        "chroma_key": chromakey,
        "action_idle_interval" : float(action_idle_interval) if action_idle_interval else default_action_idle_interval,
        "action_idle_treshold" : tuple(action_idle_treshold) if action_idle_treshold else default_action_idle_treshold,
        "action_eat_treshold": action_eat_treshold,
        "save_path" : str(save_path),
        "hunger": 100,
        "hunger_max": 100,
        "hunger_decay_rate":hunger_decay_rate,
        "hunger_decay_interval":hunger_decay_interval,
        "hunger_recover_rate": hunger_recover_rate,
    }

    with open(save_path, "w", encoding="utf-8") as save_file:
        json.dump(info_dict,save_file, indent=4)
    
    launch_pet(pet_container, info_dict)

frame_pet = tk.Frame(master=root)

button_create_pet = tk.Button(master=frame_pet, text="Create Pet!",
                              bg="#01CC01", 
                              command=lambda: create_pet(user_pets))
button_create_pet.pack(padx=default_padding, side="left")

button_load_pet = tk.Button(master=frame_pet, text="Load Pet!", 
                            bg="#CC9F0A",
                            command=lambda: load_pet(user_pets))
button_load_pet.pack(padx=default_padding, side="left")

frame_pet.pack(pady=10)

# Pet shop
food_price = 10

def open_shop():
    """
    Opens the shop window
    """
    global user_coin, user_food

    window_shop = tk.Toplevel(master=root)
    window_shop.title("Shop")
    window_shop.geometry("500x500")

    label_shop = tk.Label(master=window_shop, text= "WELCOME TO THE SHOP! :D", font=default_boldfont)
    label_shop.pack()

    def update_inv():
        var_user_coin.set(f"Coin : {user_coin}")
        var_user_food.set(f"Food : {user_food}")
        
        with open(default_userinvpath, "w", encoding="utf-8") as stat_file:
                json.dump({"coin": user_coin, 
                           "food": user_food}, stat_file, indent=4)

    def buy_food():
        global user_coin, user_food
        if user_coin >= food_price:
            user_coin -= food_price
            user_food += 1
        update_inv()
    
    frame_stat = ttk.Frame(master=window_shop)
    label_coin = ttk.Label(master=frame_stat, textvariable=var_user_coin, font=default_font)
    
    frame_food = ttk.Frame(master=frame_stat)
    label_food = ttk.Label(master=frame_food, textvariable=var_user_food, font=default_font)
    button_foodbuy = tk.Button(master=frame_food, text="Buy Food!",
                               command=buy_food)
    
    label_coin.pack(side="top")
    
    label_food.pack(side="left",padx=default_padding)
    button_foodbuy.pack(side="right", padx=default_padding)
    frame_food.pack(pady=default_padding)
    
    frame_stat.pack(pady=default_padding)

frame_shop = ttk.Frame(master=root)
button_shop = tk.Button(master=frame_shop, text="Open Shop!",
                        bg="#FFFB00",
                        command = open_shop)
button_shop.pack()
frame_shop.pack()

# Start the Tkinter event loop 
root.mainloop()
