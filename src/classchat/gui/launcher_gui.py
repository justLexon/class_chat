import subprocess
import sys
import tkinter as tk
from pathlib import Path
from tkinter import messagebox

BASE_DIR = Path(__file__).resolve().parents[3]
SERVER_PATH = BASE_DIR / "src" / "classchat" / "server" / "server.py"
CLIENT_GUI_PATH = BASE_DIR / "src" / "classchat" / "gui" / "client_gui.py"

class ClassChatLauncherGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("ClassChat Launcher")
        self.root.geometry("420x320")
        self.root.configure(bg = "#f5f5f5")

        self.server_process = None
        self.client_processes = []

        self.build_layout()
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

    def build_layout(self):
        main_frame = tk.Frame(self.root, bg = "#f5f5f5", padx = 20, pady = 20)
        main_frame.pack(fill = "both", expand = True)

        title_label = tk.Label(
            main_frame,
            text = "ClassChat Launcher",
            bg = "#f5f5f5",
            font = ("Segoe UI", 16, "bold"),
        )
        title_label.pack(anchor = "w")

        info_label = tk.Label(
            main_frame,
            text = "Start one server and open as many client windows as you need.",
            bg = "#f5f5f5",
            font = ("Segoe UI", 10),
            justify = "left",
        )
        info_label.pack(anchor = "w", pady = (8, 18))

        self.server_button = tk.Button(
            main_frame,
            text = "Start Server",
            bg = "#2e8b57",
            fg = "white",
            activebackground = "#256f46",
            activeforeground = "white",
            font = ("Segoe UI", 11, "bold"),
            command = self.start_server,
        )
        self.server_button.pack(fill = "x", pady = (0, 10))

        self.open_client_button = tk.Button(
            main_frame,
            text = "Open Client",
            bg = "#1f6feb",
            fg = "white",
            activebackground = "#1754b3",
            activeforeground = "white",
            font = ("Segoe UI", 11, "bold"),
            command = self.open_client,
        )
        self.open_client_button.pack(fill = "x", pady = (0, 10))

        self.status_label = tk.Label(
            main_frame,
            text = "Server not started.",
            bg = "#f5f5f5",
            font = ("Segoe UI", 10, "italic"),
            justify = "left",
        )
        self.status_label.pack(anchor = "w", pady = (8, 8))

        self.client_count_label = tk.Label(
            main_frame,
            text = "Client windows opened: 0",
            bg = "#f5f5f5",
            font = ("Segoe UI", 10),
            justify = "left",
        )
        self.client_count_label.pack(anchor = "w")

    def start_server(self):
        if self.server_process is not None and self.server_process.poll() is None:
            messagebox.showinfo("Server Running", "The server is already running.")
            return

        try:
            self.server_process = subprocess.Popen(
                [sys.executable, str(SERVER_PATH)],
                cwd = str(BASE_DIR),
            )
        except OSError:
            messagebox.showerror("Server Error", "Could not start the server process.")
            return

        self.status_label.configure(text = "Server started.")

    def open_client(self):
        try:
            client_process = subprocess.Popen(
                [sys.executable, str(CLIENT_GUI_PATH)],
                cwd = str(BASE_DIR),
            )
        except OSError:
            messagebox.showerror("Client Error", "Could not open the client window.")
            return

        self.client_processes.append(client_process)
        self.cleanup_client_processes()
        self.client_count_label.configure(
            text = f"Client windows opened: {len(self.client_processes)}"
        )

    def cleanup_client_processes(self):
        active_clients = []

        for process in self.client_processes:
            if process.poll() is None:
                active_clients.append(process)

        self.client_processes = active_clients

    def on_close(self):
        self.cleanup_client_processes()

        if self.server_process is not None and self.server_process.poll() is None:
            should_close = messagebox.askyesno(
                "Close Launcher",
                "The server is still running. Do you want to stop it and close the launcher?",
            )

            if not should_close:
                return

            self.server_process.terminate()

        self.root.destroy()

def main():
    root = tk.Tk()
    app = ClassChatLauncherGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
