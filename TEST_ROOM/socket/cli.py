from socket import *

server_address = '192.168.0.119'

clientSock_1 = socket(AF_INET, SOCK_STREAM)         # 취소 클라이언트 실행
clientSock_1.connect((server_address, 8081)) 
print("취소 클라이언트 1 연결 완료")

clientSock_2 = socket(AF_INET, SOCK_STREAM)         # 취소 클라이언트 실행
clientSock_2.connect((server_address, 8082)) 
print("취소 클라이언트 2 연결 완료")

while True :
    text = input("입력 :")

    if "서버1" in text :
        clientSock_1.send(text.encode('utf-8'))   
    elif "서버2" in text :
        clientSock_2.send(text.encode('utf-8'))   
    else :
        clientSock_1.close()
        clientSock_2.close()
        break