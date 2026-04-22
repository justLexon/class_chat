import json
import socket
import threading
import tkinter as tk
from tkinter import messagebox
from tkinter import scrolledtext

# Personal machine for hosting
HOST = "127.0.0.1"
# Port that the server listens on
PORT = 5000
# Amount of bytes that can be read at once
BUFFER_SIZE = 1024

def send_json(client_socket, payload):
    try:
        client_socket.sendall(json.dumps(payload).encode())
        return True
    except OSError:
        return False

def receive_json(client_socket):
    try:
        response_data = client_socket.recv(BUFFER_SIZE)
        if not response_data:
            return None

        return json.loads(response_data.decode())
    except (OSError, json.JSONDecodeError):
        return None

class ClassChatGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("ClassChat")
        self.root.geometry("900x600")
        self.root.configure(bg = "#f5f5f5")

        self.client_socket = None
        self.username = ""
        self.connected = False

        self.build_layout()

    def build_layout(self):
        self.main_frame = tk.Frame(self.root, bg = "#f5f5f5", padx = 12, pady = 12)
        self.main_frame.pack(fill = "both", expand = True)

        self.left_panel = tk.Frame(self.main_frame, bg = "#e9ecef", width = 260, padx = 12, pady = 12)
        self.left_panel.pack(side = "left", fill = "y")
        self.left_panel.pack_propagate(False)

        self.right_panel = tk.Frame(self.main_frame, bg = "#ffffff", padx = 12, pady = 12)
        self.right_panel.pack(side = "right", fill = "both", expand = True)

        username_label = tk.Label(
            self.left_panel,
            text = "Username",
            bg = "#e9ecef",
            font = ("Segoe UI", 11, "bold"),
        )
        username_label.pack(anchor = "w")

        self.username_entry = tk.Entry(self.left_panel, font = ("Segoe UI", 11))
        self.username_entry.pack(fill = "x", pady = (6, 10))

        self.connect_button = tk.Button(
            self.left_panel,
            text = "Connect",
            bg = "#2e8b57",
            fg = "white",
            activebackground = "#256f46",
            activeforeground = "white",
            font = ("Segoe UI", 10, "bold"),
            command = self.connect_to_server,
        )
        self.connect_button.pack(fill = "x")

        users_label = tk.Label(
            self.left_panel,
            text = "Connected Users",
            bg = "#e9ecef",
            font = ("Segoe UI", 11, "bold"),
        )
        users_label.pack(anchor = "w", pady = (18, 6))

        self.users_listbox = tk.Listbox(self.left_panel, height = 10, font = ("Consolas", 10))
        self.users_listbox.pack(fill = "x")

        commands_label = tk.Label(
            self.left_panel,
            text = "Commands",
            bg = "#e9ecef",
            font = ("Segoe UI", 11, "bold"),
        )
        commands_label.pack(anchor = "w", pady = (18, 6))

        commands_text = (
            "1. Connect with a username\n"
            "2. Select or type a recipient\n"
            "3. Enter a message\n"
            "4. Click Send Message\n"
            "5. Click Refresh Users anytime"
        )
        self.commands_label = tk.Label(
            self.left_panel,
            text = commands_text,
            justify = "left",
            bg = "#e9ecef",
            font = ("Segoe UI", 10),
        )
        self.commands_label.pack(anchor = "w")

        self.refresh_button = tk.Button(
            self.left_panel,
            text = "Refresh Users",
            font = ("Segoe UI", 10),
            command = self.request_user_list,
            state = "disabled",
        )
        self.refresh_button.pack(fill = "x", pady = (18, 8))

        self.disconnect_button = tk.Button(
            self.left_panel,
            text = "Disconnect",
            bg = "#b22222",
            fg = "white",
            activebackground = "#8f1b1b",
            activeforeground = "white",
            font = ("Segoe UI", 10, "bold"),
            command = self.disconnect_from_server,
            state = "disabled",
        )
        self.disconnect_button.pack(fill = "x")

        chat_label = tk.Label(
            self.right_panel,
            text = "Chat",
            bg = "#ffffff",
            font = ("Segoe UI", 12, "bold"),
        )
        chat_label.pack(anchor = "w")

        self.chat_box = scrolledtext.ScrolledText(
            self.right_panel,
            wrap = "word",
            font = ("Consolas", 10),
            state = "disabled",
            height = 20,
        )
        self.chat_box.pack(fill = "both", expand = True, pady = (8, 12))

        recipient_label = tk.Label(
            self.right_panel,
            text = "Recipient",
            bg = "#ffffff",
            font = ("Segoe UI", 10, "bold"),
        )
        recipient_label.pack(anchor = "w")

        self.recipient_entry = tk.Entry(self.right_panel, font = ("Segoe UI", 11))
        self.recipient_entry.pack(fill = "x", pady = (6, 10))

        message_label = tk.Label(
            self.right_panel,
            text = "Message",
            bg = "#ffffff",
            font = ("Segoe UI", 10, "bold"),
        )
        message_label.pack(anchor = "w")

        self.message_entry = tk.Text(self.right_panel, height = 4, font = ("Segoe UI", 11))
        self.message_entry.pack(fill = "x", pady = (6, 10))

        self.send_button = tk.Button(
            self.right_panel,
            text = "Send Message",
            bg = "#1f6feb",
            fg = "white",
            activebackground = "#1754b3",
            activeforeground = "white",
            font = ("Segoe UI", 10, "bold"),
            command = self.send_message,
            state = "disabled",
        )
        self.send_button.pack(fill = "x")

        self.users_listbox.bind("<<ListboxSelect>>", self.fill_recipient_from_list)
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

    def append_chat(self, message_text):
        self.chat_box.configure(state = "normal")
        self.chat_box.insert("end", f"{message_text}\n")
        self.chat_box.see("end")
        self.chat_box.configure(state = "disabled")

    def set_connected_state(self, connected):
        self.connected = connected

        if connected:
            self.connect_button.configure(state = "disabled")
            self.disconnect_button.configure(state = "normal")
            self.refresh_button.configure(state = "normal")
            self.send_button.configure(state = "normal")
            self.username_entry.configure(state = "disabled")
        else:
            self.connect_button.configure(state = "normal")
            self.disconnect_button.configure(state = "disabled")
            self.refresh_button.configure(state = "disabled")
            self.send_button.configure(state = "disabled")
            self.username_entry.configure(state = "normal")

    def connect_to_server(self):
        if self.connected:
            return

        username = self.username_entry.get().strip()
        if username == "":
            messagebox.showerror("Username Required", "Please enter a username first.")
            return

        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        try:
            self.client_socket.connect((HOST, PORT))
        except OSError:
            messagebox.showerror("Connection Failed", "Could not connect to the server.")
            self.client_socket.close()
            self.client_socket = None
            return

        ack_message = receive_json(self.client_socket)
        if ack_message is None:
            messagebox.showerror("Connection Failed", "Server did not respond.")
            self.client_socket.close()
            self.client_socket = None
            return

        username_sent = send_json(
            self.client_socket,
            {
                "type": "register",
                "sender": username,
            },
        )

        if not username_sent:
            messagebox.showerror("Connection Failed", "Username registration could not be sent.")
            self.client_socket.close()
            self.client_socket = None
            return

        username_response = receive_json(self.client_socket)
        if username_response is None:
            messagebox.showerror("Connection Failed", "Server disconnected during registration.")
            self.client_socket.close()
            self.client_socket = None
            return

        if username_response.get("type") == "error":
            messagebox.showerror("Registration Failed", username_response.get("text", "Unknown error."))
            self.client_socket.close()
            self.client_socket = None
            return

        self.username = username
        self.set_connected_state(True)
        self.append_chat(ack_message.get("text", "Connected."))
        self.append_chat(username_response.get("text", f"Username set to {username}"))

        receive_thread = threading.Thread(
            target = self.receive_messages,
            daemon = True,
        )
        receive_thread.start()

        self.request_user_list()

    def receive_messages(self):
        while self.connected and self.client_socket is not None:
            response_message = receive_json(self.client_socket)
            if response_message is None:
                self.root.after(0, lambda: self.handle_disconnect("Server disconnected."))
                break

            self.root.after(0, self.process_server_message, response_message)

    def process_server_message(self, response_message):
        message_type = response_message.get("type")

        if message_type == "chat":
            sender = response_message.get("sender", "Unknown")
            text = response_message.get("text", "")
            self.append_chat(f"From {sender}: {text}")
            return

        if message_type == "list":
            self.users_listbox.delete(0, "end")
            for user in response_message.get("users", []):
                self.users_listbox.insert("end", user)
            self.append_chat(response_message.get("text", "Connected users updated."))
            return

        if message_type == "disconnect":
            self.append_chat(response_message.get("text", "Closing connection."))
            self.handle_disconnect("Disconnected from server.")
            return

        self.append_chat(response_message.get("text", "Server response received."))

    def request_user_list(self):
        if not self.connected or self.client_socket is None:
            return

        message_sent = send_json(
            self.client_socket,
            {
                "type": "list",
                "sender": self.username,
            },
        )

        if not message_sent:
            self.handle_disconnect("Server disconnected.")

    def send_message(self):
        if not self.connected or self.client_socket is None:
            return

        receiver = self.recipient_entry.get().strip()
        text = self.message_entry.get("1.0", "end").strip()

        if receiver == "":
            messagebox.showerror("Recipient Required", "Please enter or select a recipient.")
            return

        if text == "":
            messagebox.showerror("Message Required", "Please enter a message to send.")
            return

        message_sent = send_json(
            self.client_socket,
            {
                "type": "chat",
                "sender": self.username,
                "receiver": receiver,
                "text": text,
            },
        )

        if not message_sent:
            self.handle_disconnect("Server disconnected before the message could be sent.")
            return

        self.append_chat(f"You to {receiver}: {text}")
        self.message_entry.delete("1.0", "end")

    def disconnect_from_server(self):
        if not self.connected or self.client_socket is None:
            return

        message_sent = send_json(
            self.client_socket,
            {
                "type": "disconnect",
                "sender": self.username,
            },
        )

        if not message_sent:
            self.handle_disconnect("Server disconnected before /quit could be sent.")

    def handle_disconnect(self, message_text):
        if self.client_socket is not None:
            try:
                self.client_socket.close()
            except OSError:
                pass

        self.client_socket = None
        self.username = ""
        self.users_listbox.delete(0, "end")
        self.set_connected_state(False)
        self.append_chat(message_text)

    def fill_recipient_from_list(self, event):
        selected_indexes = self.users_listbox.curselection()
        if len(selected_indexes) == 0:
            return

        selected_user = self.users_listbox.get(selected_indexes[0])
        self.recipient_entry.delete(0, "end")
        self.recipient_entry.insert(0, selected_user)

    def on_close(self):
        if self.connected:
            self.disconnect_from_server()
        self.root.destroy()

def main():
    root = tk.Tk()
    app = ClassChatGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
