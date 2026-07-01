# Transcribes audio offline for work and pet listening
import tkinter as tk
from tkinter import ttk, scrolledtext, filedialog
import json

class NotesWindow:
    def __init__(self, master, state_callback):
        # Change state callback function
        self.state_callback = state_callback
        
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
        self.frame_title.pack()    
        
        self.label_title = tk.Label(
            self.frame_title, 
            text="Title: ", 
            bg="#f7f5dd", 
            font=("Comic Sans MS", 12, "bold"))
        self.label_title.pack(side="left")
        
        self.combo_titles = ttk.Combobox(
            self.frame_title,
            width=40,
            font=("Comic Sans MS", 12),
            values=list(self.notes.keys()))
        self.combo_titles.bind("<<ComboboxSelected>>", lambda event: self.load_note())
        self.combo_titles.pack(side="right")
        

        # Text Content        
        self.text_content = scrolledtext.ScrolledText(
            self.window,
            width=60,
            height=10,
            font=("Comic Sans MS", 12),
            wrap="word",
        )
        self.text_content.pack(pady=(0, 10))
        
        # Text Buttons 
        self.frame_textButtons = tk.Frame(
            master=self.window)
        self.frame_textButtons.pack(pady=(5, 10))
        
        self.button_save = tk.Button(
            self.frame_textButtons, 
            text="Save Note", 
            command=self.save_note, 
            bg="#87EBB4", 
            font=("Comic Sans MS", 10), 
            padx=20,)
        self.button_save.pack(side="left", padx=5)

        self.button_clear = tk.Button(
            self.frame_textButtons, 
            text="Clear Text", 
            command=self.clear_text, 
            bg="#87CEEB", 
            font=("Comic Sans MS", 10), 
            padx=20,)
        self.button_clear.pack(side="left", padx=5)
        
        self.button_delete = tk.Button(
            self.frame_textButtons, 
            text="Delete Note", 
            command=self.delete_note, 
            bg="#EB8787", 
            font=("Comic Sans MS", 10), 
            padx=20,)
        self.button_delete.pack(side="right", padx=5)
        
        # File Buttons 
        self.frame_fileButtons = tk.Frame(
            master=self.window)
        self.frame_fileButtons.pack(pady=(5, 10))
        
        self.button_saveFile = tk.Button(
            self.frame_fileButtons, 
            text="Save File", 
            command=self.save_file, 
            bg="#EBBC87", 
            font=("Comic Sans MS", 10), 
            padx=20,)
        self.button_saveFile.pack(side="left", padx=5)

        self.button_loadFile = tk.Button(
            self.frame_fileButtons, 
            text="Load File", 
            command=self.load_file,
            bg="#DA87EB", 
            font=("Comic Sans MS", 10), 
            padx=20,)
        self.button_loadFile.pack(side="left", padx=5)
        
        # Call pet to be in work mode
        self.state_callback("work")
            
    
    # Functions ===
    def refresh_combo(self):
        self.combo_titles["values"] = list(self.notes.keys())
        print(f"New titles values = {self.combo_titles['values']}")
        
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
    
    def save_file(self):
        save_path = filedialog.asksaveasfilename(
            defaultextension=".json",
            filetypes=[("JSON", "*.json")]
        )
        
        if not save_path:
            return
            
        print(save_path)
        
        with open(save_path, "w", encoding="utf-8") as save_file:
            json.dump(self.notes, save_file, indent=4)
        
    def load_file(self):
        load_path = filedialog.askopenfilename(
            filetypes=[("JSON", "*.json")]
        )
        
        if not load_path:
            return
            
        print(load_path)
        
        with open(load_path, "r", encoding="utf-8") as load_file:
            self.notes = json.load(load_file)
        
        self.refresh_combo()
        
        # Auto-load the first note if available
        if self.notes:
            first_title = list(self.notes.keys())[0]
            self.combo_titles.set(first_title)
            self.load_note()
        
    def close_window(self):
        # The pet is now relieved from duty :V
        self.state_callback("idle")
        self.window.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = NotesWindow(root, lambda x : print(f"Called state callback to {x}") )
    root.mainloop()