from multiprocessing import connection
import socket
import select
import sys
from _thread import *
# By Group 3 (Alan Lei, Julian Bucio, Juan Carrera Bravo, Raj Pannu, Shaquan Carolina)
# Sacramento State November 22 2023
# CSC 138 Section 06 
#hello
# testing
def create_server(port):
    svr_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    svr_socket.bind(("0.0.0.0", port))
    # Handles up to 10 connections
    svr_socket.listen(10)
    list_of_clients = []
    client_usernames = []
    join()
    while True:
        threading.Thread(target=)

def checkInput():
     commands = [
          "JOIN"
          "LIST"
          "MESG"
          "BCST"
          "QUIT"
     ]

     user_input = input("")

     if user_input in commands:
          print(f"" {user_})
          
     

def join():
    while True:
        request = input("Enter JOIN followed by your username: ")
        if(request.lower().startswith("join")):
            return request
        else:
            print("Please try again.")


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