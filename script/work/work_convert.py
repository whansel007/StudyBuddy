# Transcribes audio offline for work and pet listening
import tkinter as tk
import os
from tkinter import filedialog
import comtypes.client

class ConvertWindow:
    def __init__(self, master, state_callback):
        # Change state callback function
        self.state_callback = state_callback
        
        self.notes = {}
        
        self.window = tk.Toplevel(master)
        self.window.title("Convert")
        self.window.config(padx=20, pady=20, bg="#f7f5dd")
        self.window.attributes("-topmost", True)
        self.window.protocol("WM_DELETE_WINDOW", self.close_window)

        self.paths = []

        # UI SETUP ===
        self.label_windowTitle = tk.Label(
            self.window, 
            text="Convert", 
            bg="#f7f5dd", 
            font=("Comic Sans MS", 12, "bold"))
        self.label_windowTitle.pack(pady=(0, 10))
        
        self.label_windowSubTitle = tk.Label(
            self.window, 
            text="Convert MS PPT and Word files into PDFs", 
            bg="#f7f5dd", 
            font=("Comic Sans MS", 10, "bold"))
        self.label_windowSubTitle.pack(pady=(0, 10))
        
        self.button_pickFiles = tk.Button(
            self.window,
            text="Pick file(s)", 
            command= self.pick_file,  
            bg="#87EBB4", 
            font=("Comic Sans MS", 10), 
            padx=20,
        )
        self.button_pickFiles.pack(pady=10)
        
        self.button_convert = tk.Button(
            self.window,
            text="Convert", 
            command=self.convert_picked, 
            bg="#EBE187", 
            font=("Comic Sans MS", 10), 
            padx=20,
        ) 
        self.button_convert.pack(pady=10)
    
    # Functions ===
    def pick_file(self):
        self.paths = filedialog.askopenfilenames(
            title="Pick MS PPT or Word file to convert to PDF", 
            filetypes=[("All Files" , "*.*"),
                       ("MS PPT or Word", "*.ppt *.pptx *.doc *.docx"),
                       ("MS PPT","*.ppt *pptx"),("MS Word","*.doc *docx")])
        print(self.paths)
    
    def convert_picked(self):
        if not self.paths:
            print("List is empty!!!")
            return
        
        for in_path in self.paths:
            out_path = ".".join(in_path.split(".")[:-1]) + ".pdf"
            self.convert(
                in_path=os.path.normpath(in_path),
                out_path=os.path.normpath(out_path)
            )
        
    def convert(self, in_path, out_path):
        print(f"Converting {in_path}")
        
        last5 = in_path[-5:]
        print(last5)
        
        if ".doc" in last5:
            print("This is a WORD!")
            
            word = comtypes.client.CreateObject("Word.Application")
            word.Visible = 1
            
            doc = word.Documents.Open(in_path)
            doc.SaveAs(out_path, 17)
            doc.Close()
            word.Quit()
            
            
        elif ".ppt" in last5:
            print("This is a PPT!")
            
            ppt = comtypes.client.CreateObject("Powerpoint.Application")
            ppt.Visible = 1
            
            deck = ppt.Presentations.Open(in_path)
            deck.SaveAs(out_path, 32)
            deck.Close()
            ppt.Quit()
            
        else:
            print("Dunno what this is :/")
            return
        
        print(f"Result: {out_path}")
    
    def close_window(self):
        # The pet is now relieved from duty :V
        self.state_callback("idle")
        self.window.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = ConvertWindow(root, lambda x : print(f"Called state callback to {x}") )
    root.mainloop()