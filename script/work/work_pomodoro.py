import tkinter as tk
from tkinter import messagebox
import math

class PomodoroTimer:
    def __init__(self, master, work_callback, state_callback):
        # UI Constant 
        self.PINK = "#e2979c"
        self.RED = "#e7305b"
        self.GREEN = "#9bdeac"
        self.YELLOW = "#f7f5dd"
        self.BLUE = "#87CEEB"

        self.FONT_NAME = "Comic Sans MS"
        
        # Default Constant 
        self.WORK_MIN = 25
        self.SHORT_BREAK_MIN = 5
        self.LONG_BREAK_MIN = 20
        self.EARN_RATIO = 5

        # Callbacks 
        self.work_callback = work_callback
        self.state_callback = state_callback

        # Global Settings & State 
        self.mode = "Classic"
        self.session = "idle"
        self.rounds = 0

        self.main_timer = 0

        self.budget = 0
        self.coins = 0

        self.timer_settings = {
            "Classic": {"work": self.WORK_MIN, 
                        "short break": self.SHORT_BREAK_MIN, 
                        "long break": self.LONG_BREAK_MIN},
            "Budget": {"earn ratio": self.EARN_RATIO}
        }

        # UI Setup 
        self.window = tk.Toplevel(master)
        self.window.title("Pomodoro")
        self.window.config(padx=25, pady=0, bg=self.YELLOW)
        self.window.attributes('-topmost', True)
        self.window.protocol("WM_DELETE_WINDOW", self.close_pomodoro)

        self.label_title = tk.Label(self.window, text="Timer", fg=self.GREEN, bg=self.YELLOW, font=(self.FONT_NAME, 50))
        self.label_title.grid(column=0, row=0, columnspan=3, pady=5, sticky="ew")

        self.label_timer = tk.Label(self.window, text="00:00", fg="white", bg=self.GREEN, font=(self.FONT_NAME, 35, "bold"))
        self.label_timer.grid(column=0, row=1, columnspan=3, pady=20, ipady=10, ipadx=10, sticky="ew")

        self.button_settings = tk.Button(self.window, text="Settings", highlightthickness=0, command=self.open_settings_window)
        self.button_settings.grid(column=2, row=3, pady=10)

        self.button_start = tk.Button(self.window, text="Start", highlightthickness=0, command=self.handle_start_button)
        self.button_start.grid(column=1, row=3)

        self.buttonn_reset = tk.Button(self.window, text="Reset", highlightthickness=0, command=self.reset_timer)
        self.buttonn_reset.grid(column=0, row=3)

        self.label_extra = tk.Label(self.window, fg=self.BLUE, bg=self.YELLOW, font=(self.FONT_NAME, 12, "bold"))
        self.label_extra.grid(column=0, row=4, columnspan=2)
        
        self.label_coin = tk.Label(self.window, text="Coin gained : 0",fg=self.GREEN, bg=self.YELLOW, font=(self.FONT_NAME, 12, "bold"))
        self.label_coin.grid(column=0, row=5, columnspan=2)

        self.button_cashout = tk.Button(self.window, text="Cash out", highlightthickness=0, command=self.cash_out)
        self.button_cashout.grid(column=2, row=5)

        self.update_ui()  # Initial UI initialization 

    def update_ui(self):
        # Timer title 
        if self.session == "idle":
            self.label_title.config(text="Timer", fg=self.GREEN)
            self.button_start.config(text="Start")
        elif self.session == "work":
            self.label_title.config(text="Work", fg=self.RED)
            self.button_start.config(text="Finish Work")
        elif self.session == "break":
            self.label_title.config(text="Break", fg=self.BLUE)
            self.button_start.config(text="Finish Break")
        elif self.session == "long break":
            self.label_title.config(text="Long Break", fg=self.BLUE)
            self.button_start.config(text="Finish Long Break")
        
        # Timer count
        main_mins, main_secs = divmod(self.main_timer, 60)
        self.label_timer.config(text=f"{int(main_mins):02d}:{int(main_secs):02d}")

        #  Extra Label UI
        if self.mode == "Classic":
            self.label_extra.config(text=f"Work completed: {math.floor(self.rounds)}")
        else:  # Budget Mode
            budget_mins, budget_secs = divmod(self.budget, 60)
            self.label_extra.config(text=f"Budget: {int(budget_mins):02d}:{int(budget_secs):02d}")
        
        self.label_coin.config(text=f"Coin gained : {self.coins}")

    def handle_start_button(self):
        # Classic mode button logic 
        if self.mode == "Classic":
            
            # work --> break / long break
            if self.session == "work":
                self.rounds += 0.5
                # Long break for every 4th break
                if math.floor(self.rounds) % 4 == 0:
                    self.session = "long break"
                    self.main_timer = self.timer_settings["Classic"]["long break"] * 60
                # Regular break otherwise 
                else: 
                    self.session = "break"
                    self.main_timer = self.timer_settings["Classic"]["short break"] * 60

                self.count_down(self.rounds) 

            # idle / break / long break --> work
            else: 
                self.rounds += 0.5
                self.session = "work"
                self.main_timer = self.timer_settings["Classic"]["work"] * 60
                self.count_down(self.rounds) 

        # Budget mode button logic 
        else: 
            # work --> break 
            if self.session == "work":
                self.rounds += 0.5
                self.session = "break"
                self.main_timer = self.budget
                self.count_down(self.rounds) 

            # idle / break --> work
            else: 
                self.rounds += 0.5
                self.session = "work"
                self.main_timer = 0
                self.count_up(self.rounds) 
        self.update_ui()
        
        # Sync pet state
        if self.session == "work":
            self.state_callback("work")
        else:
            self.state_callback("idle")
    
    def count_up(self, initial_round):
        # When timer is reset to idle session, terminate the function
        if self.session == "idle":
            return
        
        # Only execute the same initial round to prevent count functions from other rounds leaking
        if self.rounds == initial_round: 
            self.main_timer += 1
            self.budget = self.main_timer // (self.timer_settings["Budget"]["earn ratio"])

            # Award coin every minute
            if self.main_timer % 60 == 0:
                self.coins += 1

            self.update_ui()

            self.window.after(1000, lambda : self.count_up(initial_round))
    
    def count_down(self, initial_round):
       # When timer is reset to idle session, terminate the function
        if self.session == "idle":
           return

        if self.main_timer <= 0:
           messagebox.showwarning("POMODORO TIME OUT!", "The pomodoro timer has hit 0!", parent=self.window)
           return
       
       # Only execute the same initial round to prevent count functions from other rounds leaking
        if self.rounds == initial_round: 
           self.main_timer -= 1

           if self.mode == "Budget":
               self.budget -= 1
           
           # Award coin every minute during work session
           if self.session == "work" and self.main_timer % 60 == 0:
               self.coins += 1
           
           self.update_ui()

           self.window.after(1000, lambda : self.count_down(initial_round))

    def reset_timer(self):
        self.rounds = 0
        self.session = "idle"
        self.main_timer = 0
        self.budget = 0
        self.coins = 0

        self.label_timer.config(text="00:00")
        self.update_ui()
        self.state_callback("idle")

    def cash_out(self):
        if self.coins > 0:
            self.work_callback(self.coins)
            self.coins = 0
            self.update_ui()
            messagebox.showinfo("Cash Out", "Coins transferred to your inventory!", parent=self.window)
        else:
            messagebox.showinfo("Cash Out", "No coins to cash out!", parent=self.window)
        
    def close_pomodoro(self):
        self.cash_out()
        self.state_callback("idle")
        self.window.destroy()

    def open_settings_window(self):
        settings_window = tk.Toplevel(self.window)
        settings_window.title("Pomodoro Settings")
        settings_window.config(padx=20, pady=20, bg=self.YELLOW)
        settings_window.attributes('-topmost', True)
        settings_window.grab_set() # Takes the focus to this window and the widgets in it

        # The mode variable for the setting window to not conflict with current active mode
        mode_var = tk.StringVar(value=self.mode)

        def update_settings_entries():
            if mode_var.get() == "Classic":
                label_1.config(text="Work (min):"); label_1.grid(row=1, column=0, sticky="w", pady=2)
                entry_1.grid(row=1, column=1, sticky="e", pady=2)
                entry_1.delete(0, tk.END); entry_1.insert(0, self.timer_settings["Classic"]["work"])

                label_2.config(text="Short Break (min):"); label_2.grid(row=2, column=0, sticky="w", pady=2)
                entry_2.grid(row=2, column=1, sticky="e", pady=2)
                entry_2.delete(0, tk.END); entry_2.insert(0, self.timer_settings["Classic"]["short break"])

                label_3.config(text="Long Break (min):"); label_3.grid(row=3, column=0, sticky="w", pady=2)
                entry_3.grid(row=3, column=1, sticky="e", pady=2)
                entry_3.delete(0, tk.END); entry_3.insert(0, self.timer_settings["Classic"]["long break"])

            else: # Budget
                label_1.config(text="Earn Ratio (work mins per 1 min break):"); label_1.grid(row=1, column=0, sticky="w", pady=2)
                entry_1.grid(row=1, column=1, sticky="e", pady=2)
                entry_1.delete(0, tk.END); entry_1.insert(0, self.timer_settings["Budget"]["earn ratio"])
                
                # Removes the other labels we don't need
                label_2.grid_remove(); entry_2.grid_remove()
                label_3.grid_remove(); entry_3.grid_remove()
                
        def save_and_close():
            # Get the new mode chosen 
            new_mode = mode_var.get()

            try:
                if new_mode == "Classic":
                    self.timer_settings["Classic"]["work"] = int(entry_1.get())
                    self.timer_settings["Classic"]["short break"] = int(entry_2.get())
                    self.timer_settings["Classic"]["long break"] = int(entry_3.get())
                else: # Budget
                    self.timer_settings["Budget"]["earn ratio"] = int(entry_1.get())
                
                # Only reset timer if it's a different mode, otherwise the changes will be applied next session
                if self.mode != new_mode:
                    self.mode = new_mode
                    self.reset_timer()
                
                settings_window.destroy() # Close the window

            except ValueError:
                messagebox.showerror("Invalid Input", "Please enter a valid integer.", parent=settings_window)

        # Mode Setting 

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

        update_settings_entries() # Initial update to the UI!

        button_save = tk.Button(settings_window, text="Save & Close", command=save_and_close)
        button_save.grid(row=4, column=0, columnspan=2, pady=10)

if __name__ == "__main__":
    root = tk.Tk()
    app = PomodoroTimer(root)
    root.mainloop()