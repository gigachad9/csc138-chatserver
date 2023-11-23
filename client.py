import socket
import threading
import sys

def receive_messages(client_socket):
    """Handles receiving messages from the server."""
    while True:
        try:
            message = client_socket.recv(1024).decode()
            if not message:
                print("Disconnected from server.")
                break
            print(message)
        except Exception as e:
            print(f"Error receiving message: {e}")
            break

def main():
    host = '127.0.0.1'  # The server's hostname or IP address
    port = 12345        # The port used by the server

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client_socket.connect((host, port))
    except Exception as e:
        print(f"Failed to connect to the server: {e}")
        sys.exit(1)

    # Start a thread to listen to messages from the server
    threading.Thread(target=receive_messages, args=(client_socket,), daemon=True).start()

    print("Connected to the chat server. Type 'JOIN <username>' to register.")

    try:
        while True:
            message = input("")

            if message.lower() == "quit":
                break

            try:
                client_socket.send(message.encode())
            except Exception as e:
                print(f"Error sending message: {e}")
                break
    finally:
        print("Disconnecting from server...")
        client_socket.close()

if __name__ == "__main__":
    main()