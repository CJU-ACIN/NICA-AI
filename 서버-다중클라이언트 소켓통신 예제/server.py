#server.py
from socket import *
import threading # 멀티스레드를 통한 병렬처리
import time # 작업시간 예시



'''
print(str(addr),'에서 접속이 확인되었습니다.')
print("명령 대기 중")
while True :
    try:
        data = connectionSock.recv(1024).decode('utf-8')
        
        """
        # if-elif로 해서 작업 분류하면될듯
        예시)
        
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

    except ConnectionAbortedError:
        print("기존 클라이언트와 접속 끊김")
        break
'''

# 실제로 수행하는 서비스
def service(client, address):
    client.send("SUCCESS".encode('utf-8'))
    print(f"{address}에서 접속 성공")
    
    while True:
        try:
            print(f"{address}의 명령 대기중")
            # 텍스트 형식으로 클라이언트로부터 request 받기
            request = client.recv(1024).decode('utf-8')
            
            print(f"{address}의 요청: {request} ... 처리 중")
            
            time.sleep(2) # 실제 작업; 작업 소요시간 2초
            
            print(f"{address}의 요청: {request} ... 완료")
            
            
            """
            # 위에는 예시고, if-elif로 해서 작업 분류하면됨
            # 49~57줄 지우고
            예시)
            
            if data.find('읽어줘'):
                OCR 작업수행
            
            elif data.find('저거 알려줘'):
                손끝점 작업 수행
            
            elif 등등
                ...
            """

            # 텍스트로 이루어진 결과값
            response = (f"{request}처리 결과값").encode('utf-8')
            client.send(response)
            
        except ConnectionAbortedError:
            break
        
        except ConnectionResetError:
            break
    
    client.close()



### 메인 동작

# 서버 소켓 객체 생성
serverSock = socket(AF_INET, SOCK_STREAM) #두가지인자는 어드레스 패밀리, 소켓 타입 
# '' = 포트 8080에 접속하는 모든 ip 허용

serverSock.bind(('', 8081)) #서버 소켓에서는 bind해줘야함
print("=== SERVER ON-LINE ===") # 서버 시작 알림

max_conn = 2 # 최대 접속자 2명
cur_conn = 0 # 현재 접속자

while True:
    serverSock.listen(1) # 대기열 같은 개념, 소켓 최대 인원이 아님
    client, address = serverSock.accept() # 일단 연결 수락, 거부 함수가 없음
    cur_conn += 1
    

    # 인원 초과 안될 때
    if cur_conn <= max_conn:
        
        thread_service = threading.Thread(target=service, args=(client, address))
        thread_service.start()
    
    else:
        cur_conn -= 1
        client.send('NG'.encode('utf-8'))
        client.close()
        
        
    print(f"현재 서비스 이용자: {cur_conn}")
    