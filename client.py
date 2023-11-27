# CSC 138 Project - Section 06
# Members: Raj Pannu, Julain Bucio, Juan Carrera Bravo,
#          Shaquan Carolina, Alan Lei

import socket
import sys
import threading


# @param client_socket
# Handles receiving messages from the server.
def receive_messages(client_socket):
    while True:
        try:
            # get message from the server, up to 1024 bytes
            message = client_socket.recv(1024).decode()
            # check message exists
            if message:
                print(message)
            else:
                print("Server connection closed")
                # Stop client if received empty message
                break
        except Exception as e:
            # print error on fault message
            print(f"Error receiving message: {e}")
            # Exit loop
            break
    # CLose client socket and exit thread
    client_socket.close()


# @param svr_ip server IP Address
# @param svr_port port number
def create_client(svr_ip, svr_port):
    # create client socket
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # attempt to connect to server, return failed to connect if connect fails
    try:
        client_socket.connect((svr_ip, svr_port))
    except Exception as e:
        print(f"Failed to connect to the server: {e}")
        sys.exit(1)

    # Start a thread to listen to messages from the server
    threading.Thread(target=receive_messages, args=(client_socket,), daemon=True).start()

    try:
        # Create loop for messages sent to the server
        while True:
            message = input("")

            # Break out of loop if user wants to quit
            if message == "QUIT":
                break

            try:
                # Attempt to send user's message to the server
                client_socket.send(message.encode())
            except Exception as e:
                # print error statement on message send failure
                print(f"Error sending message: {e}")
                break
    finally:
        # exit the program by closing client socket
        client_socket.close()
        sys.exit(1)


def main():
    # ensure command line arguments is exactly 3
    if len(sys.argv) != 3:
        print("Usage:python client.py < server_ip> < server_port>")
        sys.exit(1)

    # get ip and port from command line args
    svr_ip = sys.argv[1]
    svr_port = int(sys.argv[2])
    create_client(svr_ip, svr_port)


# start the program
if __name__ == "__main__":
    main()
