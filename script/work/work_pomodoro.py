import tkinter as tk
from tkinter import messagebox
import math

class PomodoroTimer:
    def __init__(self, master):
        # UI Constant ====
        self.PINK = "#e2979c"
        self.RED = "#e7305b"
        self.GREEN = "#9bdeac"
        self.YELLOW = "#f7f5dd"
        self.BLUE = "#87CEEB"

        self.FONT_NAME = "Comic Sans MS"
        
        # Default Constant ===
        self.WORK_MIN = 25
        self.SHORT_BREAK_MIN = 5
        self.LONG_BREAK_MIN = 20
        self.EARN_RATIO = 5

        # Global Settings & State ===
        self.app_state = {
            "mode": "Classic",
            "rounds": 0,
            "break_budget_seconds": 0,
            "timer_id": None,
            "current_session": "idle",  # idle, work_down, work_up, break_down
        }

        self.timer_settings = {
            "Classic": {"work": self.WORK_MIN, 
                        "short_break": self.SHORT_BREAK_MIN, 
                        "long_break": self.LONG_BREAK_MIN},
            "Budget": {"earn_ratio": self.EARN_RATIO}
        }

        # --- UI SETUP ---
        self.window = tk.Toplevel(master)
        self.window.title("Pomodoro")
        self.window.config(padx=25, pady=0, bg=self.YELLOW)
        self.window.attributes('-topmost', True)

        self.title_label = tk.Label(self.window, text="Timer", fg=self.GREEN, bg=self.YELLOW, font=(self.FONT_NAME, 50))
        self.title_label.grid(column=0, row=0, columnspan=3, pady=5, sticky="ew")

        self.timer_text_label = tk.Label(self.window, text="00:00", fg="white", bg=self.GREEN, font=(self.FONT_NAME, 35, "bold"))
        self.timer_text_label.grid(column=0, row=1, columnspan=3, pady=20, ipady=10, ipadx=10, sticky="ew")

        self.settings_button = tk.Button(self.window, text="Settings", highlightthickness=0, command=self.open_settings_window)
        self.settings_button.grid(column=1, row=3, pady=10)

        self.start_button = tk.Button(self.window, text="Start", highlightthickness=0, command=self.handle_start_button)
        self.start_button.grid(column=2, row=3)

        self.reset_button = tk.Button(self.window, text="Reset", highlightthickness=0, command=self.reset_timer)
        self.reset_button.grid(column=0, row=3)

        self.check_marks = tk.Label(self.window, fg=self.BLUE, bg=self.YELLOW, font=(self.FONT_NAME, 12, "bold"))
        self.check_marks.grid(column=1, row=4, columnspan=1)

        self.update_ui_for_state()

    def update_ui_for_state(self):
        session = self.app_state["current_session"]
        mode = self.app_state["mode"]

        if mode == "Classic":
            self.check_marks.config(text="✔" * self.app_state["rounds"])
            self.start_button.config(text="Start Work", state="normal")
            if session == "idle":
                self.title_label.config(text="Timer", fg=self.GREEN)
        
        else:  # Budget Mode
            mins, secs = divmod(self.app_state["break_budget_seconds"], 60)
            self.check_marks.config(text=f"Budget: {int(mins):02d}:{int(secs):02d}")

            if session == "idle":
                self.title_label.config(text="Timer", fg=self.GREEN)
                if self.app_state["break_budget_seconds"] > 0:
                    self.start_button.config(text="Start Break", state="normal")
                else:
                    self.start_button.config(text="Start Work", state="normal")
            elif session == "work_up":
                self.start_button.config(text="Stop Work", state="normal")
            elif session == "break_down":
                self.start_button.config(text="Stop Break", state="normal")

    def handle_start_button(self):
        session = self.app_state["current_session"]
        mode = self.app_state["mode"]

        if mode == "Classic":
            if session == "idle":
                self.app_state["rounds"] += 1
                self.title_label.config(text="Work", fg=self.RED)
                self.app_state["current_session"] = "work_down"
                self.count_down(self.timer_settings["Classic"]["work"] * 60)
            return

        if session == "idle":
            if self.app_state["break_budget_seconds"] > 0:
                self.app_state["current_session"] = "break_down"
                self.title_label.config(text="Break", fg=self.BLUE)
                self.update_ui_for_state()
                self.count_down(self.app_state["break_budget_seconds"])
            else:
                self.app_state["current_session"] = "work_up"
                self.title_label.config(text="Work", fg=self.RED)
                self.update_ui_for_state()
                self.count_up(0)
        elif session == "work_up":
            if self.app_state["timer_id"]:
                self.window.after_cancel(self.app_state["timer_id"])
            self.app_state["current_session"] = "idle"
            self.update_ui_for_state()
            self.timer_text_label.config(text="00:00")
        elif session == "break_down":
            if self.app_state["timer_id"]:
                self.window.after_cancel(self.app_state["timer_id"])
            self.app_state["current_session"] = "idle"
            mins, secs = map(int, self.timer_text_label.cget("text").split(":"))
            self.app_state["break_budget_seconds"] = mins * 60 + secs
            self.update_ui_for_state()
            self.timer_text_label.config(text="00:00")

    def count_up(self, count_seconds):
        if count_seconds > 0 and count_seconds % 60 == 0:
            earned_seconds = 60 / self.timer_settings["Budget"]["earn_ratio"]
            self.app_state["break_budget_seconds"] += earned_seconds
            self.update_ui_for_state()

        minutes, secs = divmod(count_seconds, 60)
        self.timer_text_label.config(text=f"{int(minutes):02d}:{int(secs):02d}")
        self.app_state["timer_id"] = self.window.after(1000, self.count_up, count_seconds + 1)

    def count_down(self, count_seconds):
        minutes, secs = divmod(count_seconds, 60)
        self.timer_text_label.config(text=f"{int(minutes):02d}:{int(secs):02d}")

        if count_seconds > 0:
            self.app_state["timer_id"] = self.window.after(1000, self.count_down, count_seconds - 1)
        else:
            session_type = self.app_state["current_session"]
            
            if session_type == "work_down":
                break_type = "long" if self.app_state["rounds"] % 4 == 0 else "short"
                break_seconds = self.timer_settings["Classic"][break_type] * 60
                self.title_label.config(text="Break", fg=self.PINK if break_type == "short" else self.BLUE)
                self.app_state["current_session"] = "break_down"
                self.count_down(break_seconds)
            
            elif session_type == "break_down":
                self.app_state["current_session"] = "idle"
                self.update_ui_for_state()
                if self.app_state["mode"] == "Classic":
                    self.app_state["rounds"] += 1
                    self.app_state["current_session"] = "work_down"
                    self.title_label.config(text="Work", fg=self.RED)
                    self.update_ui_for_state()
                    self.count_down(self.timer_settings["Classic"]["work"] * 60)
            
            else:
                self.app_state["current_session"] = "idle"
                self.update_ui_for_state()

    def reset_timer(self):
        if self.app_state["timer_id"]:
            self.window.after_cancel(self.app_state["timer_id"])
        
        self.app_state["rounds"] = 0
        self.app_state["timer_id"] = None
        self.app_state["current_session"] = "idle"
        self.app_state["break_budget_seconds"] = 0

        self.timer_text_label.config(text="00:00")
        self.update_ui_for_state()

    def open_settings_window(self):
        settings_window = tk.Toplevel(self.window)
        settings_window.title("Pomodoro Settings")
        settings_window.config(padx=20, pady=20, bg=self.YELLOW)
        settings_window.attributes('-topmost', True)
        settings_window.grab_set() # Takes the focus to this window and the widgets in it

        # Mode Setting 
        mode_var = tk.StringVar(value=self.app_state["mode"])

        button_classic = tk.Radiobutton(settings_window, text="Classic", 
                                        variable=mode_var, value="Classic", 
                                        command=update_settings_entries, bg=self.YELLOW)
        button_classic.grid(row=0, column=0)

        button_budget = tk.Radiobutton(settings_window, text="Break Budget", 
                                       variable=mode_var, value="Budget", 
                                       command=update_settings_entries, bg=self.YELLOW)
        button_budget.grid(row=0, column=1)
        
        # Create 3 place holder text that we can change the content of easily
        label_1 = tk.Label(settings_window, bg=self.YELLOW, font=(self.FONT_NAME, 12))
        entry_1 = tk.Entry(settings_window, width=7)

        label_2 = tk.Label(settings_window, bg=self.YELLOW, font=(self.FONT_NAME, 12))
        entry_2 = tk.Entry(settings_window, width=7)

        label_3 = tk.Label(settings_window, bg=self.YELLOW, font=(self.FONT_NAME, 12))
        entry_3 = tk.Entry(settings_window, width=7)

        def update_settings_entries():
            # Get the current mode selected
            mode = mode_var.get()

            if mode == "Classic":
                label_1.config(text="Work (min):"); label_1.grid(row=1, column=0, sticky="w", pady=2)
                entry_1.grid(row=1, column=1, sticky="e", pady=2)
                entry_1.delete(0, tk.END); entry_1.insert(0, self.timer_settings["Classic"]["work"])

                label_2.config(text="Short Break (min):"); label_2.grid(row=2, column=0, sticky="w", pady=2)
                entry_2.grid(row=2, column=1, sticky="e", pady=2)
                entry_2.delete(0, tk.END); entry_2.insert(0, self.timer_settings["Classic"]["short_break"])

                label_3.config(text="Long Break (min):"); label_3.grid(row=3, column=0, sticky="w", pady=2)
                entry_3.grid(row=3, column=1, sticky="e", pady=2)
                entry_3.delete(0, tk.END); entry_3.insert(0, self.timer_settings["Classic"]["long_break"])

            else: # Budget
                label_1.config(text="Earn Ratio (work mins per 1 min break):"); label_1.grid(row=1, column=0, sticky="w", pady=2)
                entry_1.grid(row=1, column=1, sticky="e", pady=2)
                entry_1.delete(0, tk.END); entry_1.insert(0, self.timer_settings["Budget"]["earn_ratio"])
                
                # Removes the other labels we don't need
                label_2.grid_remove(); entry_2.grid_remove()
                label_3.grid_remove(); entry_3.grid_remove()
                
        def save_and_close():
            # Get the new mode chosen 
            new_mode = mode_var.get()

            try:
                if new_mode == "Classic":
                    self.timer_settings["Classic"]["work"] = int(entry_1.get())
                    self.timer_settings["Classic"]["short_break"] = int(entry_2.get())
                    self.timer_settings["Classic"]["long_break"] = int(entry_3.get())
                else: # Budget
                    self.timer_settings["Budget"]["earn_ratio"] = int(entry_1.get())
                
                if self.app_state["mode"] != new_mode:
                    self.app_state["mode"] = new_mode
                    self.reset_timer()
                
                settings_window.destroy() # Close the window

            except ValueError:
                messagebox.showerror("Invalid Input", "Please enter a valid integer.", parent=settings_window)
        
        update_settings_entries() # Initial update to the UI!

        tk.Button(settings_window, text="Save & Close", command=save_and_close).grid(row=4, column=0, columnspan=2, pady=10)

if __name__ == "__main__":
    root = tk.Tk()
    app = PomodoroTimer(root)
    root.mainloop()