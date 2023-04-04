#server.py
from socket import *
# import threading # 멀티스레드를 통한 병렬처리
import time # 작업시간 예시
import multiprocessing

# 실제로 수행하는 서비스
def service(connectionSock):
    #client.send("SUCCESS".encode('utf-8'))
    print("서버 서비스 리시버 실행")
    while True:
        try:
            command = connectionSock.recv(1024)
            command = command.decode('utf-8')
            print(f"서버 수신 명령 => {command}")
            
            if command == "book" or command == "word" :
                
                # 이미지 디코딩 후 저장
                imageDecode()

                img = "t.jpeg"
                ocr = Pororo(task="ocr", lang='ko')

                text = ""

                # 텍스트 생성
                for word in ocr(img) :
                    text += word
                print(f'=> {text}')

                if len(text) <= 2:
                    connectionSock.send("글자를 탐지하지 못했어요...".encode('utf-8'))
                else :
                    # 인식한 텍스트 전송
                    connectionSock.send(text.encode('utf-8'))

            else :
                # 객체 선언
                mpHands = mp.solutions.hands
                hands = mpHands.Hands()
                mpDraw = mp.solutions.drawing_utils

                # 이미지 디코딩 후 저장
                imageDecode()

                src = cv2.imread('t.jpeg', cv2.IMREAD_COLOR)

                dst = cv2.cvtColor(src, cv2.COLOR_BGR2RGB)
                result = hands.process(dst)

                if result.multi_hand_landmarks:
                    for handLms in result.multi_hand_landmarks:
                        for id, lm in enumerate(handLms.landmark):
                            h, w, c = src.shape
                            cx, cy = int(lm.x * w), int(lm.y * h)

                            #print(cx, cy)
                            if id == 8:
                                cv2.circle(src, (cx, cy), 15, (0, 255, 0), cv2.FILLED)
                                print(cx,cy)

                        mpDraw.draw_landmarks(src, handLms)

                cv2.imwrite("hand.jpeg", src)
                print("손 인식 사진 저장 완료")
            
        except ConnectionAbortedError:
            break
        
        except ConnectionResetError:
            break
    
    client.close()


def checkStopSignal(client):
    # 단순히 두번 째 소켓에서 입력이 들어오면 바로
    # 첫번째 소켓의 프로세스(니카 서비스) 중지
    print("취소 서버 클라이언트 실행")
    client.recv(1024)
    print("===== 종료 명령을 받았습니다. =====")
    

## 메인
if __name__ == '__main__' :
    ### 메인 동작

    # 서버 소켓 객체 생성
    serverSock = socket(AF_INET, SOCK_STREAM) #두가지인자는 어드레스 패밀리, 소켓 타입 
    # '' = 포트 8080에 접속하는 모든 ip 허용

    serverSock.bind(('', 8081)) #서버 소켓에서는 bind해줘야함
    print("=== SERVER ON-LINE ===") # 서버 시작 알림
    cur_conn = 0

    serverSock.listen() # 대기열 같은 개념, 소켓 최대 인원이 아님

    # 총 두 번 수락
    mainClient, _ = serverSock.accept() # clientSock for main
    cur_conn += 1
    print(f'메인 : {mainClient}')

    subClient, _ = serverSock.accept() # subSock for sub
    cur_conn += 1
    print(f'서브 : {subClient}')

    
    
    while True:
        print("while문 실행")
        current_process = []
        print(f'클라이언트 소켓 확인: {subClient}')
        mainProcess = multiprocessing.Process(target=service, args=(mainClient,))
        subProcess = multiprocessing.Process(target=checkStopSignal, args=(subClient,))
       
        # 일단 연결 수락
        current_process.append(mainProcess)
        mainProcess.start()
        
        current_process.append(subProcess)
        subProcess.start()
        
        time.sleep(1)
        print("== 프로세스 확인 시작 ==")
        print(f'=> 프로세스 실행 확인 :{current_process}')
        
        while len(current_process) == 2:
            print("while문 도는 중")
            print(current_process)
            for i in current_process:
                if not i.is_alive():
                    #current_process.remove(i)
                    #i.terminate()
            #if len(current_process) != 2 :
                #print(len(current_process))
                    current_process.append("1")
                    break
            time.sleep(1) # 1초 간격마다 확인
        
        # 남은 프로세스 제거
        current_process.pop()
        for i in current_process:
            #print(i.Process(processID))
            
            i.terminate()
    
        
        mainProcess.join()
        subProcess.join()
        mainProcess.close()
        subProcess.close()
            
        print(f'재실행 전 확인 :{current_process}')
        
        subProcess = ""
        mainProcess = ""
            
        # 리스트 초기화
        current_process.clear()
        #print(len(current_process))
                
        print("서버 재시작 실행 ")
        
        time.sleep(5) # 안전빵 부팅
        
        
    print(f"현재 서비스 이용자: {cur_conn}")
    