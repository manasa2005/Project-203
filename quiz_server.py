import socket
import threading
import tkinter as tk
from tkinter import Text, Scrollbar
import threading

class GUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.withdraw()
        self.login_window = tk.Toplevel()
        self.login_window.title("Login")
        self.login_window.geometry("300x100")
        self.login_window.resizable(False, False)

        label = tk.Label(self.login_window, text="Please login before continuing.")
        label.place(relx=0.5, rely=0.4, anchor="center")

        self.name_label = tk.Label(self.login_window, text="Enter your nickname:")
        self.name_label.place(relx=0.2, rely=0.6, anchor="center")

        self.name_entry = tk.Entry(self.login_window)
        self.name_entry.place(relx=0.5, rely=0.6, anchor="center")

        login_button = tk.Button(self.login_window, text="Login", command=lambda: self.goAhead())
        login_button.place(relx=0.8, rely=0.6, anchor="center")

        self.name = None

    def layout(self, name):
        self.login_window.destroy()
        self.name = name

        self.root.deiconify()
        self.root.geometry("400x400")

        # Display the user's name at the top
        welcome_label = tk.Label(self.root, text="Welcome, " + self.name)
        welcome_label.place(relx=0.5, rely=0.05, anchor="center")

        # Create a TextArea for messages
        self.text_area = Text(self.root, wrap=tk.WORD)
        self.text_area.place(relx=0.5, rely=0.2, relwidth=0.9, relheight=0.6, anchor="center")

        # Create an Entry for user input
        self.input_entry = tk.Entry(self.root)
        self.input_entry.place(relx=0.5, rely=0.85, relwidth=0.7, anchor="center")

        # Create a Label as a separator
        separator_label = tk.Label(self.root, text="--------------------------------------------------")
        separator_label.place(relx=0.5, rely=0.92, anchor="center")

        # Create a Send button
        send_button = tk.Button(self.root, text="Send", command=self.sendMessage)
        send_button.place(relx=0.8, rely=0.85, anchor="center")

        # Add a Scrollbar to the TextArea
        scrollbar = Scrollbar(self.text_area)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.text_area.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.text_area.yview)

    def goAhead(self):
        name = self.name_entry.get()
        self.layout(name)

    def sendMessage(self):
        message = self.input_entry.get()
        if message:
            self.show_message("You: " + message)
            # Send message to the server and handle it accordingly (replace with your logic)
            self.input_entry.delete(0, tk.END)

    def show_message(self, message):
        self.text_area.insert(tk.END, message + "\n")

if __name__ == "__main__":
    GUI()


def handle_client(client_socket, nickname):
    nicknames.append(nickname)

    while True:
        try:
            message = client_socket.recv(1024).decode('utf-8')
            if not message:
                remove_client(client_socket, nickname)
                break
            broadcast(message, nickname)
        except:
            remove_client(client_socket, nickname)
            break

def broadcast(message, sender):
    for client, nickname in clients:
        if client != sender:
            try:
                client.send(message.encode('utf-8'))
            except:
                remove_client(client, nickname)

def remove_client(client_socket, nickname):
    nicknames.remove(nickname)
    client_socket.close()

def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_ip = '127.0.0.1' 
    server_port = 12345  
    server.bind((server_ip, server_port))
    server.listen(5)

    print("Server started listening on {}:{}".format(server_ip, server_port))

    while True:
        client_socket, client_address = server.accept()
        print("Connected from {}:{}".format(client_address[0], client_address[1]))

        client_socket.send("NICKNAME".encode('utf-8'))
        nickname = client_socket.recv(1024).decode('utf-8')

        client_thread = threading.Thread(target=handle_client, args=(client_socket, nickname))
        client_thread.start()
        clients.append((client_socket, nickname))

if __name__ == "__main__":
    nicknames = []
    clients = []
    main()