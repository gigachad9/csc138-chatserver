# CSC 138 Project - Section 06
# Members: Raj Pannu, Julain Bucio, Juan Carrera Bravo, 
#          Shaquan Carolina, Alan Lei
# Python chat room project that is connects various clients with each other
# while letting the user choose in what way they wish to interact.

import socket
import sys
import threading

MAX_CLIENTS = 10
clients = {}


# Manages communication with the client
# Parameters inlcude the client socket and client address
def handle_client(client_socket, client_address):
    # This will hold a username
    username = None
    # This is dicitionary to hold the commands
    # Commands point to handle join function and handle list function
    command_directory = {
        "join": handle_join,
        "list": handle_list,
        "bcst": handle_bcst,
        "mesg": handle_mesg
    }

    # This is the message that will be sent to the user the first time they connect
    welcome_message = "Enter JOIN followed by your username "
    # Send a message to the client over the socket connection
    client_socket.send(welcome_message.encode())

    # Try block to catch any exceptions that can happen
    try:
        # Infinite loop
        while True:
            message = client_socket.recv(1024).decode()
            split_message = message.split()
            command = split_message[0].lower()

            if command == "join":
                username = handle_join(client_socket, username, message)
            elif command == "quit":
                if username:
                    for client in clients.values():
                        client.send(f"{username} left".encode())
                    del clients[username]
                    print(f"{username} is quitting the chat server")
                client_socket.close()
            # Checks if registered
            elif username:
                if command == "list":
                    command_directory[command](client_socket)
                elif command == "bcst":
                    command_directory[command](username, message)
                elif command == "mesg":
                    command_directory[command](client_socket, username, message)
                # Send Unknown Message to client if the command isn't known
                else:
                    client_socket.send("Unknown Message".encode())
            # If the client is not registered, send message
            else:
                client_socket.send("You must register to chat. JOIN <username>".encode())
    finally:
        print(f"An error occurred")


# Registers a client with specified username
# As well as checking size and if username already exists
def handle_join(client_socket, username, message):
    if username:
        client_socket.send("You are already registered".encode())
        return username
    #JOIN args check
    split_message = message.split()
    if len(split_message) != 2:
        client_socket.send("Usage: JOIN <username>".encode())
        return None
    #number of clients check
    requested_username = message.split()[1]
    if len(clients) >= MAX_CLIENTS:
        client_socket.send("Too Many Users".encode())
    elif requested_username in clients:
        client_socket.send("Username taken".encode())
    else:
        # Client registered to client dictionary
        clients[requested_username] = client_socket

        client_ip, client_port = client_socket.getpeername()
        print(f"Connected with {client_ip}, {client_port}")

        join_message = f"{requested_username} joined!"
        for user, client in clients.items():
            if user != requested_username:
                client.send(join_message.encode())

        welcome_mess2 = f"{requested_username} joined! Connected to server!"
        client_socket.send(welcome_mess2.encode())

        return requested_username
    return None


# Sends a list of registed clients
def handle_list(client_socket):
    list_message = "\n".join(clients.keys())
    client_socket.send(list_message.encode())


# Sends a message to all registered clients
def handle_bcst(username, message):
    print(message)  # test purposes delete later
    broadcast_message = message[5:]

    message_for_everyone = f"{username}: {broadcast_message}"
    message_for_sender = f"{username} is sending a broadcast"

    for userr, client in clients.items():
        if userr == username:
            client.send(message_for_sender.encode('utf-8'))
        client.send(message_for_everyone.encode('utf-8'))


# Handles messanging by checking to see if it meets the specified number of arguments
def handle_mesg(client_socket, username, message):
    # checks if there are enough args
    # gives error if there are less than 3 args
    messparts = message.split(maxsplit=1)
    if len(messparts) < 2:
        client_socket.send("Invalid usage. Use MESG <username> <message>".encode())
        return

    target_username, target_message = message.split(maxsplit=1)

    if target_username in clients:
        clients[target_username].send(f"{username}: {target_message}".encode())
    else:
        client_socket.send("Unknown recipient.".encode())
        return


# Creates chat server with specified port, it accepts incoming connections
def create_server(svr_port):
    svr_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    svr_socket.bind(("0.0.0.0", svr_port))
    svr_socket.listen()

    hostname = socket.gethostname()
    svr_ip = socket.gethostbyname(hostname)
    #   Prints IP
    print(f"The Chat Server Started on {svr_ip}:{svr_port}")

    try:
        while True:
            #   Creates a new thread for each user connected
            client_socket, client_address = svr_socket.accept()
            thread = threading.Thread(target=handle_client, args=(client_socket, client_address))
            thread.start()
    finally:
        svr_socket.close()


# Main function that deals with system arugments
def main():
    try:
        # Checks if system arugments don't equal 2
        if len(sys.argv) != 2:
            print("Usage: python3 server.py <srv_port>")
            sys.exit()
            # Checks if port number is less than 65536
        if int(sys.argv[1]) < 65536:
            svr_port = int(sys.argv[1])
            create_server(svr_port)
    # Exception
    except Exception as e:
        print(f"An error occurred: {e}")
        sys.exit()


# Makes sure program is running as main
if __name__ == "__main__":
    main()

