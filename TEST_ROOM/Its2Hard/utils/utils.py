import utils

# 음성 인식
def speech2Text(work,source,time,r,model):
    #global r
    
    try :
        # 음성 입력
        print(f'{work} => 음성을 입력 준비 완료')
        audio = r.listen(source,timeout=time,phrase_time_limit=time)

        # 입력 받은 음성 저장
        with open(f'voice/input.wav',"wb") as f :
            f.write(audio.get_wav_data())

        # 저장된 음성 파일로 텍스트 추출
        audio = utils.whisper.load_audio("voice/input.wav")
        audio = utils.whisper.pad_or_trim(audio)
        mel = utils.whisper.log_mel_spectrogram(audio).to(model.device)
        _, probs = model.detect_language(mel)
        
        # 입력 값 확인 후 반환
        print(f"- 감지된 언어 : {max(probs, key=probs.get)}")
        options = utils.whisper.DecodingOptions(fp16 = False)
        result = utils.whisper.decode(model, mel, options)
        utils.os.remove('voice/input.wav')

        # Text 출력
        print(f'- 인식 결과 : {result.text}\n')
        return result.text
    
    except Exception as e:
        print(f'STT 오류 : {e}\n')
        return "none"



def commandList(source, clientSock,r):
    model = utils.whisper.load_model("base")

    for i in range(3) :
        # 음성 명령어 입력 받음
        utils.playsound('settingvoice/good.mp3')
        command = speech2Text("[명령]",source,3,r,model)
    
        if i != 3 :
            # 어떤 명령인지 mqtt를 통해서 전달 (사물인식, 네비게이션, 책 읽기, 거리 측정
            if '책' in command or 'next' in command or 'Next' in command:
                utils.playsound('settingvoice/startBook.mp3') # 네 알겠습니다. 책 읽기를 도와드릴게요.

                # (명령애 따라서) 카메라 작동 및 소켓 통신
                ocr(clientSock,"book",model,r,source) # => 독서 모드
                break

            elif '글자' in command :
                utils.playsound('settingvoice/start_word_recognize.mp3') # 네 알겠습니다. 책 읽기를 도와드릴게요.

                # (명령애 따라서) 카메라 작동 및 소켓 통신
                ocr(clientSock,"word",model,r,source) # => 글자 인식 모드
                break

            elif '손' in command :
                # (명령애 따라서) 카메라 작동 및 소켓 통신
                handRecognize(clientSock,"hand",model,r,source) # => 글자 인식 모드
                break


            elif '니카' in command or '니가' in command or '안녕' in command or '안녕니깐' in command or '일번' in command :
                utils.playsound('settingvoice/start.mp3') # 안녕하세요 니카입니다. 무엇을 도와드릴까요?
                utils.time.sleep(0.5)

            else :
                utils.playsound('settingvoice/re_voice_input.mp3') # 해당하는 명령어를 찾을 수 없어요. 다시 말씀해 주세요.
                utils.time.sleep(0.5)
                
        else :
            utils.playsound('settingvoice/re_voice_end.mp3') # 해당하는 명령어를 찾을 수 없어요. 3회 이상 반복하여 대기 모드르 돌아갑니다.
            
        
def call_NICA(clientSock,r):
    print("|       니카 클라이언트 실행      |")
    model = utils.whisper.load_model("base")
    utils.playsound('settingvoice/system_start.mp3') # 니카 온라인
    
    while True:
        # 마이크 
        with utils.sr.Microphone(sample_rate=16000) as source:
            
            
            # 음성 인식
            result = speech2Text("[호출]",source,3,r,model)

            # 호출
            if '니카' in result or '니가' in result or 'next' in result:
                utils.playsound('settingvoice/start.mp3') # 안녕하세요 니카입니다. 무엇을 도와드릴까요?
                utils.time.sleep(0.5)

                # 명령어 판별
                commandList(source, clientSock, r)
                

            elif '종료' in result :
                exit()
            utils.time.sleep(0.5) # 0.5초 대기
            

def read_button_value(client_socket):
    print("|    프로세스 종료 시스템 실행    |")
    btn_value = False # 중지 버튼 안 누름
    
    while not btn_value: # 라즈베리파이 버튼값 계속 받아오기
        utils.time.sleep(120) # n초 뒤 중지 버튼 누름
        btn_value = True # 중지 버튼 누름
        # btn_value = 0
    
    client_socket.send('STOP'.encode())
    
    print("중단 요청 확인!")

def sendPhoto(sock,frame,type) :
    # 캡쳐한 사진 데이터 변환
    encode_param=[int(utils.cv2.IMWRITE_JPEG_QUALITY),90]
    result, imgencode = utils.cv2.imencode('.jpeg', frame, encode_param)
    
    data = utils.np.array(imgencode)

    # 서버로 전송
    print(f"클라이언트 수신 명령 => {type}")
    sock.send(type.encode('utf-8'))
    sock.sendall(str(len(data)).ljust(16).encode('utf-8'))
    utils.time.sleep(0.5)
    sock.send(data.tobytes())
    print('메시지를 전송했습니다.')


def ocr(sock,type,model,r,source) :

    # 음성 인식
    def speech2Text(work,source,time,r,model) :
        # 음성 입력
        print(f'{work} => 음성을 입력 준비 완료')
        audio = r.listen(source,timeout=time,phrase_time_limit=time)

        # 입력 받은 음성 저장
        with open(f'voice/input.wav',"wb") as f :
            f.write(audio.get_wav_data())

        # 저장된 음성 파일로 텍스트 추출
        audio = utils.whisper.load_audio("voice/input.wav")
        audio = utils.whisper.pad_or_trim(audio)
        mel = utils.whisper.log_mel_spectrogram(audio).to(model.device)
        _, probs = model.detect_language(mel)
        
        # 입력 값 확인 후 반환
        print(f"- 감지된 언어 : {max(probs, key=probs.get)}")
        options = utils.whisper.DecodingOptions(fp16 = False)
        result = utils.whisper.decode(model, mel, options)
        utils.os.remove('voice/input.wav')

        # Text 출력
        print(f'- 인식 결과 : {result.text}\n')
        return result.text
    
    count = 0
    while count < 3 :
        
        # 생성
        vid = utils.cv2.VideoCapture(0)
        ret, frame = vid.read() 
        
        ### TEST용 이미지로 전송함. 실제 카메라로 하고싶으면 바로 아래줄 주석처리
        #frame = utils.cv2.imread('book_example.jpg')

        if ret :
            # 인코딩 후 사진 전송
            sendPhoto(sock,frame,type)

            try :
                # 서버에서 처리한 음성데이터 텍스트 수신
                data = sock.recv(1024)
                speech_text = data.decode('utf-8', "ignore")

                # 서버에서 글자를 인식하지 못 했을때
                if "글자를 탐지하지 못했어요..." == speech_text :
                    # 다시 재 촬영
                    utils.playsound("settingvoice/re_vid_cap.mp3") # 글자를 탐지하지 못했어요 다시 탐지하겠습니다.
                    count += 1
                    utils.time.sleep(2)
                    continue
                
                # 서버에서 글자를 인식 했을때
                else :
                    # TTS 음성 파일 생성 => 재생 => 삭제
                    tts = utils.gTTS(text=speech_text, lang='ko', slow=False)
                    mp3_file = 'read.mp3'
                    tts.save(mp3_file)
                    utils.playsound(mp3_file)
                    utils.os.remove(mp3_file)
                    
                    # 명령어가 책 읽기 일때
                    if type == "book" :
                        utils.playsound("settingvoice/next_page.mp3") # 다음 페이지로 넘겨주세요.
                        count = 0 
                        utils.time.sleep(5) 
                        continue 

                    # 명령어가 글자 인식일떄
                    elif type == "word" :
                        
                        # 글주 추가 인식 여부 확인
                        utils.playsound("settingvoice/word_end.mp3")
                        utils.playsound('settingvoice/good.mp3')
                        result = speech2Text("[단어 재인식 여부]",source,5,r,model)

                        # 추가 인식
                        if "응" in result :
                            utils.playsound("settingvoice/ok_re_recognize.mp3") # 네 알겠습니다. 다시 단어를 인식해볼게요.
                            count = 0
                            utils.time.sleep(5)
                            continue
                        
                        # 추가 인식 종료
                        else : 
                        # elif "아니" in result :
                            utils.playsound("settingvoice/no_re_recognize.mp3") # 네 알겠습니다. 대기 모드로 돌아가겠습니다.
                            count = 0
                            break

            except Exception as e :
                print(e)
                pass
        
        # opencv 캡쳐 오류 시 다시 캡쳐
        else :
            print("사진 캡쳐에 오류가 있습니다.")
            utils.playsound('settingvoice/cap_error.mp3')
            count += 1
            utils.time.sleep(2)
            continue

        # 3회 글자 인식 실패
        if count >= 2 : utils.playsound('settingvoice/count_out_read_book.mp3') # 3회 이상 틀려서 대기모드로 돌아갑니다.
    
    

def handRecognize(sock,type,model,r,source) :

    # 생성
    vid = utils.cv2.VideoCapture(0)
    ret, frame = vid.read() 

    if ret :
        # 인코딩 후 사진 전송
        sendPhoto(sock,frame,type)

        print("성공")

    # opencv 캡쳐 오류 시 다시 캡쳐
    else :
        utils.print("사진 캡쳐에 오류가 있습니다.")
        utils.playsound('settingvoice/cap_error.mp3')
        