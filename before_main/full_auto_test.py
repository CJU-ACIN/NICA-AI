import os
import time, cv2  
import numpy as np

from whisper import whisper         # Speech to Text
from gtts import gTTS               # Text to Speech
import speech_recognition as sr     # 음성 인식
from playsound import playsound     # 파이썬 음성 파일 재생 => 경로에 특수문자 들어가면 안됨

from socket import *

from socket_c import ocr, handRecognize

# 라즈베리파이에서 시스템 호출를 위해 사용
# 2023.03.30
# 자동으로 음성 입력을 받고 이를 텍스트로 전환해줌

# 기본 세팅
model = whisper.load_model("base")
r = sr.Recognizer()

# 음성 인식
def speech2Text(work,source,time) :

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

def commandList(source) :
    # 소켓 통신 세팅
    clientSock = socket(AF_INET, SOCK_STREAM)
    clientSock.connect(('203.252.240.40', 8080)) 
    print('연결 확인 됐습니다.')

    for i in range(3) :
        # 음성 명령어 입력 받음
        playsound('settingvoice/good.mp3')
        command = speech2Text("[명령]",source,10)
    
        if i != 3 :
            # 어떤 명령인지 mqtt를 통해서 전달 (사물인식, 네비게이션, 책 읽기, 거리 측정
            if '책' in command :
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


            elif '니카' in command or '니가' in command :
                playsound('settingvoice/start.mp3') # 안녕하세요 니카입니다. 무엇을 도와드릴까요?
                time.sleep(0.5)

            else :
                playsound('settingvoice/re_voice_input.mp3') # 해당하는 명령어를 찾을 수 없어요. 다시 말씀해 주세요.
                time.sleep(0.5)
        else :
            playsound('settingvoice/re_voice_end.mp3') # 해당하는 명령어를 찾을 수 없어요. 3회 이상 반복하여 대기 모드르 돌아갑니다.

playsound('settingvoice/system_start.mp3') # 니카 온라인

while True :
    # 마이크 
    with sr.Microphone(sample_rate=16000) as source:

        # 음성 인식
        result = speech2Text("[호출]",source,5)

        # 호출
        if '니카' in result or '니가' in result :
            playsound('settingvoice/start.mp3') # 안녕하세요 니카입니다. 무엇을 도와드릴까요?
            time.sleep(0.5)

            # 명령어 판별
            commandList(source)

        elif '종료' in result :
            exit()
        
        time.sleep(1)