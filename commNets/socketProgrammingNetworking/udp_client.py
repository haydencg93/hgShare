from socket import *

print("Start")

serverPort = 12000
serverName = "localhost"
message = "hello world!"

clientSocket = socket(AF_INET, SOCK_DGRAM)

print("Sending message")

clientSocket.sendto(message.encode(), (serverName, serverPort))

print("Wait for response")
modifiedMessage, serverAddress = clientSocket.recvfrom(1024)
print(modifiedMessage.decode())

print("End")