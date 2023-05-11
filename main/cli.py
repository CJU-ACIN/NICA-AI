#client.py
import os
from socket import *
import multiprocessing, time, signal
import speech_recognition as sr  
from playsound import playsound   

# module
from module import speech2Text, handRecognize, ocr, face_recog
 
#--------------------------------- 커멘드 센터 ---------------------------------# 
# 어떤 명령인지 mqtt를 통해서 전달 (사물인식, 네비게이션, 책 읽기, 거리 측정)

call_nica = ['니카','니가','니까','니깐','리카']

def commandList(source,clientSock) :

    # 명령어 모음 사전
    command_dict = {
    '책': (ocr, clientSock, "book", source),                            # 책 읽기 모드
    '글자': (ocr, clientSock, "word", source),                           # 단어 읽기 모드
    '손': (handRecognize, clientSock, 'hand'),                          # 손으로 가리키는 사물 탐지
    '누구': (face_recog, clientSock, 'face', source),                    # 얼굴 인식 => 누구인지 알려줌
    '저장': (face_recog, clientSock, 'face_save', source),               # (인식대상) 사람 얼굴 저장
    }
    c = False
    i = 0

    while i < 4 :
        if i != 3 :
            playsound('settingvoice/good.mp3')
            command = speech2Text("[호출/명령]",source,10)                # 음성 명령어 입력 받음

            for command_dict_key, func_args in command_dict.items():    # 명령어 사전에서 함수와 인자를 받음
                if command_dict_key in command:                         # 음성 입력과 일치되는 함수 실행
                    func = func_args[0]
                    args = func_args[1:]
                    func(*args)
                    c = True
                    break
            else : playsound('settingvoice/re_voice_input.mp3')                # 해당하는 명령어를 찾을 수 없어요. 다시 말씀해 주세요.
            if c : break
        else :
            playsound('settingvoice/re_voice_end.mp3')                  # 해당하는 명령어를 찾을 수 없어요. 3회 이상 반복하여 대기 모드르 돌아갑니다.
        i+=1

#--------------------------------- 클라이언트 ---------------------------------# 

# 메인 서비스 (주로 호출 담당)
def service(clientSock):
    while True :

        # 마이크 
        with sr.Microphone(sample_rate=16000) as source :       
            result = speech2Text("[호출]",source,5)              # 음성 인식
            
            # 호출
            if any(word in result for word in call_nica) :             
                playsound('settingvoice/start.mp3')             # 안녕하세요 니카입니다. 무엇을 도와드릴까요?
                time.sleep(0.5)
                commandList(source,clientSock)                  # 명령어 판별

            elif '종료' in result :
                exit()
        
            time.sleep(1)


# 취소 클라이언트 => 서버에 취소 명령을 보냄
def cancelClient(clientSock) :
   
    for i in range(3) :                     # 3초 뒤에 작동
        print(i+1)
        time.sleep(1)
    
    print("취소 실행")
    clientSock.send("종료".encode())

    for i in range(10,0,-1) :               # 서버 재시작까지 10초 대기
        print(f'서버 재시작 까지 : {i}초')
        time.sleep(1)


#--------------------------------- 메인 ---------------------------------# 
if __name__ == '__main__' :

    server_address = '203.252.240.40'

    clientSock1 = socket(AF_INET, SOCK_STREAM)                                                  # 서비스 클라이언트 실행
    clientSock1.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1) # 포트 즉시 사용
    clientSock1.connect((server_address, 8081)) 
    print("서비스 클라이언트 연결 완료")

    time.sleep(2)

    clientSock = socket(AF_INET, SOCK_STREAM)                                                   # 취소 클라이언트 실행
    clientSock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1) # 포트 즉시 사용
    clientSock.connect((server_address, 8081)) 
    print("취소 클라이언트 연결 완료")

    mainService = multiprocessing.Process(target=service,args=(clientSock1,))
    mainService.start()

    while True :                                                                                # 취소 명령 루프
        text = input()

        if text == "종료" :                                                                      # 취소 명령 클라이언트 실행
            cancelProcess = multiprocessing.Process(target=cancelClient, args=(clientSock,))    
            cancelProcess.start()
            cancelProcess.join()                                                                # 클라이언트가 종료되기를 기다림
            cancelProcess.close()                                                               # 자원 반환 후 다시 취소 클라이언트 재시작

            print("서비스 종료 실행")
            os.kill(mainService.pid, signal.SIGTERM)
            mainService = multiprocessing.Process(target=service,args=(clientSock1,))
            mainService.start()

        elif text == "exit" :
            break

        time.sleep(0.5)



    


    
    

    


