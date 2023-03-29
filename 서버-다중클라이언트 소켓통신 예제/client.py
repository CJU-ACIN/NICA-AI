#client.py
from socket import *

clientSock = socket(AF_INET, SOCK_STREAM)
server_address = '192.168.0.2'

clientSock.connect((server_address, 8081)) 

data = clientSock.recv(1024) # 서버 접속 성공여부 받기
data = data.decode('utf-8')

print(f"서버 접속 상황: {data}")

# 성공
if data == "SUCCESS":
    print('연결 확인 됐습니다.')
    while True :
        text=input("입력하세요 : ")
        if text == '종료':
            break
        
        clientSock.send(text.encode('utf-8'))

        data = clientSock.recv(1024)
        print('받은 데이터 : ', data.decode('utf-8'))

# 실패
elif data == "NG":
    print("서버 접속 실패!")
    clientSock.close()