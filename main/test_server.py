#server.py
from socket import *

serverSock = socket(AF_INET, SOCK_STREAM) #두가지인자는 어드레스 패밀리, 소켓 타입 
serverSock.bind(('', 8080)) #서버 소켓에서는 bind해줘야함, 
# ''이므로 8080번 포트에서 모든 인터페이스에게 연결하도록 한다.

serverSock.listen(1) #서버소켓에서만 쓰임,해당 소켓이 총 몇개의 동시접속까지를 허용수 인자

connectionSock, addr = serverSock.accept() 
print(str(addr),'에서 접속이 확인되었습니다.')


while True :
    try :
        data = connectionSock.recv(1024)
        print('받은 데이터 : ', data.decode('utf-8'))

        text=input("입력하세요 : ")

        connectionSock.send(text.encode('utf-8'))
        print('메시지를 보냈습니다.')
    except :
        pass