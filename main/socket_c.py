#client.py
import os
from socket import *
import cv2,time
from gtts import gTTS
from playsound import playsound
import numpy as np

def bookRead(sock) :

    def capVideo() :
        # 생성
        vid = cv2.VideoCapture(0)
        ret, frame = vid.read() 

        if ret :

            # 캡쳐한 사진 데이터 변환
            encode_param=[int(cv2.IMWRITE_JPEG_QUALITY),90]
            result, imgencode = cv2.imencode('.jpeg', frame, encode_param)
            data = np.array(imgencode)

            # 서버로 전송
            sock.sendall(str(len(data)).ljust(16).encode('utf-8'))
            time.sleep(0.5)
            sock.send(data.tobytes())
            print('메시지를 전송했습니다.')

            try :
                # 서버에서 처리한 음성데이터 텍스트 수신
                data = sock.recv(1024)
                speech_text = data.decode('utf-8')

                # TTS 음성 파일 생성 => 재생 => 삭제
                tts = gTTS(text=speech_text, lang='ko', slow=False)
                mp3_file = 'read.mp3'
                tts.save(mp3_file)
                playsound(mp3_file)
                os.remove(mp3_file)
                
            except :
                pass
        else :
            print("사진 캡쳐에 오류가 있습니다.")
            playsound('settingvoice/cap_error.mp3')
            capVideo()
            sock.close()

    capVideo() 