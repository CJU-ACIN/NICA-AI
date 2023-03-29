from gtts import gTTS

if __name__ == '__main__' :
    tts = gTTS(text="추가적으로 글자를 인식할까요?", lang='ko', slow=False)
    tts.save('../main/settingvoice/word_end.mp3')