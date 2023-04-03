from . import utils

import os
import multiprocessing                      # 중지 스위치
from socket import *                        # 서버-클라이언트 통신
import time, cv2  
import numpy as np

from .whisper import whisper         # Speech to Text
from gtts import gTTS                       # Text to Speech
import speech_recognition as sr             # 음성 인식
from playsound import playsound             # 파이썬 음성 파일 재생 => 경로에 특수문자 들어가면 안됨
#from commands import ocr, handRecognize     # 제공 서비스
import random

print("=========== import 완료 ===========")