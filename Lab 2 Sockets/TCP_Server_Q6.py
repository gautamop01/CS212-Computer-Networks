# Gautam Kumar Mahar 2103114
import socket

# Create a socket for listening to new connections
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind it to a host and a port
host = 'localhost'
port = 43389
s.bind((host, port))
print("Server started... waiting for a connection from the client")

# Start listening for TCP connections
s.listen(1)

# Accept a connection
connection_socket, addr = s.accept()
print("Connection initiated from", addr)

# Receive the client's name
client_name = connection_socket.recv(1024).decode()
print("Client name is :", client_name)

# Run an infinite loop to receive expressions from the client
while True:
  # Receive the expression from the client
  expression = connection_socket.recv(1024).decode()

  # Check if the client wants to quit
  if expression == "q":
    print("Session Ended")
    break

  # Split the expression into parts
  parts = expression.split()
  try:
    a = float(parts[0])
    b = float(parts[2])
  except ValueError:
    connection_socket.send("Incorrect expression format".encode('utf-8'))
    continue

  operator = parts[1]
  if operator not in ["+", "-", "*", "/"]:
    connection_socket.send("Incorrect operator".encode('utf-8'))
    continue
    
  # Calculate the result
  if operator == "+":
    result = a + b
  elif operator == "-":
    result = a - b
  elif operator == "*":
    result = a * b
  elif operator == "/":
    result = a / b

  # Send the result back to the client
  connection_socket.send(str(result).encode('utf-8'))

# Close the connection
connection_socket.close()

