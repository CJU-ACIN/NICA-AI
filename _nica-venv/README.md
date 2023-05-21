# 용도

| <center> 이름 </center> | <center> 용도 </center> |
|:---|:---:|
| whisper | STT 기능 |
| SpeechRecognition | 음성 입력 |
| gTTS | TTS 기능 |
| playsound | 음성 재생 |
| opencv | 영상 처리 |
| mqtt | 통신 |


<br><br><br>

# 가상환경 설정 가이드

***virtualenv python 3.8.x 가상환경 기준*** 

~~***3.8.10***~~

<br>

## 1. whisper 설치


```
git clone https://github.com/openai/whisper.git
```

```
cd whisper
```
```
pip install -e .
```

<br><br>

## 2. ffmpeg 설치

[링크](https://www.gyan.dev/ffmpeg/builds/)

위 사이트에 접속해서 latest git master branch build (제일 상단) 에서

ffmpeg-git-essentials.7z
.ver .sha256

```
가상환경이름/Script/
```
여기에 들어와서 ffmpeg.exe 넣어주셈

~~pyhton-ffmpeg 패키지에 ffmpeg.exe 파일이 누락되어있음~~


<br><br>

## 3. 나머지 설치

***주의: playsound는 1.2.2 버전 설치. 호환성 문제***

```
python -m pip install opencv-python gtts SpeechRecognition playsound==1.2.2 pyaudio

```

<br><br>

## 3. 결과

![result.png](result.png)

<br><br>

``moduleImportTest.py`` 실행해서 테스트

작업파일은 moudleImportTest랑 동일한 경로에서 실행

## 4. mqtt 설치 
```
pip install paho-mqtt

```
