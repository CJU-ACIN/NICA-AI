import multiprocessing
import time
from socket import *



def foo(clientSock):    
    print("FOO ACITVE")
    time.sleep(5)
    clientSock.send("FOO".encode())
    
    


def foo1():
    global a
    while not a:
        print("foo1 ACTIVE")
        time.sleep(12.5)
        a = True
    
    print("END foo1")
    


def createSock():
    clientSock = socket(AF_INET, SOCK_STREAM)
    print(f'클라이언트 소켓 : {clientSock}')
    return clientSock


a = False

myClientSock = createSock()
p = multiprocessing.Process(target = foo, args=(myClientSock,))
p1 = multiprocessing.Process(target = foo1) # 취소 대기
print(f'p1 확인 :{p1.is_alive()}')
pl = []   

if __name__ == "__main__":
    server_address = "127.0.0.1"
    print(myClientSock.connect((server_address, 6974)))
    print("START")

    pl.append(p)
    pl.append(p1)
    
    print(pl)
    p.start()
    p1.start()
    
    print(len(pl))
    while len(pl) == 2:
        for i in pl:
            if not i.is_alive():
                pl.remove(i)
        print(pl)
        time.sleep(0.1)
    
    for proc in pl:
        proc.terminate()
    print(len(pl))
    
    p.join()
    p1.join()
    
    print("END ALL")
