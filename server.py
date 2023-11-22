from multiprocessing import connection
import socket
import select
import sys
from _thread import *
# By Group 3 (Alan Lei, Julian Bucio, Juan Carrera Bravo, Raj Pannu, Shaquan Carolina)
# Sacramento State November 22 2023
# CSC 138 Section 06 

MaxNumberOfClients = 10

def create_server(port):
    svr_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    svr_socket.bind(("0.0.0.0", port))
    # Handles up to 10 connections
    svr_socket.listen();
    
    while True:
        client_socket, address = svr_socket.accept()
        print(f"Accepted connection from {address}")
        threading.Thread(target=handle_client, args=(client_socket, address)).start()
    

def join(client_socket,parts):



def handle_request(client_socket, request):
    parts = request.split()
    command = parts[0].upper()

    match command:
        case "JOIN":
            join(client_socket, parts)
        case "LIST":
            listM(client_socket)
        case "MESG":
            mesg(client_socket, parts)
        case "BCST":
            bcst(client_socket, parts)
        case "QUIT":
            quitSvr(clientsocket)
        case :
            send_response(client_socket, "Unknown Message")



def handle_unknown(client_socket, parts):
    send_response(client_socket, "Unknown Message"   





def clientthread(conn, addr): 
    # Sends a message to the client whose user object is connected
        request = input("Enter JOIN followed by your username: ")
        if(request.lower() == "JOIN")

    #thread = threading.Thread(target=clientthread, args=(conn, addr))
while True: 
            try: 
                message = connection.recv(2048) 
                if message: 
                    """prints the message and address of the 
                    user who just sent the message on the server 
                    terminal"""
                    print ("<" + addr[0] + "> " + message) 
                    # Calls broadcast function to send message to all 
                    message_to_send = "<" + addr[0] + "> " + message 
                    broadcast(message_to_send, conn) 
                else: 
                    """message may have no content if the connection 
                    is broken, in this case we remove the connection"""
                    remove(conn)
            except: 
                continue    




def broadcast(message, connection): 
    create_server()
    for clients in list_of_clients: 
        if clients!=connection: 
            try: 
                clients.send(message) 
            except: 
                clients.close() 
                # if the link is broken, we remove the client 
                remove(clients)




def main():
    try:
        if len(sys.argv) != 2:
            print("Usage: python server.py <srv_port>")
            sys.exit(1)
        svr_port = int(sys.argv[1])
        create_server(svr_port)
    except Exception as e:
        print("Error, please try again!")
        sys.exit(1)
if __name__ == "__main__":
    main()