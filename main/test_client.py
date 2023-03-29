#client.py
from socket import *
from _thread import *
## _thread 모듈로 msg 송신동작과 수신 동작을 각개 다른 스레드가 처리
## 병렬 처리

clientSock = socket(AF_INET, SOCK_STREAM)
clientSock.connect(('203.252.240.40', 8080)) 


print('서버와 연결 확인 됐습니다.')


while True:
    
    
    clientSock.send('I am a client'.encode('utf-8'))

    print('메시지를 전송했습니다.')

    msg = clientSock.recv(1024)
    print('받은 데이터 : ', msg.decode('utf-8'))
