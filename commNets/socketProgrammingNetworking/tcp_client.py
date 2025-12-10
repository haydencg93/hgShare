from socket import *

print("Start")

serverPort = 12000
serverName = "localhost"
message = "hello world!"

clientSocket = socket(AF_INET, SOCK_STREAM)

print("Sending message")
clientSocket.connect((serverName, serverPort))
clientSocket.send(message.encode())

print("Wait for response")
modifiedMessage = clientSocket.recv(1024)
print(modifiedMessage.decode())

print("End")