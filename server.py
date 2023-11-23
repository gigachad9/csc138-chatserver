import socket
import sys
import threading

MAX_CLIENTS = 10
clients = {}

# Manages communication with the client
# parameters inlcude the client socket and client address
def handle_client(client_socket, client_address): 
    #this will hold a username
    username = None
    #this is dicitionary to hold the commands they point to handle join function and handle list function
    command_directory = {
        "join": handle_join,
        "list": handle_list,
        "bcst": handle_bcst
    }
    
    #this is the message that will be sent to the user the first time they connect 
    welcome_message = "Enter JOIN followed by your username "
    #send a message to the client over the socket connection 
    client_socket.send(welcome_message.encode())
    
    #try block to catch any exceptions that can happen
    try:
        #infinite loop
        while True:
            message = client_socket.recv(1024).decode()
            split_message = message.split()
            command = split_message[0].lower()
            
            if command == "join":
                username = handle_join(client_socket, username, message)
            #checks if registered
            elif username:
                if command in command_directory:
                    command_directory[command](client_socket, username, ' '.join(split_message[1:]))
                elif command == "quit":
                    #go to finally block to handle QUIT command
                    break
                #send unknown message to client if command isn't known
                else:
                    client_socket.send("Unknown Message".encode())
            else:
                client_socket.send("You must register to chat".encode())
    #handle QUIT command            
    finally:
        if username:
            del clients[username]
            print(f"{username} is quitting the chat server")
        client_socket.close()
            



def handle_join(client_socket, username, message):
    if username:
        client_socket.send("You are already registered".encode())
        return username
    
    requested_username = message.split()[1]
    if len(clients) >= MAX_CLIENTS:
        client_socket.send("Too Many Users".encode())
    elif requested_username in clients:
        client_socket.send("Username taken".encode())
    else:
        #client registered to client dictionary
        clients[requested_username] = client_socket
        
        join_message = (f"{requested_username} joined!")
        for user, client in clients.items():
            if user != requested_username:
                client.send(join_message.encode())
                
        welcome_mess2 = (f"{requested_username} joined! Connected to server!")
        client_socket.send(welcome_mess2.encode())
        
        return requested_username
    return None




def handle_list(client_socket):
    list_message = "\n".join(clients.keys())
    client_socket.send(list_message.encode())




def handle_bcst(client_socket, username, message):
    bcst_message = (f"{username}: {message[5:]}")
    for user, client in clients.items():
        if user != username:
            client.send(bcst_message.encode())




def create_server(svr_port):
    svr_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    svr_socket.bind(("0.0.0.0", svr_port))
    svr_socket.listen()
    
    hostname = socket.gethostname()
    svr_ip = socket.gethostbyname(hostname)
    print(f"The Chat Server Started on {svr_ip}:{svr_port}")
    
    try:
        while True:
            client_socket, client_address = svr_socket.accept()
            thread = threading.Thread(target=handle_client, args=(client_socket, client_address))
            thread.start()
    finally:
        svr_socket.close()




def main():
    try:
        if len(sys.argv) != 2:
            print("Usage: python3 server.py <srv_port>")
            sys.exit()
        if int(sys.argv[1]) < 65536:
            svr_port = int(sys.argv[1])
            create_server(svr_port)
    except Exception as e:
        print(f"An error occurred: {e}")
        sys.exit()


if __name__ == "__main__":
    main()