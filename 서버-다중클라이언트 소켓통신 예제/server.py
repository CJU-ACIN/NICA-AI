#server.py
from socket import *
import threading # 멀티스레드를 통한 병렬처리
import time # 작업시간 예시


## 아래 작업명령boolean 과 결과값 따로 변수 밖에 뺴서 이걸로 쓰는거라
## 멀티 사용자는 안됨
## 하지만 클래스를 만들어서 안에 다 꼬라박으면 됨
# 그니깐 누군가 해줘

# 작업 명령 boolean
serviceToy_active = True
stopService_active = True

# 결과값
result_toy = ""

## 중단의 중단 신호 체크 하는 거 만들기

# 진행중인 작업 중단
def stopServiceProcess(client, service_thread):
    global serviceToy_active
    global stopService_active
    while stopService_active:
        data = client.recv(1024)
    
        if data.decode('utf-8') == "종료":
            serviceToy_active = False
            print("요청 중단!")


def toy():
    global serviceToy_active
    global stopService_active
    global result_toy
    
    for i in range(3):
        print(i)
        time.sleep(0.5)
        
        
        if serviceToy_active == False:
            client.send("중단".encode('utf-8'))
            
            break

        result_toy = "결과값"
        
    return result_toy

    
# 클라이언트 서비스
def service(client, address):
    client.send("SUCCESS".encode('utf-8'))
    print(f"{address}에서 접속 성공")
    
    while True:
        try:
            print(f"{address}의 명령 대기중")
            # 텍스트 형식으로 클라이언트로부터 request 받기
            request = client.recv(1024).decode('utf-8')
            
            print(f"{address}의 요청: {request} ... 처리 중")
            
            thread_toy = threading.Thread(target=toy)
            thread_stopServiceProcess = threading.Thread(target=stopServiceProcess, args=(client,thread_toy))
            
            thread_toy.start()
            thread_stopServiceProcess.start()

            thread_toy.join()
            thread_stopServiceProcess.join()
            
            
            time.sleep(0.5) # 이거 안넣으면 쓰레드 멈춰야하는거 감지못해서 계속함
            
            # 다시 active 상태로 만들어주기
            global serviceToy_active
            serviceToy_active = True
    
            
            
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
    