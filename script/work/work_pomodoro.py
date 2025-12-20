import tkinter as tk
from tkinter import messagebox
import math

# --- CONSTANTS ---
PINK = "#e2979c"
RED = "#e7305b"
GREEN = "#9bdeac"
YELLOW = "#f7f5dd"
BLUE = "#87CEEB"
FONT_NAME = "Comic Sans MS"
WORK_MIN = 25
SHORT_BREAK_MIN = 5
LONG_BREAK_MIN = 20
DEFAULT_EARN_RATIO = 5

# --- GLOBAL STATE & SETTINGS ---
app_state = {
    "mode": "Classic",
    "break_budget_seconds": 0,
    "rounds": 0,
    "timer_id": None,
    "current_session": "idle",  # idle, work_down, work_up, break_down
}

timer_settings = {
    "Classic": {"work": WORK_MIN, "short_break": SHORT_BREAK_MIN, "long_break": LONG_BREAK_MIN},
    "Budget": {"earn_ratio": DEFAULT_EARN_RATIO}
}

# --- UI UPDATE ---
def update_ui_for_state():
    session = app_state["current_session"]
    mode = app_state["mode"]

    if mode == "Classic":
        check_marks.config(text="✔" * app_state["rounds"])
        start_button.config(text="Start Work", state="normal")
        if session == "idle":
            title_label.config(text="Timer", fg=GREEN)
    
    else:  # Budget Mode
        mins, secs = divmod(app_state["break_budget_seconds"], 60)
        check_marks.config(text=f"Budget: {int(mins):02d}:{int(secs):02d}")

        if session == "idle":
            title_label.config(text="Timer", fg=GREEN)
            if app_state["break_budget_seconds"] > 0:
                start_button.config(text="Start Break")
            else:
                start_button.config(text="Start Work")
        elif session == "work_up":
            start_button.config(text="Stop Work")
        elif session == "break_down":
            start_button.config(text="Stop Break")

# --- TIMER LOGIC ---

def handle_start_button():
    session = app_state["current_session"]
    mode = app_state["mode"]

    # Classic mode is simple
    if mode == "Classic":
        if session == "idle":
            app_state["rounds"] += 1
            title_label.config(text="Work", fg=RED)
            app_state["current_session"] = "work_down"
            count_down(timer_settings["Classic"]["work"] * 60)
        return

    # Budget mode state machine
    if session == "idle":
        if app_state["break_budget_seconds"] > 0: # Start a break
            app_state["current_session"] = "break_down"
            title_label.config(text="Break", fg=BLUE)
            update_ui_for_state()
            count_down(app_state["break_budget_seconds"])
        else: # Start work
            app_state["current_session"] = "work_up"
            title_label.config(text="Work", fg=RED)
            update_ui_for_state()
            count_up(0)
    elif session == "work_up": # Stop work
        window.after_cancel(app_state["timer_id"])
        app_state["current_session"] = "idle"
        # Finalize partial minute earnings
        total_seconds = int(timer_text_label.cget("text").replace(":", ""))
        if total_seconds % 60 != 0:
             # This logic can be enhanced for more granular earning, but for now we stop.
             pass
        update_ui_for_state()
        timer_text_label.config(text="00:00")
    elif session == "break_down": # Stop break
        window.after_cancel(app_state["timer_id"])
        app_state["current_session"] = "idle"
        mins, secs = map(int, timer_text_label.cget("text").split(":"))
        app_state["break_budget_seconds"] = mins * 60 + secs
        update_ui_for_state()
        timer_text_label.config(text="00:00")


def count_up(count_seconds):
    # Award break time every minute
    if count_seconds > 0 and count_seconds % 60 == 0:
        earned_seconds = 60 / timer_settings["Budget"]["earn_ratio"]
        app_state["break_budget_seconds"] += earned_seconds
        update_ui_for_state()

    minutes, secs = divmod(count_seconds, 60)
    timer_text_label.config(text=f"{int(minutes):02d}:{int(secs):02d}")
    app_state["timer_id"] = window.after(1000, count_up, count_seconds + 1)

def count_down(count_seconds):
    minutes, secs = divmod(count_seconds, 60)
    timer_text_label.config(text=f"{int(minutes):02d}:{int(secs):02d}")

    if count_seconds > 0:
        app_state["timer_id"] = window.after(1000, count_down, count_seconds - 1)
    else:
        session_type = app_state["current_session"]
        
        if session_type == "work_down": # Classic work session finished
            break_type = "long" if app_state["rounds"] % 4 == 0 else "short"
            break_seconds = timer_settings["Classic"][break_type] * 60
            title_label.config(text="Break", fg=PINK if break_type == "short" else BLUE)
            app_state["current_session"] = "break_down"
            count_down(break_seconds)
        
        elif session_type == "break_down": # Any break session finished
            # Automatically start the next work session
            if app_state["mode"] == "Budget":
                app_state["current_session"] = "work_up"
                title_label.config(text="Work", fg=RED)
                update_ui_for_state()
                count_up(0)
            else: # Classic mode
                app_state["rounds"] += 1
                app_state["current_session"] = "work_down"
                title_label.config(text="Work", fg=RED)
                update_ui_for_state()
                count_down(timer_settings["Classic"]["work"] * 60)
        
        else: # Fallback
            app_state["current_session"] = "idle"
            update_ui_for_state()

def reset_timer():
    if app_state["timer_id"]:
        window.after_cancel(app_state["timer_id"])
    
    app_state["rounds"] = 0
    app_state["timer_id"] = None
    app_state["current_session"] = "idle"
    app_state["break_budget_seconds"] = 0

    timer_text_label.config(text="00:00")
    update_ui_for_state()

# --- SETTINGS WINDOW ---
def open_settings_window():
    settings_window = tk.Toplevel(window)
    settings_window.title("Pomodoro Settings")
    settings_window.config(padx=20, pady=20, bg=YELLOW)
    settings_window.attributes('-topmost', True)
    settings_window.grab_set()

    mode_var = tk.StringVar(value=app_state["mode"])
    
    # Widgets that change based on mode
    work_entry = tk.Entry(settings_window, width=7)
    label_2 = tk.Label(settings_window, bg=YELLOW, font=(FONT_NAME, 12))
    entry_2 = tk.Entry(settings_window, width=7)
    label_3 = tk.Label(settings_window, bg=YELLOW, font=(FONT_NAME, 12))
    entry_3 = tk.Entry(settings_window, width=7)

    def configure_widgets_for_mode(*args):
        mode = mode_var.get()
        if mode == "Classic":
            # Configure and place classic widgets
            tk.Label(settings_window, text="Work (min):", bg=YELLOW, font=(FONT_NAME, 12)).grid(row=1, column=0, sticky="w", pady=2)
            work_entry.grid(row=1, column=1, sticky="e", pady=2)
            work_entry.delete(0, tk.END); work_entry.insert(0, timer_settings["Classic"]["work"])

            label_2.config(text="Short Break (min):"); label_2.grid(row=2, column=0, sticky="w", pady=2)
            entry_2.grid(row=2, column=1, sticky="e", pady=2)
            entry_2.delete(0, tk.END); entry_2.insert(0, timer_settings["Classic"]["short_break"])

            label_3.config(text="Long Break (min):"); label_3.grid(row=3, column=0, sticky="w", pady=2)
            entry_3.grid(row=3, column=1, sticky="e", pady=2)
            entry_3.delete(0, tk.END); entry_3.insert(0, timer_settings["Classic"]["long_break"])
        else: # Budget
            # Configure and place budget widgets
            tk.Label(settings_window, text="Earn Ratio (work mins per 1 min break):", bg=YELLOW, font=(FONT_NAME, 12)).grid(row=1, column=0, sticky="w", pady=2)
            work_entry.grid(row=1, column=1, sticky="e", pady=2)
            work_entry.delete(0, tk.END); work_entry.insert(0, timer_settings["Budget"]["earn_ratio"])
            
            # Hide others
            label_2.grid_remove(); entry_2.grid_remove()
            label_3.grid_remove(); entry_3.grid_remove()
            
    def save_and_close():
        new_mode = mode_var.get()
        try:
            if new_mode == "Classic":
                timer_settings["Classic"]["work"] = int(work_entry.get())
                timer_settings["Classic"]["short_break"] = int(entry_2.get())
                timer_settings["Classic"]["long_break"] = int(entry_3.get())
            else: # Budget
                timer_settings["Budget"]["earn_ratio"] = int(work_entry.get())
            
            if app_state["mode"] != new_mode:
                app_state["mode"] = new_mode
                reset_timer()
            
            settings_window.destroy()
        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter a valid integer.", parent=settings_window)

    tk.Radiobutton(settings_window, text="Classic", variable=mode_var, value="Classic", command=configure_widgets_for_mode, bg=YELLOW).grid(row=0, column=0)
    tk.Radiobutton(settings_window, text="Break Budget", variable=mode_var, value="Budget", command=configure_widgets_for_mode, bg=YELLOW).grid(row=0, column=1)
    
    configure_widgets_for_mode() # Initial setup

    tk.Button(settings_window, text="Save & Close", command=save_and_close).grid(row=4, column=0, columnspan=2, pady=10)

# --- UI SETUP ---
window = tk.Tk()
window.title("Pomodoro")
window.config(padx=25, pady=0, bg=YELLOW)
window.attributes('-topmost', True)

title_label = tk.Label(text="Timer", fg=GREEN, bg=YELLOW, font=(FONT_NAME, 50))
title_label.grid(column=0, row=0, columnspan=3, pady=5, sticky="ew")

timer_text_label = tk.Label(text="00:00", fg="white", bg=GREEN, font=(FONT_NAME, 35, "bold"))
timer_text_label.grid(column=0, row=1, columnspan=3, pady=20, ipady=10, ipadx=10, sticky="ew")

settings_button = tk.Button(text="Settings", highlightthickness=0, command=open_settings_window)
settings_button.grid(column=1, row=2, pady=10)

start_button = tk.Button(text="Start", highlightthickness=0, command=handle_start_button)
start_button.grid(column=0, row=3)

reset_button = tk.Button(text="Reset", highlightthickness=0, command=reset_timer)
reset_button.grid(column=2, row=3)

check_marks = tk.Label(fg=BLUE, bg=YELLOW, font=(FONT_NAME, 12, "bold"))
check_marks.grid(column=1, row=4, columnspan=3)

update_ui_for_state()
window.mainloop()
