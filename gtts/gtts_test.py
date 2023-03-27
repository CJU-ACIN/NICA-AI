from gtts import gTTS

if __name__ == '__main__' :
    tts = gTTS(text="네 알겠습니다.. 책 읽기를 도와드릴게요.", lang='ko', slow=False)
    tts.save('../main/settingvoice/startBook.mp3')