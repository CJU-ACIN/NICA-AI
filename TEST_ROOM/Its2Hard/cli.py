### CLIENT

### Import
import multiprocessing                      # 중지 스위치
from socket import *                        # 서버-클라이언트 통신
import time
import os

from whisper import whisper                 # Speech to Text
from gtts import gTTS                       # Text to Speech
import speech_recognition as sr             # 음성 인식
from playsound import playsound             # 파이썬 음성 파일 재생 => 경로에 특수문자 들어가면 안됨
from commands import ocr, handRecognize     # 제공 서비스
import random


### 함수 선언

# 음성 인식
def speech2Text(work,source,time):
    global r
    
    try :
        # 음성 입력
        print(f'{work} => 음성을 입력 준비 완료')
        audio = r.listen(source,timeout=time,phrase_time_limit=time)

        # 입력 받은 음성 저장
        with open(f'voice/input.wav',"wb") as f :
            f.write(audio.get_wav_data())

        # 저장된 음성 파일로 텍스트 추출
        audio = whisper.load_audio("voice/input.wav")
        audio = whisper.pad_or_trim(audio)
        mel = whisper.log_mel_spectrogram(audio).to(model.device)
        _, probs = model.detect_language(mel)
        
        # 입력 값 확인 후 반환
        print(f"- 감지된 언어 : {max(probs, key=probs.get)}")
        options = whisper.DecodingOptions(fp16 = False)
        result = whisper.decode(model, mel, options)
        os.remove('voice/input.wav')

        # Text 출력
        print(f'- 인식 결과 : {result.text}')
        return result.text
    
    except Exception as e:
        print(e)
        return "none"



def commandList(source, clientSock):
    for i in range(3) :
        # 음성 명령어 입력 받음
        playsound('settingvoice/good.mp3')
        command = speech2Text("[명령]",source,3)
    
        if i != 3 :
            # 어떤 명령인지 mqtt를 통해서 전달 (사물인식, 네비게이션, 책 읽기, 거리 측정
            if '책' in command or 'next' in command or 'Next' in command:
                playsound('settingvoice/startBook.mp3') # 네 알겠습니다. 책 읽기를 도와드릴게요.

                # (명령애 따라서) 카메라 작동 및 소켓 통신
                ocr(clientSock,"book",model,r,source) # => 독서 모드
                break

            elif '글자' in command :
                playsound('settingvoice/start_word_recognize.mp3') # 네 알겠습니다. 책 읽기를 도와드릴게요.

                # (명령애 따라서) 카메라 작동 및 소켓 통신
                ocr(clientSock,"word",model,r,source) # => 글자 인식 모드
                break

            elif '손' in command :
                # (명령애 따라서) 카메라 작동 및 소켓 통신
                handRecognize(clientSock,"hand",model,r,source) # => 글자 인식 모드
                break


            elif '니카' in command or '니가' in command or '안녕' in command or '안녕니깐' in command or '일번' in command :
                playsound('settingvoice/start.mp3') # 안녕하세요 니카입니다. 무엇을 도와드릴까요?
                time.sleep(0.5)

            else :
                playsound('settingvoice/re_voice_input.mp3') # 해당하는 명령어를 찾을 수 없어요. 다시 말씀해 주세요.
                time.sleep(0.5)
                
        else :
            playsound('settingvoice/re_voice_end.mp3') # 해당하는 명령어를 찾을 수 없어요. 3회 이상 반복하여 대기 모드르 돌아갑니다.
            
            

def call_NICA(clientSock):
    while True:
        # 마이크 
        with sr.Microphone(sample_rate=16000) as source:
            
            playsound('settingvoice/system_start.mp3') # 니카 온라인
            # 음성 인식
            result = speech2Text("[호출]",source,3)

            # 호출
            if '니카' in result or '니가' in result or 'next' in result:
                playsound('settingvoice/start.mp3') # 안녕하세요 니카입니다. 무엇을 도와드릴까요?
                time.sleep(0.5)

                # 명령어 판별
                commandList(source, clientSock)
                

            elif '종료' in result :
                exit()
            time.sleep(0.5) # 0.5초 대기
            

def read_button_value(client_socket):
    btn_value = False # 중지 버튼 안 누름
    
    while not btn_value: # 라즈베리파이 버튼값 계속 받아오기
        time.sleep(120) # n초 뒤 중지 버튼 누름
        btn_value = True # 중지 버튼 누름
        # btn_value = 0
    
    client_socket.send('STOP'.encode())
    
    print("중단 요청 확인!")
    

# 글로벌 변수 초기화
button_value = 0 # 0 ~ 1 사이의 랜덤 실수 값


# 기본 세팅
model = whisper.load_model("base")
r = sr.Recognizer()




# if __name__ == "__main__" 에 프로세스 모듈 선언해야함, 아니면 에러 (무한재귀호출 에러)
### 메인
if __name__ == "__main__":
    server_address = "203.252.240.40" # 서버 주소
    port_num = 6974
    # 무한 반복
    while True:
        try:
            
            client_socket = socket(AF_INET, SOCK_STREAM)
            client_socket.connect((server_address, port_num))
            process_list = []
            
            # 프로세스 선언
            process_call_NICA = multiprocessing.Process(target = call_NICA, args = (client_socket,))
            process_read_button_value = multiprocessing.Process(target = read_button_value, args = (client_socket,))
            
            # 프로세스를 리스트에 추가
            process_list.append(process_call_NICA)
            process_list.append(process_read_button_value)
            
            # 음성 인식
            process_call_NICA.start()
            process_read_button_value.start()
            
            
            
            while len(process_list) == 2:
                for i in process_list:
                    if not i.is_alive():
                        process_list.remove(i)
                        
                print(process_list)
                time.sleep(1.5)
        
            for i in process_list:
                i.terminate()
                print("모든 프로세스 중단!")
            
            # 프로세스 종료 대기
            process_call_NICA.join()
            process_read_button_value.join()
            
            print("3초 뒤, 서버로 재접속 시도")
            time.sleep(6) # 6초 뒤 접속끊고 다시접속
            client_socket.close()
        
        
        except Exception:
            print("3초 뒤, 서버로 재접속 시도")
            time.sleep(6) # 6초 뒤 접속끊고 다시접속
            client_socket.close()
            port_num += 1
            pass    
        
    