# Define a pet class to be initialized
import tkinter as tk
import random
import time
from PIL import Image, ImageTk

class pet():
    def __init__(self, master, info_dict:dict):
        # Static Data
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

        self.idle_interval = info_dict["idle_interval"]
        self.idle_treshold = info_dict["idle_treshold"]

        # Dynamic Data
        self.state = "idle"
        self.state_ani = "idle"
        self.state_mov = "idle"

        self.move_x = 0
        self.move_y = 0

        self.speed_modifier = 1

        self.img = tk.PhotoImage(file=self.sprites_idle[0])

        self.idle_timestamp = time.time()
        self.idle_roll = 0

        self.sprite_timestamp = time.time()
        self.sprite_set = self.sprites_idle
        self.sprite_index = 0

        self.sprite_flip = False

        # Window 
        self.window = tk.Toplevel(master)
        self.window.overrideredirect(True) # Frameless
        self.window.attributes('-topmost', True) # Draw over all others
        self.window.wm_attributes('-transparentcolor',self.chroma_key) # Interpert exery pixel of that color is transparent
        
        self.x = self.x if self.x > 0 else self.screenwidth + self.x
        self.y = self.y if self.y > 0 else self.screenheight + self.y
        self.window.geometry(f'{self.size_x}x{self.size_y}+{self.x}+{self.y}') 
        
        # Image
        self.label = tk.Label(self.window, bd=0, bg=self.chroma_key) # Border line thickness of 0 and the background chroma key color (since need to have background color) 
        
        self.label.configure(image=self.img)
        self.label.pack()
        
        # Run self.update() after 0ms when mainloop starts
        self.window.after(0, self.update)

        print(f"self is {self}")
    
    def __str__(self):
        attirbutes = "\n".join(f"{key} = {value}" for key,value in self.__dict__.items())
        return attirbutes

    def switch_state(self, target):
        self.state = target
    
    def update_substates(self):
        # IDLE STATE --> Frolick around randomly
        if self.state == "idle":

            # Randomly switchs between moving right, moving left, and idle every interval
            if time.time() >= self.idle_timestamp + self.idle_interval:        
                self.idle_roll = random.randint(self.idle_treshold[0], self.idle_treshold[1])
                print(f"ROLLED {self.idle_roll}")

                #                 ========idle========
                # -10 - - - - - T0 - - - -  0 - - - - T1 - - - - -  10
                # =====left=======                    =====right=======

                if self.idle_roll <= self.idle_treshold[0]:
                    self.change_movement("left", vary_speed=True)
                    self.change_animation("left")
                elif self.idle_roll >= self.idle_treshold[1]:
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
            self.speed_modifier = random.uniform(0,1.0)
        else:
            self.speed_modifier = 1


    def update_position(self):
        if self.state_mov == "left":
            self.move_x = -int(self.speed_x * self.speed_modifier)
            self.move_y = 0
        elif self.state_mov == "right":
            self.move_x = int(self.speed_x * self.speed_modifier)
            self.move_y = 0
        else:
            self.move_x = 0
            self.move_y = 0
        
        #print(self.x, self.y)

        self.x += self.move_x
        self.y += self.move_y

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
        self.update_substates()
        self.update_position()
        self.update_animation()

        self.window.after(10, self.update)
        
