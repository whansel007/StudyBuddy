import tkinter as tk
import time
import random

class Pet():
    def __init__(self, master, x_pos=0, y_pos = 0):
        # Window 
        self.window = tk.Toplevel(master)
        
        self.name = "Test"
        
        self.size_x = 600
        self.size_y = 600        
        
        self.x = x_pos if x_pos < 0 else f'+{x_pos}'
        self.y = y_pos if y_pos < 0 else f'+{y_pos}'
        
        self.window.geometry(f'{self.size_x}x{self.size_y}{self.x}{self.y}') 
        
        self.window.overrideredirect(True) # frameless
        self.window.attributes('-topmost', True) # draw over all others
        
        chroma_key = 'gray' #a color not in sprite 
        self.window.wm_attributes('-transparentcolor',chroma_key) # window will interpert exery pixel of that color is transparent
        
        
        # Image
        self.total_frames = 20
        self.walking_right = [tk.PhotoImage(file='Assets/william_cat_idle.gif', format='gif -index %i' % (i)) for i in range(self.total_frames)]
        self.frame_index = 0
        self.img = self.walking_right[self.frame_index] 
         
        self.label = tk.Label(self.window, bd=0, bg=chroma_key) # border line thickness of 0 and the background chroma key color (since will always have background color) 
        self.label.configure(image=self.img)
        self.label.pack()


        # Time
        self.timestamp = time.time()
        self.animation_interval = 0.20
        
        
        # Run self.update() after 0ms when mainloop starts
        self.window.after(0, self.update)  
        
    def update(self):
        
        # Movement
        self.x += random.randrange(-5,5)
        
        if time.time() > self.timestamp + self.animation_interval:
            self.timestamp = time.time()
            # advance the frame by one, wrap back to 0 at the end
            self.frame_index = (self.frame_index + 1) % self.total_frames
            self.img = self.walking_right[self.frame_index]
        
        self.window.geometry(f'{self.size_x}x{self.size_y}{self.x}{self.y}') 

        self.label.configure(image=self.img)
        self.label.pack()
        
        self.window.after(10, self.update)
        

