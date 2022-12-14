import json
from socket import *

import requests


serverPort = 12000
serverSocket = socket(AF_INET, SOCK_DGRAM)
serverSocket.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)
serverSocket.bind(('', serverPort))

api_url = "https://shifttrackerapi.azurewebsites.net/Shifts"


print('The server is ready to receive')
while True:
    message, clientAddress = serverSocket.recvfrom(2048)
    response = ""
    try:
        receivedMessage = json.loads(message.decode())
        print(f'Received message from client: {receivedMessage}')
        dataNfcCardId = receivedMessage["nfcCardId"]
        dataDate = receivedMessage["Date"]
        print(f'Client nfcCardId: {dataNfcCardId}')
        print(f'Client date: {dataDate}')

        if dataNfcCardId is not None and dataDate is not None:
            apiResponse = requests.post(api_url, json=receivedMessage)
            print(f'API response: {apiResponse.json()}')
            response = str(apiResponse.json())

        else:
            response = 'Invalid data'

    except Exception as e:
        print(f'Error: {e}')
        response = 'Invalid json message'
    finally:
        serverSocket.sendto(response.encode(), clientAddress)