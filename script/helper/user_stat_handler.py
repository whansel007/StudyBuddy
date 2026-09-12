# User Inventory Variables
from pathlib import Path
import os
import json

USER_STATPATH = str(Path("asset") / "user_stat.json")
DEFAULT_USER_STAT = { 
    "coin": 10,
    "food": 5,
    "auto":True,
    "last":""}

var_user_coin = None
var_user_food = None
var_user_auto = None
var_user_last = None

# Create User Stat if it doesn't exist
print("Checking if the user stat path exist")
if not os.path.exists(USER_STATPATH):
    print("It doesnt")
    with open(USER_STATPATH, "w",  encoding="utf-8") as save_path:
        json.dump(DEFAULT_USER_STAT,save_path, indent=4)

# Load User Stat
def load_stat():
    
    user_stat = {
        "coin" : 0,
        "food" : 0,
        "auto" : 0,
        "last" : ""
    }
    
    with open(USER_STATPATH, "r", encoding="utf-8") as save_file:
        loaded_stat = json.load(save_file)
        user_stat["auto"] = loaded_stat["auto"]
        user_stat["coin"] = loaded_stat["coin"]
        user_stat["food"] = loaded_stat["food"]
        user_stat["last"] = loaded_stat["last"]
        
        # var_user_auto = tk.BooleanVar(value=user_auto)
        # var_user_coin = tk.StringVar(value=f"Coin : {user_coin}")
        # var_user_food = tk.StringVar(value=f"Food : {user_food}")
        
    return user_stat

# Update the use stat
def update_stat(
    user_stat,
    new_user_coin = None, 
    new_user_food = None, 
    new_user_auto = None,
    new_user_last = None):
    
    with open(USER_STATPATH, "w", encoding="utf-8") as stat_file:
        json.dump({
            "coin": new_user_coin or user_stat["coin"], 
            "food": new_user_food or user_stat["food"],
            "auto": new_user_auto or user_stat["auto"],
            "last": new_user_last or user_stat["last"]}, 
            stat_file, 
            indent=4)