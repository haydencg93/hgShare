from socket import *

print("Start")

serverPort = 12000
serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.bind(('', serverPort))
serverSocket.listen(5)

print("TCP server is ready to receive")

while True:
    connectionSocket, clientAddress = serverSocket.accept()
    
    message = connectionSocket.recv(1024)
    
    print(message.decode())
    modifiedMessage = message.decode().upper()
    
    connectionSocket.send(modifiedMessage.encode())
    connectionSocket.close()

print("End")