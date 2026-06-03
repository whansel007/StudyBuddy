import time
import json
from pynput import mouse, keyboard

# Global list to store the recorded events
recorded_events = []
start_time = None

def get_elapsed_time():
    global start_time
    if start_time is None:
        start_time = time.time()
        return 0
    return time.time() - start_time

# --- RECORDING FUNCTIONS ---
def on_move(x, y):
    # Optional: Un-comment the line below if you want to record pure mouse movement
    # recorded_events.append({"type": "mouse_move", "x": x, "y": y, "time": get_elapsed_time()})
    pass

def on_click(x, y, button, pressed):
    if pressed:
        recorded_events.append({
            "type": "mouse_click", 
            "x": x, 
            "y": y, 
            "button": str(button), 
            "time": get_elapsed_time()
        })

def on_press(key):
    try:
        key_val = key.char  # Normal keys (letters, numbers)
    except AttributeError:
        key_val = str(key)  # Special keys (space, enter, ctrl)
        
    # Stop recording if we press the Escape key
    if key == keyboard.Key.esc:
        return False
        
    recorded_events.append({
        "type": "key_press", 
        "key": key_val, 
        "time": get_elapsed_time()
    })

# --- PLAYBACK FUNCTION ---
def playback_macro(loops=3):
    print(f"\n🚀 Starting playback! Will repeat {loops} times.")
    mouse_controller = mouse.Controller()
    keyboard_controller = keyboard.Controller()
    
    for i in range(loops):
        print(f"🔄 Loop {i+1}/{loops}...")
        last_time = 0
        
        for event in recorded_events:
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
                    print(f"Error playing key {k}: {e}")
                    
    print("✅ Playback finished!")

# --- MAIN EXECUTION ---
if __name__ == "__main__":
    print("🔴 Recording started...")
    print("Press 'ESC' on your keyboard to STOP recording.")
    
    # Start listeners
    mouse_listener = mouse.Listener(on_move=on_move, on_click=on_click)
    keyboard_listener = keyboard.Listener(on_press=on_press)
    
    mouse_listener.start()
    keyboard_listener.start()
    
    # Keep the main thread alive until keyboard listener stops (ESC pressed)
    keyboard_listener.join()
    mouse_listener.stop()
    
    print(f"⏹️ Recording stopped. Captured {len(recorded_events)} events.")
    
    # Ask the user how many times to repeat
    try:
        repeat_count = int(input("How many times should the bot replicate these steps? "))
        print("Get ready... Playback starts in 3 seconds!")
        time.sleep(3)
        playback_macro(loops=repeat_count)
    except ValueError:
        print("Please enter a valid number next time.")