#client.py
from socket import *
import multiprocessing, time


def cancelClient(clientSock) :

    

    #text=input("입력해줘세요 : ")
    for i in range(3) :
        print(i+1)
        time.sleep(1)
    
    print("취소 실행")
    clientSock.send("종료".encode())

    for i in range(10,0,-1) :
        print(f'서버 종료 까지 : {i}초')
        time.sleep(1)

    #time.sleep(100)



## 메인
if __name__ == '__main__' :
    
    # 서비스 클라이언트 실행
    clientSock1 = socket(AF_INET, SOCK_STREAM)
    server_address = '203.252.240.40'

    clientSock1.connect((server_address, 8081)) 
    print("서비스 연결 완료")
    #clientSock1.send('서비스'.encode())

    time.sleep(3)

    print("취소 클라이언트 실행")
    clientSock = socket(AF_INET, SOCK_STREAM)
    server_address = '203.252.240.40'

    clientSock.connect((server_address, 8081)) 
    print("취소 클라이언트 연결 완료")

    while True :
        text = input('명령 입력 : ')

        if text == "종료" :
            # 취소 명령 클라이언트
            cancelProcess = multiprocessing.Process(target=cancelClient, args=(clientSock,))
            cancelProcess.start()

            cancelProcess.join()
            cancelProcess.close()
        elif text == "exit" :
            break

        time.sleep(0.5)



    


    
    

    


