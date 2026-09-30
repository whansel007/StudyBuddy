# Transcribes audio offline for work and pet listening
import tkinter as tk
import tkinterdnd2 as tkdnd
import os
from tkinter import filedialog
import comtypes
import comtypes.client
import threading


class ConvertWindow:
    def __init__(self, master, state_callback):
        # Change state callback function
        self.state_callback = state_callback

        tkdnd.TkinterDnD.require(master)
        
        self.notes = {}
        
        self.window = tk.Toplevel(master)
        self.window.title("Convert")
        self.window.config(padx=20, pady=20, bg="#f7f5dd")
        self.window.protocol("WM_DELETE_WINDOW", self.close_window)
        
        self.paths = []

        # UI SETUP ===
        self.label_windowTitle = tk.Label(
            self.window, 
            text="Convert", 
            bg="#f7f5dd", 
            font=("Comic Sans MS", 12, "bold")
        )
        self.label_windowTitle.pack(pady=(0, 10))
        
        self.label_windowSubTitle = tk.Label(
            self.window, 
            text="Convert MS PPT and Word files into PDFs", 
            bg="#f7f5dd", 
            font=("Comic Sans MS", 10, "bold")
        )
        self.label_windowSubTitle.pack(pady=(0, 10))

        self.file_count = tk.StringVar(value="No file selected")
        
        self.label_filePaths = tk.Label(
            self.window, 
            textvariable=self.file_count, 
            bg="#f7f5dd", 
            font=("Comic Sans MS", 10, "bold")
        )
        self.label_filePaths.pack(pady=(0, 10))
        
        self.drop_area = tk.Label(
            self.window,
            text="Drag ur files here :3",
            bg="#87EBD2",
            width=40,
            height=10,
            relief="groove",
            font=("Comic Sans MS", 10, "bold")
        )
        self.drop_area.pack(pady=10)
        
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
        
        self.drop_area.drop_target_register(tkdnd.DND_FILES)

        def on_drop(event):
            self.set_paths(self.window.tk.splitlist(event.data))
            print(type(self.paths))

        self.drop_area.dnd_bind("<<Drop>>", on_drop)
    
    # Functions ===
    def set_paths(self, paths):
        self.paths = paths
        self.file_count.set(f"{len(self.paths)} files(s) selected")

    def pick_file(self):
        paths = filedialog.askopenfilenames(
            title="Pick MS PPT or Word file to convert to PDF", 
            filetypes=[("All Files" , "*.*"),
                       ("MS PPT or Word", "*.ppt *.pptx *.doc *.docx"),
                       ("MS PPT","*.ppt *pptx"),("MS Word","*.doc *docx")])
        self.set_paths(paths)
        print(self.paths)
    
    def convert_picked(self):
        if not self.paths:
            print("List is empty!!!")
            return
        self.state_callback("work")
        threading.Thread(
            target=self._convert_worker,
            args=(tuple(self.paths),),
            daemon=True,
        ).start()

    def _convert_worker(self, paths):
        comtypes.CoInitialize()
        try:
            for in_path in paths:
                out_path = os.path.splitext(in_path)[0] + ".pdf"
                self.convert(
                    in_path=os.path.normpath(in_path),
                    out_path=os.path.normpath(out_path),
                )
        finally:
            comtypes.CoUninitialize()
            self.state_callback("idle")
            
    def convert(self, in_path, out_path):
        print(f"Converting {in_path}")
        
        last5 = in_path[-5:]
        print(last5)
        
        if ".doc" in last5:
            print("This is a WORD!")
            
            word = comtypes.client.CreateObject("Word.Application")
            # word.Visible = 0
            
            doc = word.Documents.Open(in_path)
            doc.SaveAs(out_path, 17)
            doc.Close()
            word.Quit()
            
            
        elif ".ppt" in last5:
            print("This is a PPT!")
            
            ppt = comtypes.client.CreateObject("Powerpoint.Application")
            # ppt.Visible = 0
            
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