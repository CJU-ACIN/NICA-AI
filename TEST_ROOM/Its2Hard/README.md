# 구현된 기능

***`cli.py`만 멈추고 서버는 동작 멈추게 못했음***

***`ocr`기능만 테스트했고, 카메라 입력값 대신에 이미지파일 book_example.jpg 사용***
코드 수정은 `commands.py`의 64번째 줄

``` python
while count < 3 :
        
        # 생성
        vid = cv2.VideoCapture(0)
        ret, frame = vid.read() 
        
        ### TEST용 이미지로 전송함. 실제 카메라로 하고싶으면 바로 아래줄 주석처리
        frame = cv2.imread('book_example.jpg')
```


- ## 정지 버튼이 눌리면 client.py의 기능(stt, tts)들이 동작을 멈추고, 서버에서 연결을 끊음. 이때, 서버는 AI처리를 전부 한 뒤에야 연결을 끊음(즉, 중간 정지 안됨)



<br><br><br>

# 과정
<br>


1. 정지 버튼이 눌리면 client.py의 기능(stt, tts)들이 동작을 멈추고, 서버에서 연결을 끊음 
<br><br>
2. 서버는 클라이언트 연결이 끊기면 `.recv()`를 통해 클라이언트와 연결 끊겼다는 걸 알고 자기도 서버 재시작함. (이유는 모르겠는데, 서버 껐다 키는걸 안하면 클라쪽에서 제대로 못잡음..)
<br><br>
3. 이때, 클라이언트랑 서버는 서로 재접속할건데, <br>
기존 포트번호가 사용중일 경우(자원반환이 잘 안돼서),<br>
포트값을 1씩 늘려가면서 다시 서버 개설 및 접속 요청


<br><br><br>

# 설명
cli.py 122 번째 줄 

```python
def read_button_value(client_socket):
    btn_value = False # 중지 버튼 안 누름
    
    while not btn_value: # 라즈베리파이 버튼값 계속 받아오기
        time.sleep(120) # n초 뒤 중지 버튼 누름
        btn_value = True # 중지 버튼 누름
        # btn_value = 0
    
    client_socket.send('STOP'.encode())
    
    print("중단 요청 확인!")
```

루프문을 이용하여 라즈베리파이에서 버튼 값 계속 받는 것처럼 보이게 해봤음

