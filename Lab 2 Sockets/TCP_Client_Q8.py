# Gautam Kumar Mahar 2103114
# Code of Chat Room
import socket
import threading

# Create a TCP socket for the client
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Define the host as localhost
host = "10.196.13.94" # host = "localhost"

# Define the port to use
port = 43389 

# Connect the socket to the specified host and port
client.connect((host, port))

# Get the Name from the user
Name = input("Please, Enter Your Name:")

# Define the function to receive messages from the server
def coming():
    while True:
        try:
            # Receive messages from the server with a maximum size of 1024 bytes
            message = client.recv(1024).decode("utf-8")
            # Check if the message is "Name"
            if message == "Name":
                # Send the Name to the server
                client.send(Name.encode("utf-8"))
            else:
                # Print the received message
                print(message)
        except:
            # Print an error message and close the connection if an error occurs
            print("Error")
            client.close()
            break
# Define the function to send messages to the server
def send():
    while True:
        # Format the message to be sent
        message = f':{Name}:{input("")}'
        # Send the message to the server
        client.send(message.encode("utf-8"))
# Start a new thread to receive messages
coming_thread = threading.Thread(target=coming)
coming_thread.start()
# Start a new thread to send messages
send_thread = threading.Thread(target=send)
send_thread.start()
