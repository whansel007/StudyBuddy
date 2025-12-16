# Define a pet class to be initialized
import tkinter as tk
import json
import random
import time
from PIL import Image, ImageTk

class pet():
    def __init__(self, master, info_dict:dict, callback_dict:dict):
        # Extract Data
        self.name = info_dict["name"]
        
        self.size_x = info_dict["size_x"]
        self.size_y = info_dict["size_y"]

        self.x = info_dict["pos_x"]
        self.y = info_dict["pos_y"]
        self.screenwidth, self.screenheight = info_dict["screensize"]

        self.speed_x = info_dict["speed_x"]
        self.speed_y = info_dict["speed_y"]

        self.sprites_idle = info_dict["sprites_idle"]
        self.sprites_walk = info_dict["sprites_walk"]

        self.sprite_interval = info_dict["sprite_idleinterval"]
        self.sprite_idleinterval = info_dict["sprite_idleinterval"]
        self.sprite_walkinterval = info_dict["sprite_walkinterval"]
        
        self.chroma_key = info_dict["chroma_key"]
        self.prompt = info_dict["prompt"]

        self.action_interval = info_dict["action_interval"]
        self.action_treshold = info_dict["action_treshold"]
        
        self.hunger = info_dict["hunger"]
        self.hunger_max = info_dict["hunger_max"]
        self.hunger_decayrate = info_dict["hunger_decayrate"]
        self.hunger_decayinterval = info_dict["hunger_decayinterval"]

        self.save_path = info_dict["save_path"]
        self.info_dict = info_dict

        # Call back
        self.feed_callback = callback_dict.get("feed_callback")

        # Dynamic Data
        self.state = "idle"
        self.state_ani = "idle"
        self.state_mov = "idle"
        
        self.move_x = 0
        self.move_y = 0
        self.speed_modifier = 1
        
        self.keyboard_x = 0
        self.keyboard_y = 0

        self.img = tk.PhotoImage(file=self.sprites_idle[0])
        self.sprite_timestamp = time.time()
        self.sprite_set = self.sprites_idle
        self.sprite_index = 0
        self.sprite_flip = False

        self.idle_timestamp = time.time()
        self.idle_roll = 0
        
        self.hunger_timestamp = time.time()

        # Window 
        self.window = tk.Toplevel(master)
        self.window.overrideredirect(True) # Frameless
        self.window.attributes('-topmost', True) # Draw over all others
        self.window.wm_attributes('-transparentcolor',self.chroma_key) # Interpert exery pixel of that color is transparent
        self.window.protocol("WM_DELETE_WINDOW", self.close_pet)

        self.x = self.x if self.x > 0 else self.screenwidth + self.x
        self.y = self.y if self.y > 0 else self.screenheight + self.y
        self.window.geometry(f'{self.size_x}x{self.size_y}+{self.x}+{self.y}') 
        
        # Image
        self.label = tk.Label(self.window, bd=0, bg=self.chroma_key) # Border line thickness of 0 and the background chroma key color (since need to have background color)
        self.label.bind("<Button-3>", self.show_petmenu) 
        
        # Create the pet's right-click menu
        self.pet_menu = tk.Menu(self.window, tearoff=0)
        self.pet_menu.add_command(label="", state="disabled") # Index 0 for hunger status
        self.pet_menu.add_separator()
        self.pet_menu.add_command(label="Feed", command=self.feed_pet)
        self.pet_menu.add_command(label="Play", command=self.play_with_pet)
        self.pet_menu.add_separator()
        self.pet_menu.add_command(label="Send to stasis", command=self.close_pet)
        self.pet_menu.add_separator()
        self.pet_menu.add_command(label="Cancel")

        self.label.configure(image=self.img)
        self.label.pack()
        
        # Run self.update() after 0ms when mainloop starts
        self.window.after(0, self.update)

        print(f"HARK! I am brought into existence with these details \n{self}")
    
    def close_pet(self):
        self.info_dict["hunger"] = self.hunger
        print(f"Saving \n {self.info_dict}")

        with open(self.save_path, "w", encoding="utf-8") as save_file:
            json.dump(self.info_dict,save_file, indent=4)
        
        self.window.destroy()
    
    def show_petmenu(self, event):
        """
        This function is the event handler for the right-click.
        It updates the hunger status in the menu and then displays it.
        """
        
        hunger_text = f"Hunger: {int(self.hunger)}/{self.hunger_max}"
        self.pet_menu.entryconfig(0, label=hunger_text)

        self.pet_menu.post(event.x_root, event.y_root)

    def feed_pet(self):
        if self.feed_callback and self.feed_callback():
            print(f"Feeding {self.name}!")
            self.hunger = min(self.hunger + 25, self.hunger_max)
        else:
            print(f"Not enough food to feed {self.name}!")

    def play_with_pet(self):
        print(f"Playing with {self.name}!")

    def __str__(self):
        attirbutes = "\n".join(f"{key} = {value}" for key,value in self.__dict__.items())
        return attirbutes

    def switch_state(self, target):
        self.state = target
    
    def update_substates(self):
        # IDLE STATE --> Frolick around randomly
        if self.state == "idle":

            # Randomly switchs between moving right, moving left, and idle every interval
            if time.time() >= self.idle_timestamp + self.action_interval:        
                self.idle_roll = random.randint(self.action_treshold[0], self.action_treshold[1])
                print(f"ROLLED {self.idle_roll}")

                #                 ========idle========
                # -10 - - - - - T0 - - - -  0 - - - - T1 - - - - -  10
                # =====left=======                    =====right=======

                if self.idle_roll <= self.action_treshold[0]:
                    self.change_movement("left", vary_speed=True)
                    self.change_animation("left")
                elif self.idle_roll >= self.action_treshold[1]:
                    self.change_movement("right", vary_speed=True)
                    self.change_animation("right")
                else:
                    self.change_movement("idle")
                    self.change_animation("idle")
                
                self.idle_timestamp = time.time() # Reset idle timestamp
        
        # HUNGRY STATE --> Do not move
        elif self.state == "hungry":
            # Do not move and switch to hungry sprite
            self.state_mov = "idle"
            self.state_ani = "hungry"
            print("Hungry!")
    
    def change_movement(self, target:str, vary_speed:bool=False):
        self.state_mov = target
        
        if vary_speed:
            self.speed_modifier = random.uniform(0.1,1.0)
        else:
            self.speed_modifier = 1
        
        self.move_x = max(1, int(self.speed_x * self.speed_modifier))
        self.move_y = max(1, int(self.speed_y * self.speed_modifier))
    
    def update_hunger(self):
        # Update hunger
        if time.time() >= self.hunger_timestamp + self.hunger_decayinterval:
            self.hunger -= self.hunger_decayrate
            self.hunger_timestamp = time.time()
        self.hunger = max(0, min(self.hunger, self.hunger_max))

    def update_position(self):
        # TOP LEFT CORNER (0,0)
        #
        # up and left is - || down and right is +
        # 
        #                      BOTTOM RIGHT CORNER (max, max)
        if self.state_mov == "left":
            self.x -= self.move_x
        elif self.state_mov == "right":
            self.x += self.move_x
        elif self.state_mov == "up":
            self.y -= self.move_y
        elif self.state_mov == "down":
            self.y += self.move_y
        elif self.state_mov == "controlled":
            self.x = self.move_x * self.keyboard_x
            self.y = self.move_y * self.keyboard_y
        else:
            # Reset move values to 0 when idle
            self.move_x = 0
            self.move_y = 0
        
        #print(self.x, self.y)
        self.x = self.x % self.screenwidth
        self.y = self.y % self.screenheight
        self.window.geometry(f'{self.size_x}x{self.size_y}+{self.x}+{self.y}') 

    def change_animation(self, target:str):
        self.state_ani = target
        self.sprite_index = 0

        if self.state_ani == "idle":
            self.sprite_set = self.sprites_idle
            self.sprite_interval = self.sprite_idleinterval

        elif self.state_ani == "left":
            self.sprite_set = self.sprites_walk
            self.sprite_interval = self.sprite_walkinterval
            self.sprite_flip = False

        elif self.state_ani == "right":
            self.sprite_set = self.sprites_walk
            self.sprite_interval = self.sprite_walkinterval
            self.sprite_flip = True
    
    def update_animation(self):
        if time.time() >= self.sprite_timestamp + self.sprite_interval:
            self.sprite_index = (self.sprite_index + 1) % len(self.sprite_set)
            self.sprite_timestamp = time.time()

        img_path = self.sprite_set[self.sprite_index]
        img = Image.open(img_path)

        if self.sprite_flip:
            img = img.transpose(Image.FLIP_LEFT_RIGHT)

        self.img = ImageTk.PhotoImage(img)
        self.label.configure(image=self.img)
    
    def update(self):
        self.update_hunger()
        self.update_substates()
        self.update_position()
        self.update_animation()

        self.window.after(10, self.update)
        
