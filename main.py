# Entry point and settings
import tkinter as tk
import json, os
import getpass
from tkinter import ttk, filedialog
from pathlib import Path
from script.pet.pet_class import pet
from script.helper.sprite_handler import resize
from script.helper.menu_ui import create_general_entry, create_animation_entry, create_color_entry
from script.helper.picker_handler import pick_file,pick_color

# UI Constant ===
PADDING = 6
WIDTH = 5
FONT_DEFALT = ("Comic Sans MS", 10)
FONT_BOLD = ("Comic Sans MS", 12, "bold")

# Default Configs ===
USER_NAME = "User"
USER_INVPATH = str(Path("asset") / "user_inv.json")
USER_INV = { "coin": 10,
             "food": 5}

NAME = "Whiskerton"
PROMPT = f"You are a cute cat desktop pet talking to the user."

SPAWN_X = -150
SPAWN_Y = -150

SIZE_X = 125
SIZE_Y = 125

SPEED_X = 5
SPEED_Y = 5

IDLE_SPRITE = [str(Path("asset") / "default_idle.gif")]
WALK_SPRITE = [str(Path("asset") / "default_walk.gif")]
EAT_SPRITE = [str(Path("asset") / "default_eat.gif")]
HUNGRY_SPRITE = [str(Path("asset") / "default_hungry.gif")]
PET_SPRITE = [str(Path("asset") / "default_pet.gif")]
WORK_SPRITE = [str(Path("asset") / "default_work.gif")]
SIT_SPRITE = [str(Path("asset") / "default_sit.gif")]
THINK_SPRITE = [str(Path("asset") / "default_think.gif")]
SPRITE_INTERVAL = 0.1

WANDER_INTERVAL = 3
WANDER_TRESHOLD = (-5,5)
EATLOOP_TRESHOLD = 5
PETLOOP_TRESHOLD = 3

HUNGER_DECAY_INTERVAL = 180 
HUNGER_DECAY_RATE = 1
HUNGER_RECOVER_RATE = 25

def get_convert(entry:tk.Entry, default_value, value_type:type = int):
    """
    Easily convert from strings to int or other values from entries
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
root.config(padx=20, pady=20)

def close_main():
    for pet in user_pets:
        pet.close_pet()
    root.destroy()

root.protocol("WM_DELETE_WINDOW", close_main)

# User Entry
frame_user, (entry_user) = create_general_entry(
    root, 
    "What should the pet call you?", 
    default_value=USER_NAME, 
    font_bold= FONT_BOLD, 
    font_default= FONT_DEFALT)
frame_user.pack(pady=PADDING)

# Create User Inv if it doesn't exist
if not(os.path.exists(USER_INVPATH)):
    with open(USER_INVPATH, "w",  encoding="utf-8") as save_path:
        json.dump(USER_INV,save_path, indent=4)

# Load User Stat
with open(USER_INVPATH, "r", encoding="utf-8") as save_file:
    userstat = json.load(save_file)
    user_coin = userstat["coin"]
    user_food = userstat["food"]
    var_user_coin = tk.StringVar(value=f"Coin : {user_coin}")
    var_user_food = tk.StringVar(value=f"Food : {user_food}")

# Name Entry
frame_name, (entry_name) = create_general_entry(
    root, 
    "Pet name:", 
    default_value=NAME, 
    font_bold= FONT_BOLD, 
    font_default= FONT_DEFALT)
frame_name.pack(pady=PADDING)

# Prompt Entry
frame_prompt, (entry_prompt) = create_general_entry(
    root, "Prompt", 
    default_value=PROMPT,
    width_value=40, 
    font_bold=FONT_BOLD, 
    font_default=FONT_DEFALT)
frame_prompt.pack(pady=PADDING)

# Pos Entry
frame_pos, (entry_spawn_x, entry_spawn_y) = create_general_entry(
    root, 
    "Pet position (x,y):", 
    num_entries=2, 
    
    default_value= (SPAWN_X, SPAWN_Y), 
    font_bold=FONT_BOLD, 
    font_default=FONT_DEFALT)
frame_pos.pack(pady=PADDING)
label_screensize = ttk.Label(master=frame_pos, text=f"Your screensize : {str(screensize)}", font=FONT_DEFALT)
label_screensize.pack()

# Size Entry
frame_size, (entry_size_x, entry_size_y) = create_general_entry(
    root, 
    "Pet size (x,y):", 
    num_entries=2, 
    default_value=(SIZE_X, SIZE_Y),
    font_bold=FONT_BOLD,
    font_default= FONT_DEFALT)
frame_size.pack(pady=PADDING)

# Speed Entry
frame_speed, (entry_speed_x, entry_speed_y) = create_general_entry(
    root, 
    "Pet speed (x,y):", 
    num_entries=2, 
    default_value=(SPEED_X, SPEED_Y), 
    font_bold=FONT_BOLD, 
    font_default=FONT_DEFALT)
frame_speed.pack(pady=PADDING)


# ANIMATION WINDOW ==
sprite_setting = {
    "settings_open" : False,
    "idle": [IDLE_SPRITE, SPRITE_INTERVAL],
    "walk": [WALK_SPRITE, SPRITE_INTERVAL],
    "eat": [EAT_SPRITE, SPRITE_INTERVAL],
    "hungry": [HUNGRY_SPRITE, SPRITE_INTERVAL],
    "pet": [PET_SPRITE, SPRITE_INTERVAL],
    "work": [WORK_SPRITE, SPRITE_INTERVAL],
    "sit": [SIT_SPRITE, SPRITE_INTERVAL],
    "think": [THINK_SPRITE, SPRITE_INTERVAL],
}

def open_anisettings():
    """
    Open animation window
    """
    if sprite_setting["settings_open"]:
        return
    
    # The animation settings window
    sprite_setting["settings_open"] = True
    window_anisettings = tk.Toplevel(master=root, padx=10, pady=10)
    window_anisettings.title("Animation Settings")

    # Idle sprites and interval
    frame_ani_idle, sprite_setting["idle"][0], entry_ani_idle_interval = create_animation_entry(
        window_anisettings, 
        "Idle Animation Frame(s):", 
        pick_file, 
        default_value= IDLE_SPRITE, 
        default_interval= SPRITE_INTERVAL, 
        font_default= FONT_DEFALT, 
        font_bold= FONT_BOLD,
        default_width= WIDTH)
    frame_ani_idle.grid(column=0, row=0)

    # Walk sprites and interval
    frame_ani_walk, sprite_setting["walk"][0], entry_ani_walk_interval = create_animation_entry(
        window_anisettings,
        "Walk Animation Frame(s):",
        pick_file, 
        default_value= WALK_SPRITE, 
        default_interval= SPRITE_INTERVAL, 
        font_default= FONT_DEFALT, 
        font_bold= FONT_BOLD,
        default_width= WIDTH)
    frame_ani_walk.grid(column=1, row=0)

    # Eat sprites and interval
    frame_ani_eat, sprite_setting["eat"][0], entry_ani_eat_interval = create_animation_entry(
        window_anisettings, 
        "Eat Animation Frame(s):", 
        pick_file, 
        default_value= EAT_SPRITE, 
        default_interval= SPRITE_INTERVAL, 
        font_default= FONT_DEFALT, 
        font_bold= FONT_BOLD,
        default_width=WIDTH)
    frame_ani_eat.grid(column=0, row=1)

    # Hungry sprites and interval
    frame_ani_hungry, sprite_setting["hungry"][0], entry_ani_hungry_interval = create_animation_entry(
        window_anisettings, 
        "Hungry Animation Frame(s):", 
        pick_file, 
        default_value= HUNGRY_SPRITE, 
        default_interval= SPRITE_INTERVAL, 
        font_default= FONT_DEFALT, 
        font_bold= FONT_BOLD,
        default_width=WIDTH)
    frame_ani_hungry.grid(column=1, row=1)

    # Pet sprites and interval
    frame_ani_pet, sprite_setting["pet"][0], entry_ani_pet_interval = create_animation_entry(
        window_anisettings, 
        "Pet / Play Animation Frame(s):", 
        pick_file, 
        default_value= PET_SPRITE, 
        default_interval= SPRITE_INTERVAL, 
        font_default= FONT_DEFALT, 
        font_bold= FONT_BOLD,
        default_width=WIDTH)
    frame_ani_pet.grid(column=0, row=2)

    # Work sprites and interval
    frame_ani_work, sprite_setting["work"][0], entry_ani_work_interval = create_animation_entry(
        window_anisettings,
        "Work Animation Frame(s):", 
        pick_file, 
        default_value= WORK_SPRITE, 
        default_interval= SPRITE_INTERVAL, 
        font_default= FONT_DEFALT, 
        font_bold= FONT_BOLD,
        default_width=WIDTH)
    frame_ani_work.grid(column=1, row=2)
    
    # Sit sprites and interval
    frame_ani_sit, sprite_setting["sit"][0], entry_ani_sit_interval = create_animation_entry(
        window_anisettings,
        "Sit Animation Frame(s):",
        pick_file, 
        default_value= SIT_SPRITE, 
        default_interval= SPRITE_INTERVAL, 
        font_default= FONT_DEFALT, 
        font_bold= FONT_BOLD,
        default_width=WIDTH)
    frame_ani_sit.grid(column=0, row=3)
    
    # Think sprites and interval
    frame_ani_sit, sprite_setting["think"][0], entry_ani_think_interval = create_animation_entry(
        window_anisettings, 
        "Think Animation Frame(s):", 
        pick_file, 
        default_value= THINK_SPRITE, 
        default_interval= SPRITE_INTERVAL, 
        font_default= FONT_DEFALT, 
        font_bold= FONT_BOLD,
        default_width=WIDTH)
    frame_ani_sit.grid(column=0, row=3)

    def close_anisettings():

        sprite_setting["settings_open"] = False
        
        sprite_setting["idle"][1] = get_convert(entry_ani_idle_interval, SPRITE_INTERVAL, float)
        sprite_setting["walk"][1] = get_convert(entry_ani_walk_interval, SPRITE_INTERVAL, float)
        sprite_setting["eat"][1] = get_convert(entry_ani_eat_interval, SPRITE_INTERVAL, float)
        sprite_setting["hungry"][1] = get_convert(entry_ani_hungry_interval, SPRITE_INTERVAL, float)
        sprite_setting["pet"][1] = get_convert(entry_ani_pet_interval, SPRITE_INTERVAL, float)
        sprite_setting["work"][1] = get_convert(entry_ani_work_interval, SPRITE_INTERVAL, float)
        sprite_setting["sit"][1] = get_convert(entry_ani_sit_interval, SPRITE_INTERVAL, float)
        sprite_setting["think"][1] = get_convert(entry_ani_think_interval, SPRITE_INTERVAL, float)

        window_anisettings.destroy()
    
    # Closing the window
    button_close = tk.Button(window_anisettings, text="Save & close", 
                                command=close_anisettings)
    button_close.grid(column=0,row=4)
    window_anisettings.protocol("WM_DELETE_WINDOW", close_anisettings)


frame_ani = ttk.Frame(master=root)
label_ani = ttk.Label(
    master=frame_ani, 
    text="Animation Frames [GIF or PNG]", 
    font=FONT_BOLD)
label_ani.pack(pady=PADDING)
button_ani = tk.Button(
    master=frame_ani,            
    text="Open Animation Settings", 
    bg="#19CEE6", command=open_anisettings)
button_ani.pack(pady=PADDING)
frame_ani.pack(pady=PADDING)


# Chromakey Entry
frame_chromakey, var_chromakey_selection = create_color_entry(root, "Chormakey Color", pick_color, FONT_BOLD, FONT_DEFALT)
frame_chromakey.pack(pady=PADDING)


# AADDITIONAL SETTINGS WINDOW ===
additional_settings = {
    "settings_open" : False,
    "wander_interval" : WANDER_INTERVAL,
    "wander_treshold" : WANDER_TRESHOLD,
    
    "eatloop_treshold" : EATLOOP_TRESHOLD,
    
    "petloop_treshold" : PETLOOP_TRESHOLD,
    
    "hunger_decay_interval" : HUNGER_DECAY_INTERVAL,
    "hunger_decay_rate" : HUNGER_DECAY_RATE,
    "hunger_recover_rate" : HUNGER_RECOVER_RATE
}

def open_additionalsettings():
    """
    Open the additional settings window
    """
    # Additional settings window

    if additional_settings["settings_open"]:
        return
    
    additional_settings["settings_open"] = True
    window_additionalsettings = tk.Toplevel(master=root, padx=10, pady=10)
    window_additionalsettings.title("Additional Settings")

    # Action idle interval entry
    frame_wander_interval, (entry_wander_interval) = create_general_entry(
        window_additionalsettings, 
        "Idle action interval (in seconds):", 
        default_value= WANDER_INTERVAL, 
        font_bold= FONT_BOLD, 
        font_default= FONT_DEFALT)
    frame_wander_interval.pack(pady=PADDING)

    # Action idle treshhold entry
    frame_action_idle_treshold, (entry_wander_tresholdleft, entry_wander_tresholdright) = create_general_entry(
        window_additionalsettings, 
        "Idle action treshold:", 
        num_entries=2, 
        default_value= WANDER_TRESHOLD, 
        font_bold= FONT_BOLD, 
        font_default= FONT_DEFALT)
    frame_action_idle_treshold.pack(pady=PADDING)

    # Action eat treshhold entry
    frame_action_eat_treshold, (entry_eatloop_treshold)  = create_general_entry(
        window_additionalsettings, 
        "Chance for eating animation to be loop\n(1 very likely - 10 never):", 
        default_value= EATLOOP_TRESHOLD, 
        font_bold= FONT_BOLD, 
        font_default= FONT_DEFALT)
    frame_action_eat_treshold.pack(pady=PADDING)

    # Action pet treshhold entry
    frame_action_pet_treshold, (entry_petloop_treshold)  = create_general_entry(
        window_additionalsettings,
        "Chance for petting animation to be loop\n(1 very likely - 10 never):", 
        default_value= PETLOOP_TRESHOLD, 
        font_bold= FONT_BOLD, 
        font_default= FONT_DEFALT)
    frame_action_pet_treshold.pack(pady=PADDING)

    # Hunger decay interval entry
    frame_hunger_decay_interval, (entry_hunger_decay_interval) = create_general_entry(
        window_additionalsettings,
        "Hunger drain interval (in seconds):", 
        default_value= HUNGER_DECAY_INTERVAL, 
        font_bold= FONT_BOLD, 
        font_default= FONT_DEFALT)
    frame_hunger_decay_interval.pack(pady=PADDING)

    # Hunger decay rate entry
    frame_hunger_decay_rate, (entry_hunger_decay_rate) = create_general_entry(
        window_additionalsettings, 
        "Hunger drain rate:",
        default_value= HUNGER_DECAY_RATE, 
        font_bold= FONT_BOLD, 
        font_default= FONT_DEFALT)
    frame_hunger_decay_rate.pack(pady=PADDING)

    # Hunger recovery rate entry
    frame_hunger_recover_rate, (entry_hunger_recover_rate) = create_general_entry(
        window_additionalsettings, 
        "Hunger recover rate per food:", 
        default_value= HUNGER_RECOVER_RATE, 
        font_bold= FONT_BOLD, 
        font_default= FONT_DEFALT)
    frame_hunger_recover_rate.pack(pady=PADDING)

    def close_additionalsettings():

        additional_settings["settings_open"] = False

        additional_settings["wander_interval"] = get_convert(entry_wander_interval, WANDER_INTERVAL)
        additional_settings["wander_treshold"] = (get_convert(entry_wander_tresholdleft, WANDER_TRESHOLD[0]),
                                                  get_convert(entry_wander_tresholdright, WANDER_TRESHOLD[1]) )
        
        additional_settings["eatloop_treshold"] = get_convert(entry_eatloop_treshold, EATLOOP_TRESHOLD)
        additional_settings["petloop_treshold"] = get_convert(entry_petloop_treshold, PETLOOP_TRESHOLD)
        
        additional_settings["hunger_decay_interval"] = get_convert(entry_hunger_decay_interval, HUNGER_DECAY_INTERVAL)
        additional_settings["hunger_decay_rate"] = get_convert(entry_hunger_decay_rate, HUNGER_DECAY_RATE)
        additional_settings["hunger_recover_rate"] = get_convert(entry_hunger_recover_rate, HUNGER_RECOVER_RATE)

        window_additionalsettings.destroy()

    # Close and save
    button_close = tk.Button(window_additionalsettings, text="Save & close", 
                                command=close_additionalsettings)
    button_close.pack()
    window_additionalsettings.protocol("WM_DELETE_WINDOW", close_additionalsettings)

button_settings = ttk.Button(root, text="Additional Settings...", command=open_additionalsettings)
button_settings.pack(pady=10)


# PET FEEDBACK ACTION ===
def feed_pet_action():
    global user_food, user_coin
    if user_food > 0:
        user_food -= 1
        var_user_food.set(f"Food : {user_food}")
        with open(USER_INVPATH, "w", encoding="utf-8") as stat_file:
            json.dump({"coin": user_coin, "food": user_food}, stat_file, indent=4)
        return True
    return False

def pomodoro_pet_action(coin_amount):
    global user_coin
    user_coin += coin_amount
    var_user_coin.set(f"Coin : {user_coin}")
    with open(USER_INVPATH, "w", encoding="utf-8") as stat_file:
            json.dump({"coin": user_coin, 
                       "food": user_food}, stat_file, indent=4)



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
    user = get_convert(entry_user, USER_NAME, str)
    name = get_convert(entry_name, NAME, str)

    prompt = get_convert(entry_prompt, PROMPT, str)

    spawn_x = get_convert(entry_spawn_x, SPAWN_X)
    spawn_y = get_convert(entry_spawn_y, SPAWN_Y)

    size_x = get_convert(entry_size_x, SIZE_X) 
    size_y = get_convert(entry_size_y, SIZE_Y)

    speed_x = get_convert(entry_speed_x, SPEED_X)
    speed_y = get_convert(entry_speed_y, SPEED_Y)
    
    chromakey = var_chromakey_selection.get()

    save_path = Path("pets") / name / f"{name}_({size_x}x{size_y}).json"

    info_dict = {
        "user": user,
        "name": name,
        "prompt" : f"{prompt} Your name is '{name}'. Call your user '{user}'. Respond briefly",
        
        "screensize" : screensize,
        "spawn_x": spawn_x,
        "spawn_y": spawn_y,
        "size_x": size_x,
        "size_y": size_y,
        
        "speed_x": speed_x,
        "speed_y": speed_y,
        
        "sprite_idle_interval": sprite_setting["idle"][1],
        "sprite_idle_path": resize(sprite_setting["idle"][0],
                              (size_x, size_y),
                                (name, "idle")),
        
        "sprite_walk_interval" :sprite_setting["walk"][1],
        "sprite_walk_path": resize(sprite_setting["walk"][0],  
                              (size_x, size_y),
                                (name, "walk")),
        
        "sprite_eat_interval" :sprite_setting["eat"][1],
        "sprite_eat_path": resize(sprite_setting["eat"][0],  
                              (size_x, size_y),
                                (name, "eat")),
        
        "sprite_hungry_interval" :sprite_setting["hungry"][1],
        "sprite_hungry_path": resize(sprite_setting["hungry"][0],  
                              (size_x, size_y),
                                (name, "hungry")),
        
        "sprite_pet_interval" :sprite_setting["pet"][1],
        "sprite_pet_path": resize(sprite_setting["pet"][0],  
                              (size_x, size_y),
                                (name, "pet")),
        
        "sprite_work_interval" :sprite_setting["work"][1],
        "sprite_work_path": resize(sprite_setting["work"][0],  
                              (size_x, size_y),
                                (name, "work")),
        
        "sprite_sit_interval" :sprite_setting["sit"][1],
        "sprite_sit_path": resize(sprite_setting["sit"][0],  
                              (size_x, size_y),
                                (name, "sit")),
        
        "sprite_think_interval" :sprite_setting["think"][1],
        "sprite_think_path": resize(sprite_setting["think"][0],  
                              (size_x, size_y),
                                (name, "think")),
        
        "chroma_key": chromakey,
        
        "wander_interval" : additional_settings["wander_interval"],
        "wander_treshold" : additional_settings["wander_treshold"],
        
        "eatloop_treshold": additional_settings["eatloop_treshold"],
        "petloop_treshold": additional_settings["petloop_treshold"],
        
        "save_path" : str(save_path),
        
        "hunger": 100,
        "hunger_max": 100,
        "hunger_decay_rate": additional_settings["hunger_decay_rate"],
        "hunger_decay_interval":additional_settings["hunger_decay_interval"],
        "hunger_recover_rate": additional_settings["hunger_recover_rate"],
    }

    with open(save_path, "w", encoding="utf-8") as save_file:
        json.dump(info_dict,save_file, indent=4)
    
    launch_pet(pet_container, info_dict)

frame_pet = tk.Frame(master=root)

button_create_pet = tk.Button(master=frame_pet, text="Create Pet!",
                              bg="#01CC01", 
                              command=lambda: create_pet(user_pets))
button_create_pet.pack(padx=PADDING, side="left")

button_load_pet = tk.Button(master=frame_pet, text="Load Pet!", 
                            bg="#CC9F0A",
                            command=lambda: load_pet(user_pets))
button_load_pet.pack(padx=PADDING, side="left")

frame_pet.pack(pady=10)

# TO DO: MAKE THIS A DIFFERENT CLASS!
# Pet shop ===
food_price = 10

def open_shop():
    """
    Opens the shop window
    """
    global user_coin, user_food

    window_shop = tk.Toplevel(master=root)
    window_shop.title("Shop")
    window_shop.config(
        padx=20, 
        pady=20, 
        bg="#f7f5dd")

    label_shop = tk.Label(
        master=window_shop, 
        text= "WELCOME TO THE SHOP! :D", 
        font=FONT_BOLD,
        background="#f7f5dd")
    label_shop.pack()

    def update_inv():
        var_user_coin.set(f"Coin : {user_coin}")
        var_user_food.set(f"Food : {user_food}")
        
        with open(USER_INVPATH, "w", encoding="utf-8") as stat_file:
                json.dump({"coin": user_coin, 
                           "food": user_food}, stat_file, indent=4)

    def buy_food():
        global user_coin, user_food
        if user_coin >= food_price:
            user_coin -= food_price
            user_food += 1
        update_inv()
    
    frame_stat = ttk.Frame(
        master=window_shop,)
    frame_stat.pack(pady=PADDING)
    
    label_coin = ttk.Label(
        master=frame_stat, 
        textvariable=var_user_coin, 
        font=FONT_DEFALT,
        background="#FFFB00")
    label_coin.pack(side="top")
    
    frame_food = ttk.Frame(
        master=window_shop)
    frame_food.pack(pady=PADDING)
    
    label_food = ttk.Label(
        master=frame_food, 
        textvariable=var_user_food, 
        font=FONT_DEFALT,
        background="#ffbd91")
    label_food.pack(side="left",padx=PADDING)
    
    button_foodbuy = tk.Button(
        master=frame_food, 
        text="Buy Food!",
        command=buy_food,
        bg="#fdff91")
    button_foodbuy.pack(side="right", padx=PADDING)
    
    frame_powerup = ttk.Frame(
        master=window_shop)
    frame_powerup.pack(pady=PADDING)
    
    label_comingSoon = ttk.Label(
        master=frame_powerup, 
        text="More coming soon ~",
        font=FONT_DEFALT,
        background="#ffd991")
    label_comingSoon.pack(padx=PADDING)
    

frame_shop = ttk.Frame(master=root)
button_shop = tk.Button(master=frame_shop, text="Open Shop!",
                        bg="#FFFB00",
                        command = open_shop)
button_shop.pack()
frame_shop.pack()

# Start the Tkinter event loop 
root.mainloop()
