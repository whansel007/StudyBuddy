# Define a pet class to be initialized
import tkinter as tk
import time
from pet_statemachine import get_current_states
from pet_movement import get_current_movement
from pet_animation import get_current_image

class pet():
    def __init__(self, master, info_dict:dict):
        # Static Data
        self.name = info_dict["name"]
        
        self.size_x = info_dict["size_x"]
        self.size_y = info_dict["size_y"]

        self.x = info_dict["pos_x"]
        self.y = info_dict["pos_y"]

        self.sprites_idle = info_dict["sprites_idle"]
        self.sprites_walk = info_dict["sprites_walk"]
        self.sprite_interval = 10

        self.chroma_key = info_dict["chroma_key"]

        # Dynamic Data
        self.state = "Idle"
        self.state_ani = "idle"
        self.state_mov = "idle"

        self.x_move = 0
        self.y_move = 0

        self.img = tk.PhotoImage(file=self.sprites_idle[0])

        self.timestamp = time.time()
        self.timestamp_ani = time.time()
        
        # Window 
        self.window = tk.Toplevel(master)
        self.window.overrideredirect(True) # Frameless
        self.window.attributes('-topmost', True) # Draw over all others
        self.window.wm_attributes('-transparentcolor',self.chroma_key) # Interpert exery pixel of that color is transparent
        
        # Image
        self.label = tk.Label(self.window, bd=0, bg=self.chroma_key) # Border line thickness of 0 and the background chroma key color (since need to have background color) 
        self.label.configure(image=self.img)
        self.label.pack()
        
        # Run self.update() after 0ms when mainloop starts
        self.window.after(0, self.update)

        print(f"self is {self}")
    
    def update_states(self):
        self.state, self.state_ani, self.state_mov = get_current_states(self)

    def update_position(self):
        self.x_move, self.y_move = get_current_movement()

        self.x += self.x_move
        self.y += self.y_move

        draw_x = self.x if self.x < 0 else f'+{self.x}'
        draw_y = self.y if self.y < 0 else f'+{self.y}'
        
        self.window.geometry(f'{self.size_x}x{self.size_y}{draw_x}{draw_y}') 
    
    def update_animation(self):
        self.img = tk.PhotoImage(file=self.sprites_idle[0])
        self.label.configure(image=self.img)
        self.label.pack()

    
    def update(self):
        # self.update_states()
        # self.update_position()
        # self.update_animation()

        self.window.after(10, self.update)
        
