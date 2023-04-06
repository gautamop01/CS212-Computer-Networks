import socket
import os

# Define the host and port number
HOST = '10.196.13.94'
PORT = 9090

# Define the directory where the website files are stored
WEB_DIR = '/home/gautamop/Desktop/LAB5_HTML'

# Create a socket object
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to a specific address and port number
server_socket.bind((HOST, PORT))

# Listen for incoming connections
server_socket.listen()

# Loop indefinitely to accept client connections
while True:
    # Wait for a client to connect
    client_socket, client_address = server_socket.accept()

    # Receive data from the client
    request_data = client_socket.recv(1024)

    # Parse the request data to get the requested file name
    request_lines = request_data.decode().split('\r\n')
    request_file = request_lines[0].split()[1]

    # If the file name is empty, serve the index.html file
    if request_file == '/':
        request_file = '/index.html'

    # Construct the absolute path to the requested file
    abs_path = os.path.join(WEB_DIR, request_file[1:])

    # Check if the file exists
    if os.path.exists(abs_path):
        # Open the file and read its contents
        with open(abs_path, 'rb') as file:
            file_contents = file.read()

        # Send a response back to the client
        response_data = b"HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\n" + file_contents
        client_socket.sendall(response_data)
    else:
        # If the file doesn't exist, send a 404 error response
        response_data = b"HTTP/1.1 404 Not Found\r\nContent-Type: text/html\r\n\r\n<html><body><h1>404 Not Found</h1></body></html>"
        client_socket.sendall(response_data)

    # Close the connection
    client_socket.close()

# Close the server socket
server_socket.close()
