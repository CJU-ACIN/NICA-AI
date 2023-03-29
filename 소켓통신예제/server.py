#client.py
from socket import *

clientSock = socket(AF_INET, SOCK_STREAM)
clientSock.connect(('192.168.0.2', 8080)) 


print('연결 확인 됐습니다.')
while True :
    text=input("입력하세요 : ")
    if text == '종료':
        clientSock.send(text.encode('utf-8'))
        break
    
    clientSock.send(text.encode('utf-8'))

    data = clientSock.recv(1024)
    print('받은 데이터 : ', data.decode('utf-8'))

# 소켓 종료 및 자원 반환 (포트 등)
clientSock.close()