import multiprocessing
import time
from socket import *


if __name__ == "__main__":
    serverSock = socket(AF_INET, SOCK_STREAM) #두가지인자는 어드레스
    print("SERVER ON")
    serverSock.bind(('', 6974))
    serverSock.listen(1)

    client, address = serverSock.accept()
    print(client)
    msg = (client.recv(1024)).decode()
    print(msg)
    