# Gautam Kumar Mahar 2103114
import socket

# Create a socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# bind it to a host and a port
host = 'localhost'
port = 43389
s.connect((host, port))

# Send the client's name to the server
client_name = input("Please Enter your name: ")
s.send(client_name.encode('utf-8'))

# Run an infinite loop to receive input from the user
while True:
  # Read user input
  expression = input("Enter a expression and Use q for Exit : ")

  # Check if the user wants to quit
  if expression == "q":
    s.send("q".encode('utf-8'))
    print("Session Ended")
    break
  
  # Check if the expression is in the correct format
  parts = expression.split()
  if len(parts) != 3:
    print("Incorrect format, Please Enter Right format ")
    continue

  try:
    a = float(parts[0])
    b = float(parts[2])
  except ValueError:
    print("Incorrect format, Please Enter Right format")
    continue

  operator = parts[1]
  if operator not in ["+", "-", "*", "/"]:
    print("Incorrect operator, Please Enter Right Operator")
    continue

  # Send the expression to the server
  s.send(expression.encode('utf-8'))

  # Receive the result from the server
  result = s.recv(1024).decode()
  print("Result:", result)

# Close the connection
s.close()

