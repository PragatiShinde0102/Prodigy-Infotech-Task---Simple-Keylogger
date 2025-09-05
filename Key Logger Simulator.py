import tkinter as tk
from tkinter import messagebox, scrolledtext
import datetime
import os

class KeyLoggerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Ethical Keylogger (Internship Project)")
        self.root.geometry("600x500")
        self.root.config(bg="#1E1E2F")

        self.logging = False
        self.log_file = "key_log.txt"
        self.key_count = 0

        # Title
        title = tk.Label(root, text="🔑 Ethical Keystroke Logger",
                         font=("Arial", 18, "bold"), bg="#1E1E2F", fg="cyan")
        title.pack(pady=10)

        # Info
        info = tk.Label(root, text="Type inside the box below.\n"
                                   "Click 'Start Logging' to begin recording.\n"
                                   "Click 'Stop Logging' to save logs.\n"
                                   "You can also View or Clear logs.",
                        font=("Arial", 11), bg="#1E1E2F", fg="lightgray")
        info.pack(pady=5)

        # Text area
        self.text_area = scrolledtext.ScrolledText(root, height=12, width=65, font=("Consolas", 12))
        self.text_area.pack(pady=10)

        # Keystroke counter
        self.counter_label = tk.Label(root, text="Keystrokes Logged: 0",
                                      font=("Arial", 12, "bold"), bg="#1E1E2F", fg="yellow")
        self.counter_label.pack(pady=5)

        # Buttons frame
        btn_frame = tk.Frame(root, bg="#1E1E2F")
        btn_frame.pack(pady=10)

        self.start_btn = tk.Button(btn_frame, text="▶ Start Logging", 
                                   command=self.start_logging, bg="#4CAF50", fg="white", width=15)
        self.start_btn.grid(row=0, column=0, padx=8)

        self.stop_btn = tk.Button(btn_frame, text="⏹ Stop Logging", 
                                  command=self.stop_logging, bg="#F44336", fg="white", width=15, state=tk.DISABLED)
        self.stop_btn.grid(row=0, column=1, padx=8)

        self.view_btn = tk.Button(btn_frame, text="📂 View Logs", 
                                  command=self.view_logs, bg="#2196F3", fg="white", width=15)
        self.view_btn.grid(row=0, column=2, padx=8)

        self.clear_btn = tk.Button(btn_frame, text="🗑 Clear Logs", 
                                   command=self.clear_logs, bg="#9C27B0", fg="white", width=15)
        self.clear_btn.grid(row=0, column=3, padx=8)

    def start_logging(self):
        self.logging = True
        self.start_btn.config(state=tk.DISABLED)
        self.stop_btn.config(state=tk.NORMAL)
        self.text_area.bind("<KeyRelease>", self.log_keys)
        self.key_count = 0
        self.update_counter()
        messagebox.showinfo("Logging Started", "Keystroke logging has started!")

    def stop_logging(self):
        self.logging = False
        self.start_btn.config(state=tk.NORMAL)
        self.stop_btn.config(state=tk.DISABLED)
        self.text_area.unbind("<KeyRelease>")
        self.save_log()
        messagebox.showinfo("Logging Stopped", f"Logs saved to {self.log_file}")

    def log_keys(self, event):
        if self.logging:
            self.key_count += 1
            self.update_counter()
            with open(self.log_file, "a", encoding="utf-8") as f:
                f.write(event.keysym + " ")

    def update_counter(self):
        self.counter_label.config(text=f"Keystrokes Logged: {self.key_count}")

    def save_log(self):
        with open(self.log_file, "a", encoding="utf-8") as f:
            f.write(f"\n\n--- Logging session ended at {datetime.datetime.now()} ---\n\n")

    def view_logs(self):
        if not os.path.exists(self.log_file) or os.path.getsize(self.log_file) == 0:
            messagebox.showinfo("No Logs", "Log file is empty.")
            return

        log_win = tk.Toplevel(self.root)
        log_win.title("View Logs")
        log_win.geometry("600x400")
        log_win.config(bg="#2C2C3E")

        log_area = scrolledtext.ScrolledText(log_win, wrap=tk.WORD, font=("Consolas", 11))
        log_area.pack(expand=True, fill="both", padx=10, pady=10)

        with open(self.log_file, "r", encoding="utf-8") as f:
            log_area.insert(tk.END, f.read())

    def clear_logs(self):
        open(self.log_file, "w").close()
        self.key_count = 0
        self.update_counter()
        messagebox.showinfo("Logs Cleared", "Log file has been cleared!")

# Run App
if __name__ == "__main__":
    root = tk.Tk()
    app = KeyLoggerApp(root)
    root.mainloop()
