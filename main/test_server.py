#server.py
from socket import *
import time

serverSock = socket(AF_INET, SOCK_STREAM) #두가지인자는 어드레스 패밀리, 소켓 타입 
serverSock.bind(('', 8080)) #서버 소켓에서는 bind해줘야함, 
# ''이므로 8080번 포트에서 모든 인터페이스에게 연결하도록 한다.

print("대기중")
serverSock.listen(1) #서버소켓에서만 쓰임,해당 소켓이 총 몇개의 동시접속까지를 허용수 인자

connectionSock, addr = serverSock.accept() 
print(str(addr),'에서 접속이 확인되었습니다.')

while True :
    data = connectionSock.recv(1024).decode('utf-8')
    
    if data == '종료':
        break
    
    """
    # if-elif로 해서 작업 분류하면될듯
    ex)
    
    elif data.find('읽어줘'):
        OCR 작업수행
    
    elif data.find('저거 알려줘'):
        손끝점 작업 ㅜ=수행
    
    elif 등등
        ...
    """
    
    print(data + '에 대한 작업 처리 중')
    time.sleep(1.5) # 작업 소요시간 1.5초
    print(data + '에 대한 처리 완료')
    
    text = (data+"처리 결과값").encode('utf-8')
    
    connectionSock.send(text)

serverSock.close()