# Gautam Kumar Mahar 2103114
import socket
import time

# create a socket
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# bind it to a host and a port
host = 'localhost'
port = 43387  # arbitrarily chosen non-privileged port number
s.bind((host,port))

print("Server started...waiting for a request from the client")

# receive some bytes and print them
while True:
    data, addr = s.recvfrom(1024) # buffer size is 1024 bytes
    request = data.decode()
    print("Server received MESSAGE =", request, "from ADDR =", addr)

    if request == "SEND_DATE":
        response = time.strftime("%x")
    elif request == "SEND_TIME":
        response = time.strftime("%X")
    else:
        response = "Invalid request"
        
    s.sendto(response.encode('utf-8'), (addr[0], addr[1]))

# close the connection
s.close()

