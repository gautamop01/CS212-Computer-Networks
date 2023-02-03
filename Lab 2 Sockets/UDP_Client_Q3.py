# Gautam Kumar Mahar 2103114
import socket
import time, random

# create a socket
s=socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# bind it to a host and a port
host='localhost'
port=43387  # this is the server's port number, which the client needs to know

# send requests and receive responses in a loop
while True:
    message = random.choice(["SEND_DATE", "SEND_TIME"])
    s.sendto( message.encode('utf-8'), (host,port))

    data, addr = s.recvfrom(1024) # buffer size is 1024 bytes
    print("Client received MESSAGE =",data.decode()," from ADDR =",addr)
    time.sleep(random.uniform(1,2))

# close the connection
s.close()

