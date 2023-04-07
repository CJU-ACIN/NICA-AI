#client.py
import os
from socket import *
import multiprocessing, time, cv2, signal
import speech_recognition as sr  
from whisper import whisper
from playsound import playsound   
import numpy as np
from gtts import gTTS
 

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


# 사진 인코딩 후 전송 함수
def sendPhoto(sock,frame,type) :

    encode_param=[int(cv2.IMWRITE_JPEG_QUALITY),90]                         # 캡쳐한 사진 데이터 변환
    result, imgencode = cv2.imencode('.jpeg', frame, encode_param)
    data = np.array(imgencode)

    print(f"클라이언트 수신 명령 => {type}")
    sock.send(type.encode('utf-8'))                                         # 어떤 명령인지 서버로 전송
    sock.sendall(str(len(data)).ljust(16).encode('utf-8'))                  # 사진 데이터 인코딩 후 전송
    time.sleep(0.5)
    sock.send(data.tobytes())
    print('메시지를 전송했습니다.')


# STT 모듈
def speech2Text(work,source,time) :

    r = sr.Recognizer()
    model = whisper.load_model("base")
    
    try :
        print(f'{work} => 음성을 입력 준비 완료')
        audio = r.listen(source,timeout=time,phrase_time_limit=time)         # 음성 입력

        with open(f'voice/input.wav',"wb") as f :
            f.write(audio.get_wav_data())                                    # 입력 받은 음성 저장

        audio = whisper.load_audio("voice/input.wav")                        # 저장된 음성 파일로 텍스트 추출
        audio = whisper.pad_or_trim(audio)
        mel = whisper.log_mel_spectrogram(audio).to(model.device)
        _, probs = model.detect_language(mel)
        
        print(f"- 감지된 언어 : {max(probs, key=probs.get)}")                   # 입력 값 확인 후 반환
        options = whisper.DecodingOptions(fp16 = False)
        result = whisper.decode(model, mel, options)
        os.remove('voice/input.wav')

        print(f'- 인식 결과 : {result.text}')                                   # Text 출력     
        return result.text
    
    except Exception as e:
        print(e)
        return "none"


# 손 위치 인식 모듈
def handRecognize(sock,type) :

    vid = cv2.VideoCapture(0)                       # 캡쳐 객체 생성
    ret, frame = vid.read()                         

    if ret :
        # 인코딩 후 사진 전송
        sendPhoto(sock,frame,type)
        data = sock.recv(1024)                              # 서버에서 처리한 음성데이터 텍스트 수신
        speech_text = "인식한 물체는 "+ data.decode('utf-8') + " 입니다."

        print("성공")

        tts = gTTS(text=speech_text, lang='ko', slow=False)         # TTS 음성 파일 생성 => 재생 => 삭제
        mp3_file = 'read.mp3'
        tts.save(mp3_file)
        playsound(mp3_file)
        os.remove(mp3_file)

    # opencv 캡쳐 오류 시 다시 캡쳐
    else :
        print("사진 캡쳐에 오류가 있습니다.")
        playsound('settingvoice/cap_error.mp3')     


# OCR 모듈
def ocr(sock,type,source) :

    count = 0
    while count < 3 :

        print("캡쳐 실행")
        vid = cv2.VideoCapture(0)                                   # 객체 생석
        ret, frame = vid.read() 
        
        if ret :
            sendPhoto(sock,frame,type)                              # 인코딩 후 사진 전송
            vid.release()                                           # 캡쳐 객체 반환

            try :
                data = sock.recv(1024)                              # 서버에서 처리한 음성데이터 텍스트 수신
                speech_text = data.decode('utf-8')

                # 서버에서 글자를 인식하지 못 했을때
                if "글자를 탐지하지 못했어요..." == speech_text :
                    playsound("settingvoice/re_vid_cap.mp3")        # 글자를 탐지하지 못했어요 다시 탐지하겠습니다.
                    count += 1
                    time.sleep(2)
                    continue                                        # 다시 재 촬영

                elif "종료" == speech_text:
                    break
                
                # 서버에서 글자를 인식 했을때
                else :
                    tts = gTTS(text=speech_text, lang='ko', slow=False)         # TTS 음성 파일 생성 => 재생 => 삭제
                    mp3_file = 'read.mp3'
                    tts.save(mp3_file)
                    playsound(mp3_file)
                    os.remove(mp3_file)
                    
                    # 명령어가 책 읽기 일때
                    if type == "book" :
                        playsound("settingvoice/next_page.mp3")                 # 다음 페이지로 넘겨주세요.
                        count = 0 
                        time.sleep(5) 
                        continue 

                    # 명령어가 글자 인식일떄
                    elif type == "word" :
                        playsound("settingvoice/word_end.mp3")
                        playsound('settingvoice/good.mp3')
                        result = speech2Text("[단어 재인식 여부]",source,5)         # 글자 추가 인식 여부 확인

                        # 추가 인식
                        if "응" in result :
                            playsound("settingvoice/ok_re_recognize.mp3")       # 네 알겠습니다. 다시 단어를 인식해볼게요.
                            count = 0
                            time.sleep(5)
                            continue
                        
                        # 추가 인식 종료
                        else : 
                            playsound("settingvoice/no_re_recognize.mp3")       # 네 알겠습니다. 대기 모드로 돌아가겠습니다.
                            count = 0
                            break
                        
            except Exception as e :
                print(e)
                pass
        
        # opencv 캡쳐 오류 시 다시 캡쳐
        else :
            print("사진 캡쳐에 오류가 있습니다.")
            playsound('settingvoice/cap_error.mp3')
            count += 1
            time.sleep(2)
            continue

    # 3회 글자 인식 실패
    if count >= 2 : playsound('settingvoice/count_out_read_book.mp3') # 3회 이상 틀려서 대기모드로 돌아갑니다.


# 어떤 명령인지 mqtt를 통해서 전달 (사물인식, 네비게이션, 책 읽기, 거리 측정)
def commandList(source,clientSock) :
   
    for i in range(3) :
        playsound('settingvoice/good.mp3')
        command = speech2Text("[명령]",source,10)                        # 음성 명령어 입력 받음
    
        if i != 3 :

            if '책' in command :
                playsound('settingvoice/startBook.mp3')                 # 네 알겠습니다. 책 읽기를 도와드릴게요.
                ocr(clientSock,"book",source)                           # (명령애 따라서) 카메라 작동 및 소켓 통신 => 독서 모드
                break

            elif '글자' in command :
                playsound('settingvoice/start_word_recognize.mp3')      # 네 알겠습니다. 책 읽기를 도와드릴게요.
                ocr(clientSock,"word",source)                           # (명령애 따라서) 카메라 작동 및 소켓 통신 => 글자 인식 모드
                break

            elif '손' in command :
                handRecognize(clientSock,"hand")                        # (명령애 따라서) 카메라 작동 및 소켓 통신 => 손 인식 모드
                break

            elif '니카' in command or '니가' in command :
                playsound('settingvoice/start.mp3')                     # 안녕하세요 니카입니다. 무엇을 도와드릴까요?
                time.sleep(0.5)

            else :
                playsound('settingvoice/re_voice_input.mp3')            # 해당하는 명령어를 찾을 수 없어요. 다시 말씀해 주세요.
                time.sleep(0.5)
        else :
            playsound('settingvoice/re_voice_end.mp3')                  # 해당하는 명령어를 찾을 수 없어요. 3회 이상 반복하여 대기 모드르 돌아갑니다.


# 메인 서비스 (주로 호출 담당)
def service(clientSock):
    while True :

        # 마이크 
        with sr.Microphone(sample_rate=16000) as source :       
            result = speech2Text("[호출]",source,5)              # 음성 인식
            
            # 호출
            if '니카' in result or '니가' in result :             
                playsound('settingvoice/start.mp3')             # 안녕하세요 니카입니다. 무엇을 도와드릴까요?
                time.sleep(0.5)
                commandList(source,clientSock)                  # 명령어 판별

            elif '종료' in result :
                exit()
        
            time.sleep(1)


#--------------------------------- 메인 ---------------------------------# 
if __name__ == '__main__' :

    clientSock1 = socket(AF_INET, SOCK_STREAM)        # 서비스 클라이언트 실행
    server_address = '203.252.240.40'
    clientSock1.connect((server_address, 8081)) 
    print("서비스 클라이언트 연결 완료")

    time.sleep(2)

    clientSock = socket(AF_INET, SOCK_STREAM)         # 취소 클라이언트 실행
    server_address = '203.252.240.40'
    clientSock.connect((server_address, 8081)) 
    print("취소 클라이언트 연결 완료")

    mainService = multiprocessing.Process(target=service,args=(clientSock1,))
    mainService.start()

    while True :                                                                                # 취소 명령 루프
        text = input('명령 입력 : ')

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



    


    
    

    


