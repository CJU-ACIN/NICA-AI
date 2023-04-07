#server.py
from socket import *
import matplotlib.pyplot as plt
from PIL import Image
import cv2, pickle, struct, io
import numpy as np
import base64, time
from pororo import Pororo
import mediapipe as mp
import threading # 멀티스레드를 통한 병렬처리

# 작업 명령 boolean
serviceToy_active = True
stopService_active = True

# 결과값
result_toy = ""

def recvall(sock, count):
        buf = b''
        while count:
            newbuf = sock.recv(count)
            if not newbuf: return None
            buf += newbuf
            count -= len(newbuf)
        return buf

def imageDecode(connectionSock) :
    length = recvall(connectionSock,16)
    stringData = recvall(connectionSock, int(length))

    data = np.frombuffer(stringData, dtype='uint8')

    decimg=cv2.imdecode(data,1)
    cv2.imwrite("t.jpeg", decimg)

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
            connectionSock.send("중단".encode('utf-8'))
            
            break

        result_toy = "결과값"
        
    return result_toy

def service(connectionSock,addr) :

    connectionSock.send("SUCCESS".encode('utf-8'))
    print(f"{addr}에서 접속 성공")
    
    while True:
        try :
            print(f"{addr}의 명령 대기중")
            # 텍스트 형식으로 클라이언트로부터 request 받기
            request = connectionSock.recv(1024).decode('utf-8')
            
            print(f"{addr}의 요청: {request} ... 처리 중")

            command = connectionSock.recv(1024)
            command = command.decode('utf-8')
            print(f"서버 수신 명령 => {command}")
            
            if command == "book" or command == "word" :
                
                # 이미지 디코딩 후 저장
                imageDecode(connectionSock)

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
                imageDecode(connectionSock)

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
        
    connectionSock.close()

# ================================= 시작 ================================
serverSock = socket(AF_INET, SOCK_STREAM) #두가지인자는 어드레스 패밀리, 소켓 타입 
serverSock.bind(('', 8080)) #서버 소켓에서는 bind해줘야함, 
# ''이므로 8080번 포트에서 모든 인터페이스에게 연결하도록 한다.

print("=== SERVER ON-LINE ===") # 서버 시작 알림

max_conn = 2 # 최대 접속자 2명
cur_conn = 0 # 현재 접속자

while True:
    serverSock.listen(1) #서버소켓에서만 쓰임,해당 소켓이 총 몇개의 동시접속까지를 허용수 인자
    connectionSock, addr = serverSock.accept() 
    print(str(addr),'에서 접속이 확인되었습니다.')
    cur_conn += 1

    # 인원 초과 안될 때
    if cur_conn <= max_conn:
        thread_service = threading.Thread(target=service, args=(connectionSock, addr))
        thread_service.start()
    
    else:
        cur_conn -= 1
        #connectionSock.send('NG'.encode('utf-8'))
        print("접속량이 초과 했습니다.")
        connectionSock.close()
        
    print(f"현재 서비스 이용자: {cur_conn}")


    