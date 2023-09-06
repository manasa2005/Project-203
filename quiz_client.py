import socket
import threading

def receive(client_socket):
    while True:
        try:
            message = client_socket.recv(1024).decode('utf-8')
            if message == "NICKNAME":
                nickname = input("Choose your nickname: ")
                client_socket.send(nickname.encode('utf-8'))
            else:
                print(message)
        except:
            print("An error occurred.")
            client_socket.close()
            break

def write(client_socket):
    while True:
        try:
            message = input()
            client_socket.send(message.encode('utf-8'))
        except:
            print("An error occurred.")
            client_socket.close()
            break

def main():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_ip = '127.0.0.1'  
    server_port = 12345 

    client_socket.connect((server_ip, server_port))

    receive_thread = threading.Thread(target=receive, args=(client_socket,))
    write_thread = threading.Thread(target=write, args=(client_socket,))

    receive_thread.start()
    write_thread.start()

if __name__ == "__main__":
    main()