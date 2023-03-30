#client.py
from socket import *
import threading
import time


# 결과값 받기 대기 확인
getResponse_active = True
stopServiceRequest_active = True

# 진행중인 작업 중단
def stopServiceRequest(clientSock):
    global stopServiceRequest_active
    
    cnt = 0
    while stopServiceRequest_active:
        msg = "."
        time.sleep(0.5)
        clientSock.send(msg.encode('utf-8'))

        cnt+=1
        if cnt==5:
            msg = "중단"
            clientSock.send(msg.encode('utf-8'))


def getResponse(cilentSock):
    global stopServiceRequest_active
    global getResponse_active
    
    while getResponse_active:
        data = cilentSock.recv(1024)
        print('받은 데이터 : ', data.decode('utf-8'))

        if data == ".":
            ...

        elif data == "중단":
            print("서비스 중단!")
        
        else:
            print("결과값")
    


clientSock = socket(AF_INET, SOCK_STREAM)
server_address = '203.252.230.246'

clientSock.connect((server_address, 8081)) 

data = clientSock.recv(1024) # 서버 접속 성공여부 받기
data = data.decode('utf-8')

print(f"서버 접속 상황: {data}")

# 서버 접속 시도
# 성공
if data == "SUCCESS":
    print('연결 확인 됐습니다.')

    while True :
        time.sleep(0.5) # 지연 있어야 스레드 끝난걸 감지
        text=input("원하는 서비스 입력하세요 : ")
        if text == '종료':
            break
        
        clientSock.send(text.encode('utf-8'))
        
        # 스레드 선언
        thread_waitResponse = threading.Thread(target=getResponse, args = (clientSock,))
        
        thread_stopServiceRequest = threading.Thread(target=stopServiceRequest, args = (clientSock,))
        
        # 쓰레드 실행 및 상호 대기
        thread_waitResponse.start()
        thread_stopServiceRequest.start()
        
        thread_waitResponse.join()
        thread_stopServiceRequest.join()
        
        time.sleep(0.5) # 이거 안넣으면 쓰레드 멈춘걸 감지못해서 계속함
    
        # 다시 active 상태로 만들어주기
        getResponse_active = True
        stopServiceRequest_active = True



# 실패
elif data == "NG":
    print("서버 접속 실패!")
    clientSock.close()