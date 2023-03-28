# 소켓 통신 예제

## 파일
<br>

**client.py** : 클라이언트(라즈베리파이)에서 서버로 영상(프레임) 송신

**server.py** : 영상프레임 수신 및 간단한 동작 처리(opencv-python 작업 등)

**detect.py** : 무거운 동작 수행(pytorch, 모델 출력값 받기 등)

<br><br>

※ server.py에서 영상수신이 느려질까봐 오래걸리는 동작은 detect.py에 처리하게끔 했었는데, <br>

만약 합치고 싶으면<br>
Thread 모듈을 이용한 병렬처리를 통하여 server.py에 전부 동작하게 만들면 됨
<br><br><br><br>

<hr>

## 코드 설명

<br>

***필요 시 작성***