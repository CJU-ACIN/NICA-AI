# SERVER

from socket import *
import matplotlib.pyplot as plt
from PIL import Image
import cv2, pickle, struct, io
import numpy as np
import base64, time
from pororo import Pororo
import mediapipe as mp
import multiprocessing



def recvall(sock, count):
    buf = b''
    while count:
        newbuf = connectionSock.recv(count)
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


def doService(command, connectionSock):
    while True :
        try :
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

        except Exception:
            pass


def listen_button_value(connectionSock):
    connectionSock.recv(1024)
    print("중단 요청 받음!")

# 글로벌 변수 초기화


### 메인
if __name__ == "__main__":
    serverSock = socket(AF_INET, SOCK_STREAM) #두가지인자는 어드레스 패밀리, 소켓 타입 
    serverSock.bind(('', 6974)) #서버 소켓에서는 bind해줘야함, 
    # ''이므로 8080번 포트에서 모든 인터페이스에게 연결하도록 한다.
    print('=== 서버 준비 완료 ===')
    serverSock.listen(1) #서버소켓에서만 쓰임,해당 소켓이 총 몇개의 동시접속까지를 허용수 인자

    serverSock.listen() # 대기열 같은 개념, 소켓 최대 인원이 아님
    
    while True:
        process_list = [] # 프로세스 목록
        connectionSock, address = serverSock.accept()
        
        command = connectionSock.recv(1024).decode()
        print(f"서버 수신 명령 => {command}")
        
        # 프로세스 선언
        process_service = multiprocessing.Process(target = doService, args=(command, connectionSock)) # 서비스; OCR 등
        
        process_listen_button_value = multiprocessing.Process(target = listen_button_value, args=(connectionSock,)) # 정지 신호 대기
        
        # 프로세스를 리스트에 추가
        process_list.append(process_service)
        process_list.append(process_listen_button_value)
        
        process_service.start()
        process_listen_button_value.start()


        # 죽은 프로세스 리스트에서 제거
        while len(process_list) == 2:
            for i in process_list:
                if not i.is_alive():
                    process_list.remove(i)
            print("중단 요청 받음!")
            time.sleep(1)


        # 나머지 프로세스 전부 죽이기
        for i in process_list:
            i.terminate()
            print("모든 프로세스 중단!")
        
        
        # 프로세스 대기
        process_service.join()
        process_listen_button_value.join()
        
        print("2초 뒤, 클라이언트 연결 다시 받음")
        time.sleep(2) # 2초 뒤에 명령 수신 모드로 전환
    

