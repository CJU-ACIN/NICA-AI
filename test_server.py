#server.py
from socket import *
import matplotlib.pyplot as plt
from PIL import Image
import cv2, pickle, struct, io
import numpy as np
import base64
from pororo import Pororo

serverSock = socket(AF_INET, SOCK_STREAM) #두가지인자는 어드레스 패밀리, 소켓 타입 
serverSock.bind(('', 8080)) #서버 소켓에서는 bind해줘야함, 
# ''이므로 8080번 포트에서 모든 인터페이스에게 연결하도록 한다.
print('[서버 준비 완료]')
serverSock.listen(1) #서버소켓에서만 쓰임,해당 소켓이 총 몇개의 동시접속까지를 허용수 인자

connectionSock, addr = serverSock.accept() 
print(str(addr),'에서 접속이 확인되었습니다.')

def recvall(sock, count):
    buf = b''
    while count:
        newbuf = sock.recv(count)
        if not newbuf: return None
        buf += newbuf
        count -= len(newbuf)
    return buf
while True :
    try :
        length = recvall(connectionSock,16)
        stringData = recvall(connectionSock, int(length))

        data = np.frombuffer(stringData, dtype='uint8')

        decimg=cv2.imdecode(data,1)
        cv2.imwrite("t.jpeg", decimg)

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

        # 클라이언트와 연결을 종료
        connectionSock.close()

    except Exception as e :
        print(e)
        break
        pass

