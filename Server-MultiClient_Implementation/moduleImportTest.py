import os
import time
import cv2
import numpy as np
from whisper import whisper         # 폴더에서 갖고옴
from gtts import gTTS               # Text to Speech
import speech_recognition as sr     # 음성 인식
from playsound import playsound     # 파이썬 음성 파일 재생 => 경로에 특수문자 들어가면 안됨
from socket import *



if __name__ == "__main__":
    print("Import Success!")