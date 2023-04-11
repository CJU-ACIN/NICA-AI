from socket import *
import threading
import time

serverSock_1 = socket(AF_INET, SOCK_STREAM)
serverSock_2 = socket(AF_INET, SOCK_STREAM)

serverSock_1.bind(('', 8081))
serverSock_2.bind(('', 8082))

serverSock_1.listen()
serverSock_2.listen()

server_1, _ = serverSock_1.accept()
server_2, _ = serverSock_2.accept() 

print(server_1,end="\n")
print(server_2)

def ser1() :
    while True :
        recv = server_1.recv(1024)
        print(f'클라이언트1에서 보낸 데이터 :{recv}')
def ser2() :
    while True :
        recv = server_2.recv(1024)
        print(f'클라이언트2에서 보낸 데이터 :{recv}')

#server1 = threading.Thread(target=ser1)
server2 = threading.Thread(target=ser2)

#server1.start()
server2.start()

while True :
    recv = server_1.recv(1024)
    if "종료" in recv :
        server2.join()
        server2.start()