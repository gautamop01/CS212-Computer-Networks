# Gautam Kumar Mahar 2103114
# Code of a Chat Room
import socket
import threading 

# Bind it to a host and a port
host = '10.196.13.94' # host = "localhost"  # localhost IP
port = 43389 # Randomly chosen port number

# Create a socket for listening to new connections
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# Bind the socket to a specific address and port
s.bind((host, port))     
# Start listening for TCP connections
s.listen()
print("Server started... waiting for a connection from the client")

# Lists to keep track of clients and their clientnames
clients = []
clientnames = []
# Function to sending messages to all clients
def sending(message):
    for client in clients:
        client.send(message)

# Function to manage individual client connections
def manage(client):
    while True:
        try:
            # coming message from client
            message = client.recv(1024) #Highest well known
            # sending the message to all clients
            sending(message)
        except:
            # If the client connection is lost, remove the client from the list and close the connection
            index = clients.index(client)
            clients.remove(client)
            client.close()
            message1 = clientnames[index] + " left chat"
            sending(message1.encode('utf-8'))
            clientnames.remove(clientnames[index])
            break

# Function to coming incoming client connections
def coming():
    while True:
        # Accept incoming connection
        client, address = s.accept()
        print(f"Connected {str(address)}")

        # Send the clientname request to the client
        client.send("Please, Enter Your ig name".encode('utf-8'))
        # coming the clientname from the client
        clientname = client.recv(1024).decode('utf-8')

        # Add the client and its clientname to the lists
        clientnames.append(clientname)
        clients.append(client)

        print(f"new user name is {clientname}!")
        
        # Send a message to the client that they have successfully connected
        client.send(f"new user {clientname} connected!\n".encode('utf-8'))

        # sending a message to all clients that a new client has joined the chat
        sending((f"new user {clientname} joined \n").encode('utf-8'))

        # Start a new thread to manage the client's messages
        thread = threading.Thread(target=manage, args=(client,))
        thread.start()

# Call the coming function to start receiving client connections
coming()

