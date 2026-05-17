# Transcribes audio offline for work and pet listening
import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext

class NotesWindow:
    def __init__(self, master, state_callback):
        # Change state callback function
        # self.state_callback = state_callback
        
        self.notes = {}
        
        self.window = tk.Toplevel(master)
        self.window.title("Notes")
        self.window.config(padx=20, pady=20, bg="#f7f5dd")
        self.window.attributes("-topmost", True)
        self.window.protocol("WM_DELETE_WINDOW", self.close_window)

        # UI SETUP ===
        self.label_windowTitle = tk.Label(
            self.window, 
            text="Notes", 
            bg="#f7f5dd", 
            font=("Comic Sans MS", 12, "bold"))
        self.label_windowTitle.pack(pady=(0, 10))
        
        # Title Selection
        self.frame_title = tk.Frame(
            master=self.window)
        
        self.label_title = tk.Label(
            self.frame_title, 
            text="Title: ", 
            bg="#f7f5dd", 
            font=("Comic Sans MS", 10, "bold"))
        
        self.combo_titles = ttk.Combobox(
            self.frame_title,
            width=40,
            font=("Comic Sans MS", 10),
            values=list(self.notes.keys()))
        self.combo_titles.bind("<<ComboboxSelected>>", lambda event: self.load_note())
        
        self.label_title.pack(side="left")
        self.combo_titles.pack(side="right")
        self.frame_title.pack()    

        # Text Content        
        self.text_content = scrolledtext.ScrolledText(
            self.window,
            width=60,
            height=10,
            font=("Comic Sans MS", 12),
            wrap="word",
        )
        self.text_content.pack(pady=(0, 10))
        
        # Buttons 
        self.frame_buttons = tk.Frame(
            master=self.window)
        
        self.button_save = tk.Button(
            self.frame_buttons, 
            text="Save Note", 
            command=self.save_note, 
            bg="#87EBB4", 
            font=("Comic Sans MS", 10), 
            padx=20,)

        self.button_clear = tk.Button(
            self.frame_buttons, 
            text="Clear Text", 
            command=self.clear_text, 
            bg="#87CEEB", 
            font=("Comic Sans MS", 10), 
            padx=20,)
        
        self.button_delete = tk.Button(
            self.frame_buttons, 
            text="Delete Note", 
            command=self.delete_note, 
            bg="#EB8787", 
            font=("Comic Sans MS", 10), 
            padx=20,)
        
        self.button_save.pack(side="left", padx=5)
        self.button_clear.pack(side="left", padx=5)
        self.button_delete.pack(side="right", padx=5)
        self.frame_buttons.pack(pady=(5, 10))
    
    # Functions ===
    def refresh_combo(self):
        self.combo_titles["values"] = list(self.notes.keys())
        print(f"New titles values = {self.combo_titles["values"]}")
        
    def load_note(self):
        title = self.combo_titles.get()
        content = self.notes.get(title)
        
        self.text_content.delete("1.0", tk.END)
        self.text_content.insert(tk.END, content)
    
    def save_note(self):
        new_title = self.combo_titles.get()
        new_content = self.text_content.get("1.0", tk.END)
        
        self.notes[new_title] = new_content
        print(self.notes)
        
        self.refresh_combo()
        self.combo_titles.set(new_title)
    
    def delete_note(self):
        removed_title = self.combo_titles.get()
        
        removed_note = self.notes.pop(removed_title)
        print(f"Removed note : {removed_note}")
        self.text_content.delete("1.0", tk.END)
        
        self.refresh_combo()
    
    def clear_text(self):
        self.text_content.delete("1.0", tk.END)
           
    def close_window(self):
        # self.state_callback("idle")
        self.window.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = NotesWindow(root,None)
    root.mainloop()