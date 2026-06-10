import tkinter as tk
from tkinter import messagebox
import psutil
from datetime import datetime

# Suspicious keywords
suspicious_keywords = [
    "keylogger",
    "logger",
    "spy",
    "hook",
    "capture",
    "record"
]

# Scan function
def scan_processes():
    process_list.delete(0, tk.END)

    suspicious_found = False

    for process in psutil.process_iter(['pid', 'name']):
        try:
            pid = process.info['pid']
            name = str(process.info['name'])

            is_suspicious = False

            for keyword in suspicious_keywords:
                if keyword in name.lower():
                    is_suspicious = True
                    suspicious_found = True

                    alert_message = (
                        f"[{datetime.now()}] "
                        f"Suspicious Process Found: "
                        f"{name} (PID: {pid})"
                    )

                    with open("alerts.log", "a") as file:
                        file.write(alert_message + "\n")

            if is_suspicious:
                process_list.insert(
                    tk.END,
                    f"⚠ ALERT | PID: {pid} | {name}"
                )
            else:
                process_list.insert(
                    tk.END,
                    f"PID: {pid} | {name}"
                )

        except:
            pass

    if suspicious_found:
        messagebox.showwarning(
            "Alert",
            "Suspicious process detected!"
        )
    else:
        messagebox.showinfo(
            "Scan Complete",
            "No suspicious process found."
        )

# CPU & RAM Monitor
def update_usage():

    cpu = psutil.cpu_percent()

    ram = psutil.virtual_memory().percent

    cpu_label.config(
        text=f"CPU Usage : {cpu}%"
    )

    ram_label.config(
        text=f"RAM Usage : {ram}%"
    )

    root.after(1000, update_usage)

# View Logs
def view_logs():

    try:
        with open("alerts.log", "r") as file:
            content = file.read()

        log_window = tk.Toplevel(root)
        log_window.title("Alert Logs")
        log_window.geometry("700x400")

        text = tk.Text(log_window)
        text.pack(fill="both", expand=True)

        text.insert(tk.END, content)

    except:
        messagebox.showinfo(
            "Logs",
            "No logs found."
        )

# Main Window
root = tk.Tk()

root.title(
    "Keylogger Detection & System Monitoring"
)

root.geometry("900x600")
root.configure(bg="#1e1e2f")

title = tk.Label(
    root,
    text="Keylogger Detection & System Monitoring",
    font=("Arial", 18, "bold"),
    fg="white",
    bg="#1e1e2f"
)

title.pack(pady=15)

cpu_label = tk.Label(
    root,
    text="CPU Usage : 0%",
    font=("Arial", 12),
    fg="cyan",
    bg="#1e1e2f"
)

cpu_label.pack()

ram_label = tk.Label(
    root,
    text="RAM Usage : 0%",
    font=("Arial", 12),
    fg="cyan",
    bg="#1e1e2f"
)

ram_label.pack()

process_list = tk.Listbox(
    root,
    width=120,
    height=20,
    bg="#2d2d44",
    fg="white",
    font=("Consolas", 10)
)

process_list.pack(pady=15)

button_frame = tk.Frame(
    root,
    bg="#1e1e2f"
)

button_frame.pack()

scan_btn = tk.Button(
    button_frame,
    text="Scan Processes",
    command=scan_processes,
    bg="#0078D7",
    fg="white",
    width=20
)

scan_btn.grid(row=0, column=0, padx=10)

log_btn = tk.Button(
    button_frame,
    text="View Logs",
    command=view_logs,
    bg="#28A745",
    fg="white",
    width=20
)

log_btn.grid(row=0, column=1, padx=10)

update_usage()

root.mainloop()