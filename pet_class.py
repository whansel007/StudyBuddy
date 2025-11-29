import tkinter as tk
import time
import random

class pet():
    def __init__(self, master, info_dict:dict):
        # Data extraction
        self.name = info_dict["name"]
        
        self.size_x = info_dict["size_x"]
        self.size_y = info_dict["size_y"]

        self.x = info_dict["pos_x"]
        self.y = info_dict["pos_y"]
        
        # Window 
        self.window = tk.Toplevel(master)
        self.window.overrideredirect(True) # frameless
        self.window.attributes('-topmost', True) # draw over all others
        chroma_key = 'gray' #a color not in sprite 
        self.window.wm_attributes('-transparentcolor',chroma_key) # window will interpert exery pixel of that color is transparent
        
        # Image
        self.label = tk.Label(self.window, bd=0, bg=chroma_key) # border line thickness of 0 and the background chroma key color (since will always have background color) 
        self.label.configure(image=self.img)
        self.label.pack()

        # Time
        self.timestamp = time.time()
        
        # Run self.update() after 0ms when mainloop starts
        self.window.after(0, self.update)

    def update_position(self):
        draw_x = self.x if self.x < 0 else f'+{self.x}'
        draw_y = self.y if self.y < 0 else f'+{self.y}'
        
        self.window.geometry(f'{self.size_x}x{self.size_y}{draw_x}{draw_y}') 
    
    def update_animation(self):
        self.label.configure(image=self.img)
        self.label.pack()

    
    def update(self):
        self.update_position()
        self.update_animation()

        self.window.after(10, self.update)
        
