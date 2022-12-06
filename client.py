import json
from datetime import datetime
from socket import *

serverName = '255.255.255.255'
serverPort = 12000
clientSocket = socket(AF_INET, SOCK_DGRAM)
clientSocket.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)
isQuit = False
while not isQuit:
    nfcCardId = input('Input nfc card id:')
    message = {"nfcCardId": str(nfcCardId), "Date": str(datetime.now())}
    clientSocket.sendto(json.dumps(message).encode(), (serverName, serverPort))
    modifiedMessage, serverAddress = clientSocket.recvfrom(2048)
    print(modifiedMessage.decode())
    isQuit = nfcCardId == 'exit'

clientSocket.close()
