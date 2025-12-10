from socket import *

print("Start")

serverPort = 12000
serverSocket = socket(AF_INET, SOCK_DGRAM)
serverSocket.bind(('', serverPort))

print("UDP server is ready to receive")

while True:
    message, clientAddress = serverSocket.recvfrom(1024)
    print(message.decode())
    modifiedMessage = message.decode().upper()
    
    serverSocket.sendto(modifiedMessage.encode(), clientAddress)

print("End")