# CLIENT.py

## Import
from socket import * # 서버-클라이언트 통신
import threading # 스레드로 관리: 서버-클라이언트 상태 송-수신
import multiprocessing # 멀티프로세스로 관리: 자체적인 기능 동작
import time # 스레드 및 프로세스에서 지연시간 탐지





if __name__ == "__main__":
    # 서버 주소
    server_address = "203.252.230.246"
    
    # 클라이언트 소켓 객체 초기화
    clientSock = socket(AF_INET, SOCK_STREAM)
    
    # 서버로 연결 시도
    clientSock.connect((server_address, 8081))

    # 서버에서 접속 성공여부 메시지 받기 (OK / NG)
    connect_status = clientSock.recv(1024).decode("utf-8")

    
    # 접속 성공 OK
    if connect_status == "OK":
        print("서버와 연결 성공!")
        

        while True:
            ...

    # 접속 실패 NG (원인: 서버 최대 인원 제한 등)
    else:
        ...