# A window containing which animation 
# In a Tkinter app: open picker from a button callback
import tkinter as tk
from tkinter import filedialog

def pick_file():
    path = filedialog.askopenfilename(title="Open file", filetypes=[("GIF","*.gif"), ("All","*.*")])
    if path:
        label.config(text=path)

root = tk.Tk()
root.title("Animation picker")
btn = tk.Button(root, text="Choose file", command=pick_file)
btn.pack(pady=8)
label = tk.Label(root, text="No file chosen")
label.pack()
root.mainloop()