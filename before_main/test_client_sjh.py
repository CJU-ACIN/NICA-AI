from socket import *
import threading, time

def serverConnect(port) :
    clientSock = socket(AF_INET, SOCK_STREAM)
    clientSock.connect(('203.252.240.40', port)) 
    print(f'port => {port} 연결 확인 됐습니다.')

    return clientSock

def cancelRequest():
    cancel_clientSock = serverConnect(8082)

    while True :
        time.sleep(0.5) # 지연 있어야 스레드 끝난걸 감지
        text=input("취소 명령 수신 대기중 : ")

        cancel_clientSock.send(text.encode('utf-8'))
        

        if text == '1':
            time.sleep(3)
            s1= serverConnect(8080)
    
        elif text == '2' :
            time.sleep(3)
            s2 = serverConnect(8081) 
            

        elif text == '종료' :
            cancel_client.close()
            break

        

def service(port) :
    serverConnect(port)


if __name__ == "__main__":
    # cancel_client = threading.Thread(target=cancelRequest(),daemon=True)
    # time.sleep(1)
    # client_01 = threading.Thread(target=serverConnect(8080))
    # time.sleep(5)
    # client_02 = threading.Thread(target=serverConnect(8081))  
    cancel_client = threading.Thread(target=cancelRequest())
    cancel_client.start()
     
    
    


    

