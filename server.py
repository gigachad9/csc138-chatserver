# CSC 138 Project - Section 06
# Members: Raj Pannu, Julain Bucio, Juan Carrera Bravo, 
#          Shaquan Carolina, Alan Lei
# Python chat room project that is connects various clients with each other
# while letting the user choose in what way they wish to interact.

import socket
import sys
import threading

#Max number of clients that can be registered
MAX_CLIENTS = 10
#Client dictionary to hold usernames and client info
clients = {}


#Handles the client commands and messages
#Certain commands are only available to registered clients
#Also handles the QUIT command in finally block
def handle_client(client_socket, client_address):
    # This will hold a username, used to determine is client is registered
    username = None
    # This is dictionary to hold the commands
    # Dictionary points to methods to handle said command
    command_directory = {
        "JOIN": handle_join,
        "LIST": handle_list,
        "BCST": handle_bcst,
        "MESG": handle_mesg
    }

    # This is the message that will be sent to the user the first time they connect
    welcome_message = "Enter JOIN followed by your username:"
    # Send welcome to the client over the socket connection
    client_socket.send(welcome_message.encode())

    # Try block to catch any exceptions that can happen
    try:
        # Infinite loop
        while True:
            #decode client message
            message = client_socket.recv(1024).decode()
            #disconnect client if empty message is received
            if not message:
                break
            #split client message into parts
            split_message = message.split()
            #first part of message is used to determine command
            command = split_message[0]

            if command == "JOIN":
                username = handle_join(client_socket, username, message)
            elif command == "QUIT":
                #go to finally block to handle QUIT command
                break
            # Checks if client is registered and allows command if registered
            elif username:
                if command == "LIST":
                    command_directory[command](client_socket)
                elif command == "BCST":
                    command_directory[command](username, message)
                elif command == "MESG":
                    command_directory[command](client_socket, username, ' '.join(split_message[1:]))
                # Send Unknown Message to client if the command is not supported
                else:
                    client_socket.send("Unknown Message".encode())
            # If the client is not registered, send message
            else:
                client_socket.send("You must register to chat. JOIN <username>".encode())
    #handles QUIT command
    finally:
        #checks if client is registered and send messages if client is
        if username:
            client_socket.send(f"{username} is quitting the chat server".encode())
            #delete client from database
            del clients[username]
            #send left message to remaining clients
            for client in clients.values():
                client.send(f"{username} left".encode())
            #server message
            print(f"{username} is quitting the chat server")
        #Closes client socket, disconnecting client
        client_socket.close()


# Registers a client with specified username
# As well as checking database size and if username already exists
# Returns None if error in registering client
def handle_join(client_socket, username, message):
    #Checks if client is already registered
    if username:
        client_socket.send("You are already registered".encode())
        return username

    #JOIN command args check
    split_message = message.split()
    if len(split_message) != 2:
        client_socket.send("Usage: JOIN <username>".encode())
        return None

    #number of clients in database and existing username check
    requested_username = message.split()[1]
    if len(clients) >= MAX_CLIENTS:
        client_socket.send("Too Many Users".encode())
    elif requested_username in clients:
        client_socket.send("Username taken".encode())
    #register client
    else:
        # Client registered to client dictionary
        clients[requested_username] = client_socket
        #server message
        print(f"{requested_username} Joined the Chatroom")

        #join message for rest of clients
        join_message = f"{requested_username} joined!"
        #send message to everyone except registering client
        for user, client in clients.items():
            if user != requested_username:
                client.send(join_message.encode())

        #special message for only the registering client
        welcome_mess2 = f"{requested_username} joined! Connected to server!"
        client_socket.send(welcome_mess2.encode())

        return requested_username
    return None


# Sends a list of registered clients
def handle_list(client_socket):
    all_users = ", ".join(clients.keys())
    client_socket.send(all_users.encode())


# Sends a message to all registered clients
def handle_bcst(username, message):
    #trim "bcst" from message
    broadcast_message = message[5:]

    message_for_everyone = f"{username}: {broadcast_message}"
    message_for_sender = f"{username} is sending a broadcast"

    #send one message for everyone
    #And send one message just to the broadcaster
    for userr, client in clients.items():
        if userr == username:
            client.send(message_for_sender.encode('utf-8'))
        client.send(message_for_everyone.encode('utf-8'))


#Allows registered user to a send message to a specific user
def handle_mesg(client_socket, username, message):
    # checks if there are enough args
    # gives error if there are less than 3 args
    split_message = message.split(maxsplit=1)
    if len(split_message) < 2:
        client_socket.send("Invalid usage. Use MESG <username> <message>".encode())
        return

    #message split into target user and message
    target_username, target_message = message.split(maxsplit=1)

    #if target send message else tell sender "Unregistered User"
    if target_username in clients:
        clients[target_username].send(f"{username}: {target_message}".encode())
    else:
        client_socket.send("Unregistered User.".encode())
        return


#Creates chat server with specified port
#Server setups network socket over TCP
def create_server(svr_port):
    #create server socket over tcp
    svr_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #bind to host ip and specified port
    svr_socket.bind(("0.0.0.0", svr_port))
    #start listening for clients
    svr_socket.listen()

    #get server hostname
    hostname = socket.gethostname()
    #get server ip address
    svr_ip = socket.gethostbyname(hostname)
    #Server start message
    print(f"The Chat Server Started on {svr_ip}:{svr_port}")

    #accept client, print server message
    #A new thread is spawned to handle the new client socket
    try:
        while True:
            #Accepts client connection and split into variables
            client_socket, client_address = svr_socket.accept()
            #Server message with client address
            print(f"Connected with {client_address}")
            #Creates a new thread for each client and passes them to handle_client method
            thread = threading.Thread(target=handle_client, args=(client_socket, client_address))
            thread.start()
    finally:
        svr_socket.close()


# Main function that checks system arguments
# Program exits with incorrect arguments
def main():
    try:
        # Checks if system arguments don't equal 2 and print usage message
        if len(sys.argv) != 2:
            print("Usage: python3 server.py <srv_port>")
            sys.exit()
        #Checks if port number is less than 65536 and starts server with port
        if int(sys.argv[1]) < 65536:
            svr_port = int(sys.argv[1])
            create_server(svr_port)
        #Close program if port is too high or not port
        else:
            print("Usage: python3 server.py <srv_port>")
            print("Port must be under 65536")
    # Exception handling
    except Exception as e:
        print(f"An error occurred: {e}")
        sys.exit()


if __name__ == "__main__":
    main()
