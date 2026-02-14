import tkinter as tk
from tkinter import ttk

class SpeechBubble:
    def __init__(self, master, text, x, y, duration=5000, animate_dots=False):
        self.window = tk.Toplevel(master)
        self.window.overrideredirect(True)
        self.window.attributes('-topmost', True)
        
        # Style
        bg_color = "#FFFFFF"
        font = ("Comic Sans MS", 10)
        
        self.text = text
        self.animate_dots = animate_dots
        self.dot_count = 1
        self.anim_after_id = None

        self.label = tk.Label(self.window, text=text, bg=bg_color, fg="black", 
                              font=font, padx=10, pady=5, relief="solid", borderwidth=1,
                              wraplength=200, justify="left")
        self.label.pack()
        
        # Position it above the pet
        self.window.update_idletasks()
        width = self.window.winfo_width()
        height = self.window.winfo_height()
        
        # Center the bubble horizontally above the pet
        pos_x = x - (width // 2) + 62 # 62 is roughly half of 125 (pet size)
        pos_y = y - height - 10
        
        self.window.geometry(f"+{int(pos_x)}+{int(pos_y)}")
        
        # Start animation if requested
        if self.animate_dots:
            self.animate()

        # Auto-close
        self.after_id = self.window.after(duration, self.close)

    def animate(self):
        if not self.window.winfo_exists():
            return
        
        dots = "." * self.dot_count
        self.label.config(text=dots)
        self.dot_count = (self.dot_count % 3) + 1
        self.anim_after_id = self.window.after(500, self.animate)

    def close(self):
        try:
            if self.anim_after_id:
                self.window.after_cancel(self.anim_after_id)
            if self.after_id:
                self.window.after_cancel(self.after_id)
                self.after_id = None
            self.window.destroy()
        except Exception:
            pass

class ChatWindow:
    def __init__(self, master, pet_name, on_send_callback):
        self.window = tk.Toplevel(master)
        self.window.title(f"Talk to {pet_name}")
        self.window.config(padx=20, pady=20, bg="#f7f5dd")
        self.window.attributes('-topmost', True)
        
        # The function to execute when the send button is clicked
        self.on_send_callback = on_send_callback
        
        self.label_message = tk.Label(self.window, text=f"What do you want to say to {pet_name}?",bg="#f7f5dd", font=("Comic Sans MS", 12, "bold"))
        self.label_message.pack(pady=(0, 10))
        
        self.entry_message = tk.Entry(self.window, width=40, font=("Comic Sans MS", 10))
        self.entry_message.pack(pady=10)
        self.entry_message.bind("<Return>", lambda e: self.send())
        self.entry_message.focus_set()
        
        self.button_send = tk.Button(self.window, text="Send", command=self.send, bg="#9bdeac", font=("Comic Sans MS", 10), padx=20)
        self.button_send.pack()

    def send(self):
        message = self.entry_message.get()
        
        if message.strip():
            self.on_send_callback(message)
            self.window.destroy()
