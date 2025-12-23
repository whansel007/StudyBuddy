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

# UI Constant ===
PADDING = 6
WIDTH = 5
FONT_DEFALT = ("Comic Sans MS", 10)
FONT_BOLD = ("Comic Sans MS", 12, "bold")

# Default Configs ===
USER_NAME = "User"
USER_INVPATH = str(Path("asset") / "user_inv.json")
USER_INV = { "coin": 0,
             "food": 0}

NAME = "DefaultPet"
PROMPT = f"Your name is PET and you are a desktop pet. Call your user '{USER_NAME}'."

POS_X = -150
POS_Y = -150

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
SPRITE_INTERVAL = 0.1

ACTION_IDLE_INTERVAL = 3
ACTION_IDLE_TRESHOLD = (-5,5)
ACTION_EAT_TRESHOLD = 5
ACTION_PET_TRESHOLD = 3

HUNGER_DECAY_INTERVAL = 60
HUNGER_DECAY_RATE = 1
HUNGER_RECOVER_RATE = 25

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
root.config(padx=20, pady=20)

def close_main():
    for pet in user_pets:
        pet.close_pet()
    root.destroy()

root.protocol("WM_DELETE_WINDOW", close_main)

# User Entry
frame_user, (entry_user) = create_general_entry(root, "What should the pet call you?", default_value=USER_NAME, font_bold= FONT_BOLD, font_default= FONT_DEFALT)
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
frame_name, (entry_name) = create_general_entry(root, "Pet name:", default_value=NAME, font_bold= FONT_BOLD, font_default= FONT_DEFALT)
frame_name.pack(pady=PADDING)

# Prompt Entry
frame_prompt, (entry_prompt) = create_general_entry(root, "Prompt", default_value=PROMPT, width_value=40, font_bold=FONT_BOLD, font_default=FONT_DEFALT)
frame_prompt.pack(pady=PADDING)

# Pos Entry
frame_pos, (entry_pos_x, entry_pos_y) = create_general_entry(root, "Pet position (x,y):", 2, default_value= (POS_X, POS_Y), font_bold=FONT_BOLD, font_default=FONT_DEFALT)
frame_pos.pack(pady=PADDING)
label_screensize = ttk.Label(master=frame_pos, text=f"Your screensize : {str(screensize)}", font=FONT_DEFALT)
label_screensize.pack()

# Size Entry
frame_size, (entry_size_x, entry_size_y) = create_general_entry(root, "Pet size (x,y):", 2, default_value=(SIZE_X, SIZE_Y),font_bold=FONT_BOLD,font_default= FONT_DEFALT)
frame_size.pack(pady=PADDING)

# Speed Entry
frame_speed, (entry_speed_x, entry_speed_y) = create_general_entry(root, "Pet speed (x,y):", 2, default_value=(SPEED_X, SPEED_Y), font_bold=FONT_BOLD, font_default=FONT_DEFALT)
frame_speed.pack(pady=PADDING)



# ANIMATION WINDOW ==
window_anisettings_open = False

sprite_idle_paths = IDLE_SPRITE
sprite_idle_interval = SPRITE_INTERVAL

sprite_walk_paths = WALK_SPRITE
sprite_walk_interval = SPRITE_INTERVAL

sprite_eat_paths = EAT_SPRITE
sprite_eat_interval = SPRITE_INTERVAL

sprite_hungry_paths = HUNGRY_SPRITE
sprite_hungry_interval = SPRITE_INTERVAL

sprite_pet_paths = PET_SPRITE
sprite_pet_interval = SPRITE_INTERVAL

sprite_work_paths = WORK_SPRITE
sprite_work_interval = SPRITE_INTERVAL

def open_anisettings():
    """
    Open animation window
    """
    global window_anisettings_open, sprite_idle_paths, sprite_walk_paths, sprite_eat_paths, sprite_hungry_paths, sprite_pet_paths, sprite_work_paths

    if window_anisettings_open:
        return
    
    # The animation settings window
    window_anisettings_open = True
    window_anisettings = tk.Toplevel(master=root, padx=10, pady=10)
    window_anisettings.title("Animation Settings")

    # Idle sprites and interval
    frame_ani_idle, sprite_idle_paths, entry_ani_idle_interval = create_animation_entry(window_anisettings, "Idle Animation Frame(s):", pick_file, 
                                                                                                               default_value= IDLE_SPRITE, 
                                                                                                               default_interval= SPRITE_INTERVAL, 
                                                                                                               font_default= FONT_DEFALT, 
                                                                                                               font_bold= FONT_BOLD,
                                                                                                               default_width= WIDTH)
    frame_ani_idle.pack()

    # Walk sprites and interval
    frame_ani_walk, sprite_walk_paths, entry_ani_walk_interval = create_animation_entry(window_anisettings, "Walk Animation Frame(s):", pick_file, 
                                                                                                               default_value= WALK_SPRITE, 
                                                                                                               default_interval= SPRITE_INTERVAL, 
                                                                                                               font_default= FONT_DEFALT, 
                                                                                                               font_bold= FONT_BOLD,
                                                                                                               default_width= WIDTH)
    frame_ani_walk.pack(pady=PADDING)

    # Eat sprites and interval
    frame_ani_eat, sprite_eat_paths, entry_ani_eat_interval = create_animation_entry(window_anisettings, "Eat Animation Frame(s):", pick_file, 
                                                                                                           default_value= EAT_SPRITE, 
                                                                                                           default_interval= SPRITE_INTERVAL, 
                                                                                                           font_default= FONT_DEFALT, 
                                                                                                           font_bold= FONT_BOLD,
                                                                                                           default_width=WIDTH)
    frame_ani_eat.pack(pady=PADDING)

    # Hungry sprites and interval
    frame_ani_hungry, sprite_hungry_paths, entry_ani_hungry_interval = create_animation_entry(window_anisettings, "Hungry Animation Frame(s):", pick_file, 
                                                                                                           default_value= HUNGRY_SPRITE, 
                                                                                                           default_interval= SPRITE_INTERVAL, 
                                                                                                           font_default= FONT_DEFALT, 
                                                                                                           font_bold= FONT_BOLD,
                                                                                                           default_width=WIDTH)
    frame_ani_hungry.pack(pady=PADDING)

    # Play sprites and interval
    frame_ani_pet, sprite_pet_paths, entry_ani_pet_interval = create_animation_entry(window_anisettings, "Pet / Play Animation Frame(s):", pick_file, 
                                                                                                           default_value= PET_SPRITE, 
                                                                                                           default_interval= SPRITE_INTERVAL, 
                                                                                                           font_default= FONT_DEFALT, 
                                                                                                           font_bold= FONT_BOLD,
                                                                                                           default_width=WIDTH)
    frame_ani_pet.pack(pady=PADDING)

    # Work sprites and interval
    frame_ani_work, sprite_pet_paths, entry_ani_work_interval = create_animation_entry(window_anisettings, "Pet / Play Animation Frame(s):", pick_file, 
                                                                                                           default_value= WORK_SPRITE, 
                                                                                                           default_interval= SPRITE_INTERVAL, 
                                                                                                           font_default= FONT_DEFALT, 
                                                                                                           font_bold= FONT_BOLD,
                                                                                                           default_width=WIDTH)
    frame_ani_work.pack(pady=PADDING)

    def close_anisettings():
        global window_anisettings_open, sprite_idle_interval, sprite_walk_interval, sprite_eat_interval, sprite_hungry_interval, sprite_pet_interval, sprite_work_interval

        window_anisettings_open = False
        sprite_idle_interval = get_with_default(entry_ani_idle_interval, SPRITE_INTERVAL, float)
        sprite_walk_interval = get_with_default(entry_ani_walk_interval, SPRITE_INTERVAL, float)
        sprite_eat_interval = get_with_default(entry_ani_eat_interval, SPRITE_INTERVAL, float)
        sprite_hungry_interval = get_with_default(entry_ani_hungry_interval, SPRITE_INTERVAL, float)
        sprite_pet_interval = get_with_default(entry_ani_pet_interval, SPRITE_INTERVAL, float)
        sprite_work_interval = get_with_default(entry_ani_work_interval, SPRITE_INTERVAL, float)

        window_anisettings.destroy()
    
    # Closing the window
    button_close = tk.Button(window_anisettings, text="Save & close", 
                                command=close_anisettings)
    button_close.pack()
    window_anisettings.protocol("WM_DELETE_WINDOW", close_anisettings)


frame_ani = ttk.Frame(master=root)
label_ani = ttk.Label(master=frame_ani, text="Animation Frames [GIF or PNG]", font=FONT_BOLD)
button_ani = tk.Button(master=frame_ani, 
                       text="Open Animation Settings", 
                       bg="#19CEE6", command=open_anisettings)
label_ani.pack(pady=PADDING)
button_ani.pack(pady=PADDING)
frame_ani.pack(pady=PADDING)



# Chromakey Entry
frame_chromakey, var_chromakey_selection = create_color_entry(root, "Chormakey Color", pick_color, FONT_BOLD, FONT_DEFALT)
frame_chromakey.pack(pady=PADDING)



# AADDITIONAL SETTINGS WINDOW ===
action_idle_interval = ACTION_IDLE_INTERVAL
action_idle_treshold = ACTION_IDLE_TRESHOLD
action_eat_treshold = ACTION_EAT_TRESHOLD
action_pet_treshold = ACTION_PET_TRESHOLD

hunger_decay_interval = HUNGER_DECAY_INTERVAL
hunger_decay_rate = HUNGER_DECAY_RATE

hunger_recover_rate = HUNGER_RECOVER_RATE

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
    window_additionalsettings = tk.Toplevel(master=root, padx=10, pady=10)
    window_additionalsettings.title("Additional Settings")

    # Action idle interval entry
    frame_action_idle_interval, (entry_action_idle_interval) = create_general_entry(window_additionalsettings, "Idle action interval (in seconds):", 1, 
                                                                                    default_value= ACTION_IDLE_INTERVAL, 
                                                                                    font_bold= FONT_BOLD, 
                                                                                    font_default= FONT_DEFALT)
    frame_action_idle_interval.pack(pady=PADDING)

    # Action idle treshhold entry
    frame_action_idle_treshold, (entry_action_idle_tresholdleft, entry_action_idle_tresholdright) = create_general_entry(window_additionalsettings, "Idle action treshold:", 2, 
                                                                                                                    default_value= ACTION_IDLE_TRESHOLD, 
                                                                                                                    font_bold= FONT_BOLD, 
                                                                                                                    font_default= FONT_DEFALT)
    frame_action_idle_treshold.pack(pady=PADDING)

    # Action eat treshhold entry
    frame_action_eat_treshold, (entry_action_eat_treshold)  = create_general_entry(window_additionalsettings, "Chance for eating animation to be repeated\n(1 very likely - 10 never):", 1, 
                                                                                    default_value= ACTION_EAT_TRESHOLD, 
                                                                                    font_bold= FONT_BOLD, 
                                                                                    font_default= FONT_DEFALT)
    frame_action_eat_treshold.pack(pady=PADDING)

    # Action pet treshhold entry
    frame_action_pet_treshold, (entry_action_pet_treshold)  = create_general_entry(window_additionalsettings, "Chance for petting animation to be repeated\n(1 very likely - 10 never):", 1, 
                                                                                    default_value= ACTION_PET_TRESHOLD, 
                                                                                    font_bold= FONT_BOLD, 
                                                                                    font_default= FONT_DEFALT)
    frame_action_pet_treshold.pack(pady=PADDING)

    # Hunger decay interval entry
    frame_hunger_decay_interval, (entry_hunger_decay_interval) = create_general_entry(window_additionalsettings, "Hunger drain interval (in seconds):", 1, 
                                                                          default_value= HUNGER_DECAY_INTERVAL, 
                                                                          font_bold= FONT_BOLD, 
                                                                          font_default= FONT_DEFALT)
    frame_hunger_decay_interval.pack(pady=PADDING)

    # Hunger decay rate entry
    frame_hunger_decay_rate, (entry_hunger_decay_rate) = create_general_entry(window_additionalsettings, "Hunger drain rate:", 1, 
                                                                  default_value= HUNGER_DECAY_RATE, 
                                                                  font_bold= FONT_BOLD, 
                                                                  font_default= FONT_DEFALT)
    frame_hunger_decay_rate.pack(pady=PADDING)

    # Hunger recovery rate entry
    frame_hunger_recover_rate, (entry_hunger_recover_rate) = create_general_entry(window_additionalsettings, "Hunger recover rate per food:", 1, 
                                                                  default_value= HUNGER_RECOVER_RATE, 
                                                                  font_bold= FONT_BOLD, 
                                                                  font_default= FONT_DEFALT)
    frame_hunger_recover_rate.pack(pady=PADDING)

    def close_additionalsettings():
        global window_additionalsettings_open, action_idle_interval, action_idle_treshold, action_eat_treshold, action_pet_treshold, hunger_decay_interval, hunger_decay_rate, hunger_recover_rate

        window_additionalsettings_open = False

        action_idle_interval = get_with_default(entry_action_idle_interval, ACTION_IDLE_INTERVAL)
        action_idle_treshold = ( get_with_default(entry_action_idle_tresholdleft, ACTION_IDLE_TRESHOLD[0]),
                                 get_with_default(entry_action_idle_tresholdright, ACTION_IDLE_TRESHOLD[1]) )
        
        action_eat_treshold = get_with_default(entry_action_eat_treshold, ACTION_EAT_TRESHOLD)
        action_pet_treshold = get_with_default(entry_action_pet_treshold, ACTION_EAT_TRESHOLD)
        
        hunger_decay_interval = get_with_default(entry_hunger_decay_interval, HUNGER_DECAY_INTERVAL)
        hunger_decay_rate = get_with_default(entry_hunger_decay_rate, HUNGER_DECAY_RATE)
        hunger_recover_rate = get_with_default(entry_hunger_recover_rate, HUNGER_RECOVER_RATE)

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
    user = get_with_default(entry_user, USER_NAME, str)
    name = get_with_default(entry_name, NAME, str)

    prompt = get_with_default(entry_prompt, PROMPT, str)

    pos_x = get_with_default(entry_pos_x, POS_X)
    pos_y = get_with_default(entry_pos_y, POS_Y)

    size_x = get_with_default(entry_size_x, SIZE_X) 
    size_y = get_with_default(entry_size_y, SIZE_Y)

    speed_x = get_with_default(entry_speed_x, SPEED_X)
    speed_y = get_with_default(entry_speed_y, SPEED_Y)
    
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
        "sprite_pet_interval" :sprite_pet_interval,
        "sprite_pet_path": resize(sprite_pet_paths,  
                              (size_x, size_y),
                                (name, "pet")),
        "sprite_work_interval" :sprite_work_interval,
        "sprite_work_path": resize(sprite_work_paths,  
                              (size_x, size_y),
                                (name, "work")),
        "chroma_key": chromakey,
        "action_idle_interval" : float(action_idle_interval) if action_idle_interval else ACTION_IDLE_INTERVAL,
        "action_idle_treshold" : tuple(action_idle_treshold) if action_idle_treshold else ACTION_IDLE_TRESHOLD,
        "action_eat_treshold": action_eat_treshold,
        "action_pet_treshold": action_pet_treshold,
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
button_create_pet.pack(padx=PADDING, side="left")

button_load_pet = tk.Button(master=frame_pet, text="Load Pet!", 
                            bg="#CC9F0A",
                            command=lambda: load_pet(user_pets))
button_load_pet.pack(padx=PADDING, side="left")

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

    label_shop = tk.Label(master=window_shop, text= "WELCOME TO THE SHOP! :D", font=FONT_BOLD)
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
    
    frame_stat = ttk.Frame(master=window_shop)
    label_coin = ttk.Label(master=frame_stat, textvariable=var_user_coin, font=FONT_DEFALT)
    
    frame_food = ttk.Frame(master=frame_stat)
    label_food = ttk.Label(master=frame_food, textvariable=var_user_food, font=FONT_DEFALT)
    button_foodbuy = tk.Button(master=frame_food, text="Buy Food!",
                               command=buy_food)
    
    label_coin.pack(side="top")
    
    label_food.pack(side="left",padx=PADDING)
    button_foodbuy.pack(side="right", padx=PADDING)
    frame_food.pack(pady=PADDING)
    
    frame_stat.pack(pady=PADDING)

frame_shop = ttk.Frame(master=root)
button_shop = tk.Button(master=frame_shop, text="Open Shop!",
                        bg="#FFFB00",
                        command = open_shop)
button_shop.pack()
frame_shop.pack()

# Start the Tkinter event loop 
root.mainloop()
