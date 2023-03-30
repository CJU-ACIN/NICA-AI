from gtts import gTTS
from playsound import playsound
import multiprocessing
import time

# text = "어머님, 나는 별 하나에 아름다운 말 한마디씩 불러 봅니다. 소학교 때 책상을 같이 했던 아이들의 이름과, 패, 경, 옥, 이런 이국 소녀들의 이름과, 벌써 아기 어머니 된 계집애들의 이름과, 가난한 이웃 사람들의 이름과, 비둘기, 강아지, 토끼, 노새, 노루, '프랑시스 잠', '라이너 마리아 릴케' 이런 시인의 이름을 불러 봅니다."
# tts = gTTS(text=text, lang='ko', slow=True)
# tts.save('long.mp3')


def process_tts(mp3):
    playsound(mp3)
    p2.terminate()
    time.sleep(0.3)
    p2.close()


def process_input():
    while True:
        input("enter to stop: ")
        break

    p1.terminate()
    time.sleep(0.3)
    p1.close()



if __name__ == "__main__":
    p1 = multiprocessing.Process(target=playsound, args=("long.mp3", ))
    p2 = multiprocessing.Process(target=process_input)

    p1.start()
    p2.start()

    p2.join()

    print("END!")
