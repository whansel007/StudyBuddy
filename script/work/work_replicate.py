# The pet can record your mouse and keyboard movements and replicate them
import time
import threading
from pynput import mouse, keyboard
import tkinter as tk
from tkinter import ttk, scrolledtext

class ReplicateWindow:
    def __init__(self, master, state_callback):
        # Change state callback function
        self.state_callback = state_callback
        self.state_callback("work")
        
        # Global list to store the recorded events
        self.recorded_events = []
        self.start_time = None
        self.playback_allowed = False
        self.already_running = False
        
        self.window = tk.Toplevel(master)
        self.window.title("Replicate")
        self.window.config(padx=20, pady=20, bg="#f7f5dd")
        self.window.attributes("-topmost", True)
        self.window.protocol("WM_DELETE_WINDOW", self.close_window)

        # UI SETUP ===
        self.frame_title = tk.Frame(
            master=self.window)
        self.frame_title.pack(pady=(5, 10))
        
        self.label_windowTitle = tk.Label(
            self.frame_title, 
            text="Replicate", 
            bg="#f7f5dd", 
            font=("Comic Sans MS", 12, "bold"))
        self.label_windowTitle.pack(pady=(0, 10))
        
        self.text_log = scrolledtext.ScrolledText(
            self.window,
            width=60,
            height=10,
            font=("Comic Sans MS", 10),
            wrap="word",
        )
        self.text_log.pack(pady=(0, 10))
        self.log("Record mouse and keyboard presses and play them back for a certain number of loops (press ESC to stop recording) :D")
        
        self.label_loop = tk.Label(
            self.window, 
            text="Number of loop(s): ", 
            bg="#f7f5dd", 
            font=("Comic Sans MS", 12, "bold"))
        self.label_loop.pack(side="left",pady=(0, 10))
        
        self.entry_loop = ttk.Entry(
            self.window, 
            width=5,
            font=("Comic Sans MS", 10))
        self.entry_loop.pack(side="left", pady=(0, 10))
        
        self.button_start = tk.Button(
            self.window, 
            text="Start Recording & Playback", 
            command=self.start_recording, 
            bg="#87EBB4", 
            font=("Comic Sans MS", 10), 
            padx=20,)
        self.button_start.pack(side="right", padx=5)
    
    # Time ===
    def get_elapsed_time(self):
        if self.start_time is None:
            self.start_time = time.time()
            return 0
        return time.time() - self.start_time
      
    # Events ===
    def on_move(self, x, y):
        # Not needed for now, unless we figure out how to drag
        # event = {
        #     "type": "mouse_move", 
        #     "x": x, 
        #     "y": y, 
        #     "time": self.get_elapsed_time()}
        # self.log(event)
        # self.recorded_events.append(event)
        pass

    def on_click(self, x, y, button, pressed):
        if pressed:
            event = {
                "type": "mouse_click", 
                "x": x, 
                "y": y, 
                "button": str(button), 
                "time": self.get_elapsed_time()
            }
            self.log(str(event))
            self.recorded_events.append(event)

    def on_press(self, key):
        try:
            key_val = key.char  # Normal keys (letters, numbers)
        except AttributeError:
            key_val = str(key)  # Special keys (space, enter, ctrl)
            
        # Stop recording if we press the Escape key
        if key == keyboard.Key.esc:
            return False
        
        event = {
            "type": "key_press", 
            "key": key_val, 
            "time": self.get_elapsed_time()
        }
        self.log(str(event))
        self.recorded_events.append(event)
    
    # Recording ===
    def start_recording(self):
        self.playback_allowed = False
        
        if not self.already_running:
            self.playback_allowed = True
            self.already_running = True
            threading.Thread(target=self.recording_worker, daemon=True).start()

    def recording_worker(self):
        self.log("Recording started... :0")
        self.log("Press 'ESC' on your keyboard to STOP recording.")

        self.mouse_listener = mouse.Listener(
            on_move=self.on_move, 
            on_click=self.on_click)
        
        self.keyboard_listener = keyboard.Listener(
            on_press=self.on_press)

        # Start listener
        self.mouse_listener.start()
        self.keyboard_listener.start()
        
        # Keep the main thread alive until keyboard listener stops (ESC pressed)
        self.keyboard_listener.join()
        self.mouse_listener.stop()
        
        self.log(f"Recording stopped!!!!\nCaptured {len(self.recorded_events)} event(s)")
        
        total_loops = int(self.entry_loop.get())
        self.log(f"User entered {total_loops} loop(s)")
        
        for i in range(3, -1, -1):
            self.log(f"Playback starting in {i} seconds!")
            time.sleep(1)
        
        self.playback_macro(loops=total_loops)
        
    # Playback ===
    def playback_macro(self, loops=3):
        # Enable the abortion escape option
        threading.Thread(target=self.enable_abortion, daemon=True).start()
        
        self.log(f"\n!!! Starting playback !!! \nWill repeat {loops} time(s)")
        mouse_controller = mouse.Controller()
        keyboard_controller = keyboard.Controller()
        
        for i in range(loops):
            self.log(f"==> Loop {i+1}/{loops}...")
            last_time = 0
            
            for event in self.recorded_events:
                
                # Stop playback if false
                if not self.playback_allowed:
                    return
                
                # Maintain the original timing/delay between actions
                time.sleep(max(0, event["time"] - last_time))
                last_time = event["time"]
                
                if event["type"] == "mouse_click":
                    mouse_controller.position = (event["x"], event["y"])
                    # Extract button type (e.g., Button.left)
                    btn = mouse.Button.left if "left" in event["button"] else mouse.Button.right
                    mouse_controller.click(btn)
                    
                elif event["type"] == "key_press":
                    # Handle special keys vs normal keys
                    if "Key." in event["key"]:
                        k = getattr(keyboard.Key, event["key"].split(".")[1])
                    else:
                        k = event["key"]
                    
                    try:
                        keyboard_controller.press(k)
                        keyboard_controller.release(k)
                    except Exception as e:
                        self.log(f"Error playing key {k}: {e}")
                        
        self.log("Playback finished! :D")
        self.already_running = False
        self.abortion_listener.stop()
            
    # Emergency abortion ===
    def enable_abortion(self):
        self.abortion_listener = keyboard.Listener(
            on_press=self.check_abortion)
        self.abortion_listener.start()
        
    def check_abortion(self, key):
        # Stop recording if we press the Escape key
        if key == keyboard.Key.esc:
            self.abortion_listener.stop()
            self.log("ABORTING THE MISSION!!!")
            self.close_window()
    
    # UI Handling ===
    def log(self, text):
        self.text_log.insert(tk.END, text + "\n")
        self.text_log.see(tk.END)
    
    def close_window(self):
        # The pet is now relieved from duty :V
        self.state_callback("idle")
        self.playback_allowed = False
        self.already_running = False
        self.window.destroy()
    
# Main execution
if __name__ == "__main__":
    root = tk.Tk()
    app = ReplicateWindow(root, lambda x : print(f"Called state callback to {x}"))
    root.mainloop()
    