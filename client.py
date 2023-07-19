import socket
import threading
import json
import os

def enter_server():
    os.system('cls||clear')
    with open('servers.json') as f:
        data = json.load(f)
    print('Your servers:', end=" ")
    print(*data.keys(), sep=" ")
    server_name = input("\nEnter the server name: ")
    nickname = input("Choose Your Nickname: ")
    if nickname == 'admin':
        password = input("Enter Password for Admin: ")

    server_info = data.get(server_name)
    if server_info is None:
        print("Server not found.")
        return

    ip = server_info.get("ip")
    port = server_info.get("port")

    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client.connect((ip, port))
    except ConnectionRefusedError:
        print("Failed to connect to the server.")
        return

    client.sendall("NICK".encode('ascii'))
    client.sendall(nickname.encode('ascii'))

    if client.recv(1024).decode('ascii') == 'PASS':
        client.sendall(password.encode('ascii'))
        response = client.recv(1024).decode('ascii')
        if response == 'REFUSE':
            print("Connection is Refused! Wrong Password.")
            return

    stop_thread = False

    def receive():
        nonlocal stop_thread
        while not stop_thread:
            try:
                message = client.recv(1024).decode('ascii')
                if message == 'BAN':
                    print('Connection Refused due to Ban')
                    break
                else:
                    print(message)
            except socket.error:
                print('Error Occurred while Connecting')
                break

    def write():
        nonlocal stop_thread
        while not stop_thread:
            message = input(f' ')
            if message.startswith('/'):
                if nickname == 'admin':
                    if message.startswith('/kick'):
                        client.sendall(f'KICK {message[6:]}'.encode('ascii'))
                    elif message.startswith('/ban'):
                        client.sendall(f'BAN {message[5:]}'.encode('ascii'))
                else:
                    print("Commands can only be executed by Admins!!")
            else:
                client.sendall(f'{nickname}: {message}'.encode('ascii'))

    receive_thread = threading.Thread(target=receive)
    write_thread = threading.Thread(target=write)

    receive_thread.start()
    write_thread.start()

    while True:
        if not receive_thread.is_alive() or not write_thread.is_alive():
            stop_thread = True
            break


def add_server():
    os.system('cls||clear')
    server_name = input("Enter a name for the server: ")
    server_ip = input("Enter the IP address of the server: ")
    server_port = int(input("Enter the port number of the server: "))

    with open('servers.json', 'r') as f:
        data = json.load(f)

    data[server_name] = {"ip": server_ip, "port": server_port}

    with open('servers.json', 'w') as f:
        json.dump(data, f, indent=4)


while True:
    os.system('cls||clear')
    option = input("(1) Enter server\n(2) Add server\n")
    if option == '1':
        enter_server()
        break
    elif option == '2':
        add_server()
