import tkinter as tk
from pet_ui import Pet

# Pet Creation
def create_pet(input_x, input_y):
    new_pet = Pet(root, x_pos=input_x, y_pos=input_y)
    pets.append(new_pet)

# Main window
root = tk.Tk()
root.title("Settings")
root.geometry("200x200")

tk.Label(root, text="X position").pack(anchor="w", padx=6)
xpos_entry = tk.Entry(root)
xpos_entry.pack(fill="x", padx=6)

tk.Label(root, text="Y position").pack(anchor="w", padx=6)
ypos_entry = tk.Entry(root)
ypos_entry.pack(fill="x", padx=6)

add_pet_button = tk.Button(root, text="Add Pet", command= lambda : create_pet(xpos_entry.get(), ypos_entry.get()))
add_pet_button.pack(pady=20)


pets = [] # List to hold pet instances

# Start the Tkinter event loop 
root.mainloop()
