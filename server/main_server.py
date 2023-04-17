#server.py
import os
import shutil
from socket import *
# import threading # 멀티스레드를 통한 병렬처리
import time, math # 작업시간 예시
import multiprocessing
from multiprocessing import set_start_method
import torch

#server.py
from socket import *
import face_recognition
import matplotlib.pyplot as plt
from PIL import Image
import cv2, pickle, struct, io
import numpy as np
import base64, time
from pororo import Pororo
import mediapipe as mp

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


def handPoint(x1,y1,x2,y2,src,where_hand) :

    if x1 == x2 :
        grad = 0
    else : 
        grad = round((y2 - y1) / (x2 - x1),1)

    d = int((math.sqrt((x2 - x1)**2 + (y2 - y1)**2))/2)

    if where_hand == True :  # 오른손
        x = x1 - d
    else :                   # 왼손
        x = x1 + d

    y = int(grad * (x - x1) + y1)

    cv2.line(src, (x1, y1), (x2, y2), (0, 255, 0), 3)
    cv2.circle(src, (x, y), 3, (0, 0, 255), cv2.FILLED)

    return (x, y)


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
                imageDecode(connectionSock)

                img = "t.jpeg"
                #device = torch.device("cpu")
                ocr = Pororo(task="ocr", lang='ko',)
                
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

            # 손 인식 일 경우
            elif 'hand' in command :
                # 객체 선언
                mpHands = mp.solutions.hands
                hands = mpHands.Hands()
                #mpDraw = mp.solutions.drawing_utils

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

                            if id == 8 :
                                x1, y1 = cx, cy
                            elif id == 7 :
                                x2, y2 = cx, cy
                                
                    if x1<x2 :
                        xy_tuple = handPoint(x1,y1,x2,y2,src,True)
                        #reuslt_text = whatIsThat(org, xy_tuple) # 아예 이미지 원본값. 점이 찍혀있는 이미지면 안되니깐
                        #print(reuslt_text)

                    else :
                        xy_tuple = handPoint(x1,y1,x2,y2,src,False)
                        #reuslt_text = whatIsThat(org, xy_tuple) # 아예 이미지 원본값. 점이 찍혀있는 이미지면 안되니깐
                        #print(reuslt_text)
                    
                    os.rename('t.jpeg', f'{xy_tuple}.jpeg') # 손 끝점이 있는 곳으로 파일 이름 변경
                    print("사진 이름 변경 완료")
                    shutil.move(f'{xy_tuple}.jpeg', f"./yolo_images_result/{xy_tuple}.jpeg") # 이미지 파일 이동
                    print("사진 이동 완료")
                    time.sleep(5)
                    result_object = str(os.listdir('./yolo_images_result/result/')[0])
                    connectionSock.send(result_object.split(".")[0].encode('utf-8'))
                    
                    os.remove(f"./yolo_images_result/result/{result_object}")
                    print("== 물체 인식 완료 ==")

            elif 'face' in command :

                length = recvall(connectionSock,16)
                stringData = recvall(connectionSock, int(length))
                data = np.frombuffer(stringData, dtype='uint8')
                decimg=cv2.imdecode(data,1)
                cv2.imwrite("./input_unknown_face/input_face_data.jpeg", decimg)

                # 등록된 사람 얼굴 목록 불러오기
                known_faces = [face_recognition.load_image_file(f"./known_faces/{x}") for x in sorted(os.listdir('./known_faces/'))]
                # 얼굴 특징점 인코딩
                known_encodings = [face_recognition.face_encodings(x)[0] for x in known_faces]
                # 이름 목록
                known_names = [x.split('.')[0] for x in sorted(os.listdir('./known_faces/'))]

                input_image = face_recognition.load_image_file("./input_unknown_face/input_face_data.jpeg") # 입력 사진 불러오기

                select_image = input_image 

                try:
                    # check if image has face
                    test_image_face_locations = face_recognition.face_locations(select_image)

                    # encode test image
                    test_image_face_encoding = face_recognition.face_encodings(select_image, test_image_face_locations)

                    result_boolean = []
                    for fe in test_image_face_encoding:
                        # put list of arrays
                        # if simularity >= 50%, it returns true
                        result_boolean.append(face_recognition.compare_faces(known_encodings, fe, tolerance=0.5))

                    print(result_boolean) # ex) [[True, False]] or [[True, False], [False, False]]

                    result_name = []
                    for res in result_boolean:
                        # if [[False, False]]
                        if sum(res) == 0:
                            pass

                        else:
                            result_name.append(known_names[np.argmax(res)])
                    
                    name_text = "확인한 사람은 "
                    
                    for name in result_name :
                        name_text += f"{name}, "
                    name_text += "입니다."

                    print(name_text)
                    connectionSock.send(name_text.encode('utf-8'))
                    os.remove(f"./input_unknown_face/input_face_data.jpeg")

                except IndexError:
                    print("인식된 사람이 없습니다.")
                    pass

            else : # 사람 얼굴 등록 시킬때 == 타입이 사람 이름일 경우 == commad가 사람 이름인 경우

                name = command  # 커멘드는 저장할 사람 이름

                length = recvall(connectionSock,16)
                stringData = recvall(connectionSock, int(length))
                data = np.frombuffer(stringData, dtype='uint8')
                decimg=cv2.imdecode(data,1)
                
                #if name not in os.listdir('./known_faces/') : # 아는 사람 목록에 사진 저장 (같은 이름 또 입력 했을떄 처리 필요함)
                cv2.imwrite(f"./known_faces/{name}.jpeg", decimg) 

                connectionSock.send(f'{name} 님이 얼굴 인식 시스템에 등록 되었습니다.'.encode('utf-8'))

        except ConnectionAbortedError:
            break
        
        except ConnectionResetError:
            break
    
    #client.close()


def checkStopSignal(client):
    # 단순히 두번 째 소켓에서 입력이 들어오면 바로
    # 첫번째 소켓의 프로세스(니카 서비스) 중지
    print("취소 서버 클라이언트 실행")
    client.recv(1024)
    print("===== 종료 명령을 받았습니다. =====")
    

## 메인
if __name__ == '__main__' :

    #set_start_method('spawn')
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
    print(f'서브 : {subClient}\n')

    
    
    while True:
       
        #print("while문 실행")
        current_process = []
        #print(f'클라이언트 소켓 확인: {subClient}')
        #multi.set_start_method('spawn')
        mainProcess = multiprocessing.Process(target=service, args=(mainClient,))
        subProcess = multiprocessing.Process(target=checkStopSignal, args=(subClient,))
       
        # 일단 연결 수락
        current_process.append(mainProcess)
        mainProcess.start()
        
        current_process.append(subProcess)
        subProcess.start()
        
        time.sleep(1)
        print("== 프로세스 확인 시작 ==")
        #print(f'=> 프로세스 실행 확인 :{current_process}')
        
        while len(current_process) == 2:
            #print("while문 도는 중")
            #print(current_process)
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
            
        #print(f'재실행 전 확인 :{current_process}')
        
        subProcess = ""
        mainProcess = ""
            
        # 리스트 초기화
        current_process.clear()
        #print(len(current_process))
                
        print("서버 재시작 실행 ")
        
        time.sleep(5) # 안전빵 부팅
        
    