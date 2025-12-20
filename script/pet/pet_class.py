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

        self.sprite_idle_path = info_dict["sprite_idle_path"]
        self.sprite_idle_interval = info_dict["sprite_idle_interval"]

        self.sprite_walk_path = info_dict["sprite_walk_path"]
        self.sprite_walk_interval = info_dict["sprite_walk_interval"]

        self.sprite_eat_path = info_dict["sprite_eat_path"]
        self.sprite_eat_interval = info_dict["sprite_eat_interval"]
    
        self.sprite_hungry_path = info_dict["sprite_hungry_path"]
        self.sprite_hungry_interval = info_dict["sprite_hungry_interval"]

        self.chroma_key = info_dict["chroma_key"]
        self.prompt = info_dict["prompt"]

        self.action_idle_interval = info_dict["action_idle_interval"]
        self.action_idle_treshold = info_dict["action_idle_treshold"]

        self.action_eat_treshold = info_dict["action_eat_treshold"]
        
        self.hunger = info_dict["hunger"]
        self.hunger_max = info_dict["hunger_max"]
        self.hunger_decay_rate = info_dict["hunger_decay_rate"]
        self.hunger_decay_interval = info_dict["hunger_decay_interval"]
        self.hunger_recover_rate = info_dict["hunger_recover_rate"]

        self.save_path = info_dict["save_path"]
        self.info_dict = info_dict

        # Call back
        self.feed_callback = callback_dict["feed_callback"]

        # Dynamic Data
        self.state = "idle"
        self.state_ani = "null"
        self.state_mov = "null"
        self.previous_state = self.state
        
        self.move_x = 0
        self.move_y = 0
        self.speed_modifier = 1
        
        self.keyboard_x = 0
        self.keyboard_y = 0

        self.img = tk.PhotoImage(file=self.sprite_idle_path[0])
        self.sprite_flip = False        
        self.sprite_current = self.sprite_idle_path
        self.sprite_interval = info_dict["sprite_idle_interval"]
        self.sprite_timestamp = time.time()
        self.sprite_index = 0

        self.action_idle_timestamp = time.time()
        self.action_idle_roll = 0

        self.action_eat_roll = 0
        
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
        

        # THE PET MENU ===
        # Create the pet's right-click menu
        self.pet_menu = tk.Menu(self.window, tearoff=0)
        
        # Pet Stat menu
        self.pet_menu.add_command(label="Hunger 0/0", state="disabled") # Index 0 for hunger status
        self.pet_menu.add_separator()
        
        # Feed menu
        self.pet_menu.add_command(label="Feed", command=self.feed_pet)
        self.pet_menu.add_separator() 
        
        # Play menu
        self.pet_menu.add_command(label="Play", command=self.play_with_pet)
        self.pet_menu.add_separator()
       
        # Work Pomodoro menu
        self.pet_menu.add_command(label="Pomodoro", command=self.open_pomodoro)

        # Work Transcribe menu
        self.transcribe_submenu = tk.Menu()
        self.pet_menu.add_separator()
        
        self.pet_menu.add_command(label="Send to stasis", command=self.close_pet)
        self.pet_menu.add_separator()
        self.pet_menu.add_command(label="Cancel")

        self.label.configure(image=self.img)
        self.label.pack()
        
        # Run self.update() after 0ms when mainloop starts
        self.window.after(0, self.update)

        print(f"HARK! I am brought into existence with these details \n{self}")
    
    # To print out all attributes the object has
    def __str__(self):
        attirbutes = "\n".join(f"{key} = {value}" for key,value in self.__dict__.items())
        return attirbutes
    


    # PET INTERACTION ===
    def close_pet(self):
        self.info_dict["hunger"] = self.hunger
        print(f"SAVING \n {self.info_dict}")

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
        if self.feed_callback():
            print(f"Feeding {self.name}!")
            self.change_state("eating")
            self.hunger = min(self.hunger + self.hunger_recover_rate, self.hunger_max)
        else:
            print(f"Not enough food to feed {self.name}!")

    def play_with_pet(self):
        print(f"Playing with {self.name}!")
    
    def open_pomodoro(self):
        print(f"{self.name} Opening pomodoro window!")



    # PET STATE + HUNGER  ===
    def change_state(self, target:str):
        # Return early if already at target state
        if self.state == target:
            return
        
        # If switching into idle, set time stamp to be 0 so that the roll and switching of other states happens instantly instead of waiting for the timestamp window
        if target == "idle":
            self.action_idle_timestamp = 0

        # Save previous state only if it's not the hungry state
        if self.state != "hungry":
            self.previous_state = self.state

        self.state = target
        print(f"PREVIOUSLY {self.previous_state} ==> {self.state}")
    
    def update_hunger(self):
        # Update hunger
        if time.time() >= self.hunger_timestamp + self.hunger_decay_interval:
            self.hunger -= self.hunger_decay_rate
            self.hunger_timestamp = time.time()
        self.hunger = max(0, min(self.hunger, self.hunger_max))

        if self.hunger <= 0:
            self.change_state("hungry")
    
    def update_substates(self):
        # IDLE STATE --> Frolick around randomly
        if self.state == "idle":
            # print(f"{self.name} is Idle!")
            self.update_hunger()
            # Randomly switchs between moving right, moving left, and idle every interval
            if time.time() >= self.action_idle_timestamp + self.action_idle_interval:        
                self.action_idle_roll = random.randint(-10, 10)
                print(f"ROLLED {self.action_idle_roll}")

                #                 ========idle========
                # -10 - - - - - T0 - - - -  0 - - - - T1 - - - - -  10
                # =====left=======                    =====right=======

                if self.action_idle_roll <= self.action_idle_treshold[0]:
                    self.change_movement("left", vary_speed=True)
                    self.change_animation("left")
                elif self.action_idle_roll >= self.action_idle_treshold[1]:
                    self.change_movement("right", vary_speed=True)
                    self.change_animation("right")
                else:
                    self.change_movement("idle")
                    self.change_animation("idle")
                
                self.action_idle_timestamp = time.time() # Reset idle timestamp
        
        # EATING STATE --> Do not move and eat
        elif self.state == "eating":
            # Do not move and switch to hungry sprite
            self.change_movement("idle")
            self.change_animation("eating")
            #print(f"{self.name} is Eating!")

        # HUNGRY STATE --> Do not move and make sad face
        elif self.state == "hungry":
            # Do not move and switch to hungry sprite
            self.change_movement("idle")
            self.change_animation("hungry")
            # print(f"{self.name} is Hungry!")
    

    
    # MOVEMENT STATE ===
    def change_movement(self, target:str, vary_speed:bool=False):
        # Return early if already at target state
        if self.state_mov == target:
            return

        self.state_mov = target
        
        if vary_speed:
            self.speed_modifier = random.uniform(0.1,1.0)
        else:
            self.speed_modifier = 1
        
        self.move_x = max(1, int(self.speed_x * self.speed_modifier))
        self.move_y = max(1, int(self.speed_y * self.speed_modifier))

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



    # ANIMATION STATE ===
    def change_animation(self, target:str):
        # Return early if already at target state
        if self.state_ani == target:
            return

        self.state_ani = target
        self.sprite_index = 0

        if self.state_ani == "idle":
            self.sprite_current = self.sprite_idle_path
            self.sprite_interval = self.sprite_idle_interval

        elif self.state_ani == "left":
            self.sprite_current = self.sprite_walk_path
            self.sprite_interval = self.sprite_walk_interval
            self.sprite_flip = False

        elif self.state_ani == "right":
            self.sprite_current = self.sprite_walk_path
            self.sprite_interval = self.sprite_walk_interval
            self.sprite_flip = True
        
        elif self.state_ani == "eating":
            self.sprite_current = self.sprite_eat_path
            self.sprite_interval = self.sprite_eat_interval
    
        elif self.state_ani == "hungry":
            self.sprite_current = self.sprite_hungry_path
            self.sprite_interval = self.sprite_hungry_interval

        print(f"Current animation set = {self.sprite_current}")
    
    def update_animation(self):
        # Increase the sprite index every interval and reset the timer
        if time.time() >= self.sprite_timestamp + self.sprite_interval:
            self.sprite_index = self.sprite_index + 1

            # print(f"Current index {self.sprite_index} out of {len(self.sprite_current)}")

            # When we hit the last frame reset back to 0
            if self.sprite_index >= len(self.sprite_current):
                self.sprite_index = 0
                
                # Special logic for eating
                if self.state_ani == "eating":
                    self.action_eat_roll = random.randint(1,10)
                    print(f"EAT ROLLED {self.action_eat_roll}")
                    if self.action_eat_roll <= self.action_eat_treshold:
                        self.change_state(self.previous_state)
                

            self.sprite_timestamp = time.time()


        img_path = self.sprite_current[self.sprite_index]
        img = Image.open(img_path)

        if self.sprite_flip:
            img = img.transpose(Image.FLIP_LEFT_RIGHT)

        self.img = ImageTk.PhotoImage(img)
        self.label.configure(image=self.img)
    
    def update(self):
        self.update_substates()
        self.update_position()
        self.update_animation()

        self.window.after(10, self.update)
        
