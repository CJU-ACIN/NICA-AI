#client.py
import os
from socket import *
import cv2,time
from gtts import gTTS
from playsound import playsound
import numpy as np
from whisper import whisper         # Speech to Text

def sendPhoto(sock,frame,type) :
    # 캡쳐한 사진 데이터 변환
    encode_param=[int(cv2.IMWRITE_JPEG_QUALITY),90]
    result, imgencode = cv2.imencode('.jpeg', frame, encode_param)
    data = np.array(imgencode)

    # 서버로 전송
    print(f"클라이언트 수신 명령 => {type}")
    sock.send(type.encode('utf-8'))
    sock.sendall(str(len(data)).ljust(16).encode('utf-8'))
    time.sleep(0.5)
    sock.send(data.tobytes())
    print('메시지를 전송했습니다.')

def ocr(sock,type,model,r,source) :

    # 음성 인식
    def speech2Text(work,source,time) :
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
    
    count = 0
    while count < 3 :
        
        # 생성
        vid = cv2.VideoCapture(0)
        ret, frame = vid.read() 

        if ret :
            # 인코딩 후 사진 전송
            sendPhoto(sock,frame,type)

            try :
                # 서버에서 처리한 음성데이터 텍스트 수신
                data = sock.recv(1024)
                speech_text = data.decode('utf-8')

                # 서버에서 글자를 인식하지 못 했을때
                if "글자를 탐지하지 못했어요..." == speech_text :
                    # 다시 재 촬영
                    playsound("settingvoice/re_vid_cap.mp3") # 글자를 탐지하지 못했어요 다시 탐지하겠습니다.
                    count += 1
                    time.sleep(2)
                    continue
                
                # 서버에서 글자를 인식 했을때
                else :
                    # TTS 음성 파일 생성 => 재생 => 삭제
                    tts = gTTS(text=speech_text, lang='ko', slow=False)
                    mp3_file = 'read.mp3'
                    tts.save(mp3_file)
                    playsound(mp3_file)
                    os.remove(mp3_file)
                    
                    # 명령어가 책 읽기 일때
                    if type == "book" :
                        playsound("settingvoice/next_page.mp3") # 다음 페이지로 넘겨주세요.
                        count = 0 
                        time.sleep(5) 
                        continue 

                    # 명령어가 글자 인식일떄
                    elif type == "word" :
                        
                        # 글주 추가 인식 여부 확인
                        playsound("settingvoice/word_end.mp3")
                        playsound('settingvoice/good.mp3')
                        result = speech2Text("[단어 재인식 여부]",source,5)

                        # 추가 인식
                        if "응" in result :
                            playsound("settingvoice/ok_re_recognize.mp3") # 네 알겠습니다. 다시 단어를 인식해볼게요.
                            count = 0
                            time.sleep(5)
                            continue
                        
                        # 추가 인식 종료
                        else : 
                        # elif "아니" in result :
                            playsound("settingvoice/no_re_recognize.mp3") # 네 알겠습니다. 대기 모드로 돌아가겠습니다.
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

def handRecognize(sock,type,model,r,source) :

    # 생성
    vid = cv2.VideoCapture(0)
    ret, frame = vid.read() 

    if ret :
        # 인코딩 후 사진 전송
        sendPhoto(sock,frame,type)

        print("성공")

    # opencv 캡쳐 오류 시 다시 캡쳐
    else :
        print("사진 캡쳐에 오류가 있습니다.")
        playsound('settingvoice/cap_error.mp3')
        
