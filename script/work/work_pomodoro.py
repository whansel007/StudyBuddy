import tkinter as tk
from tkinter import messagebox
import math

# ---------------------------- CONSTANTS ------------------------------- #
PINK = "#e2979c"
RED = "#e7305b"
GREEN = "#9bdeac"
YELLOW = "#f7f5dd"
BLUE = "#87CEEB" # A nice sky blue
FONT_NAME = "Courier"
WORK_MIN = 25
SHORT_BREAK_MIN = 5
LONG_BREAK_MIN = 20
reps = 0
timer = None

# ---------------------------- TIMER RESET ------------------------------- # 
def reset_timer():
    global reps
    window.after_cancel(timer)
    timer_text_label.config(text="00:00", bg=GREEN) # Reset background color
    title_label.config(text="Timer")
    check_marks.config(text="")
    reps = 0

# ---------------------------- TIMER MECHANISM ------------------------------- # 
def start_timer():
    global reps
    reps += 1
    try:
        work_min = int(work_entry.get())
        short_break_min = int(short_break_entry.get())
        long_break_min = int(long_break_entry.get())
    except ValueError:
        messagebox.showerror("Invalid Input", "Please enter valid integers for time settings.")
        return

    work_sec = work_min * 60
    short_break_sec = short_break_min * 60
    long_break_sec = long_break_min * 60

    if reps % 8 == 0:
        count_down(long_break_sec)
        title_label.config(text="Break", fg=RED)
        timer_text_label.config(bg=GREEN)
    elif reps % 2 == 0:
        count_down(short_break_sec)
        title_label.config(text="Break", fg=PINK)
        timer_text_label.config(bg=GREEN)
    else:
        count_down(work_sec)
        title_label.config(text="Work", fg=GREEN)
        timer_text_label.config(bg=BLUE)

# ---------------------------- COUNTDOWN MECHANISM ------------------------------- # 
def count_down(count):
    global timer
    count_min = math.floor(count / 60)
    count_sec = count % 60
    if count_sec < 10:
        count_sec = f"0{count_sec}"

    timer_text_label.config(text=f"{count_min}:{count_sec}")
    if count > 0:
        timer = window.after(1000, count_down, count - 1)
    else:
        start_timer()
        marks = ""
        work_sessions = math.floor(reps/2)
        for _ in range(work_sessions):
            marks += "✔"
        check_marks.config(text=marks)

# ---------------------------- UI SETUP ------------------------------- #
window = tk.Tk()
window.title("Pomodoro")
window.config(padx=10, pady=0, bg=YELLOW)

title_label = tk.Label(text="Timer", fg=GREEN, bg=YELLOW, font=(FONT_NAME, 50))
title_label.grid(column=1, row=0)

timer_text_label = tk.Label(text="00:00", fg="white", bg=GREEN, font=(FONT_NAME, 35, "bold")) # timer_text_label is now a child of window
timer_text_label.grid(column=1, row=1, pady=20) # Grid timer_text_label directly into window

# --- Entry fields for setting time ---
settings_frame = tk.Frame(window, bg=YELLOW)
settings_frame.grid(column=1, row=2, pady=10)

work_label = tk.Label(settings_frame, text="Work (min):", bg=YELLOW, font=(FONT_NAME, 12))
work_label.grid(column=0, row=0)
work_entry = tk.Entry(settings_frame, width=5)
work_entry.insert(0, WORK_MIN)
work_entry.grid(column=1, row=0)

short_break_label = tk.Label(settings_frame, text="Short Break (min):", bg=YELLOW, font=(FONT_NAME, 12))
short_break_label.grid(column=0, row=1)
short_break_entry = tk.Entry(settings_frame, width=5)
short_break_entry.insert(0, SHORT_BREAK_MIN)
short_break_entry.grid(column=1, row=1)

long_break_label = tk.Label(settings_frame, text="Long Break (min):", bg=YELLOW, font=(FONT_NAME, 12))
long_break_label.grid(column=0, row=2)
long_break_entry = tk.Entry(settings_frame, width=5)
long_break_entry.insert(0, LONG_BREAK_MIN)
long_break_entry.grid(column=1, row=2)


start_button = tk.Button(text="Start", highlightthickness=0, command=start_timer)
start_button.grid(column=0, row=3)

reset_button = tk.Button(text="Reset", highlightthickness=0, command=reset_timer)
reset_button.grid(column=2, row=3)

check_marks = tk.Label(fg=GREEN, bg=YELLOW)
check_marks.grid(column=1, row=4)

window.mainloop()
