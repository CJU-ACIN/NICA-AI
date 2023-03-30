from gtts import gTTS

if __name__ == '__main__' :
    tts = gTTS(text="네 알겠습니다. 손을 탐지하겠습니다.", lang='ko', slow=False)
    tts.save('../main/settingvoice/find_hand.mp3')