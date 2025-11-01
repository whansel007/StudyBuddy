import tkinter as tk
from pet_ui import Pet

# --- Settings ---
def create_pet():
    x_pos = -300 
    y_pos = -35
    new_pet = Pet(root, x_pos=x_pos, y_pos=y_pos)
    pets.append(new_pet)

# --- Main window ---
root = tk.Tk()
root.title("Settings")
root.geometry("200x100")

add_pet_button = tk.Button(root, text="Add Pet", command=create_pet)
add_pet_button.pack(pady=20)

# --- Initial Pets ---
pets = [] # List to hold pet instances

# --- Start the Tkinter event loop ---
root.mainloop()
