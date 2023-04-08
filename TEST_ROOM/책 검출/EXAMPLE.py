import os

from ultralytics import YOLO
from pororo import Pororo
import cv2


## 함수: 책 좌표 찾기
def findBook(image_path):
    # 임시폴더 생성
    if os.path.isdir('Imgtemp/'): # 있으면, 폴더 안에 파일 다 지우고 폴더 생성
        for i in os.listdir('Imgtemp/'):
            os.remove(i)
            
        os.mkdir('Imgtemp/')
        
    else: #없으면 그냥 폴더만 생성
        os.mkdir('Imgtemp/')
    
    
    image = cv2.imread(image_path) # 이미지 가져오기
    
    model = YOLO('yolov8n-seg.pt') # pytorch에서 미리 학습된 모델 가져오기
    results = model.predict(image) # 결과 오브젝트 반환
    
    labels = list(map(int, results[0].boxes.cls.tolist()))
    xyxy = results[0].boxes.xyxy.tolist()
    
    
    coords = []
    for i, label in enumerate(labels):
        if label == 73: # 73: 'book'
            coords.append(xyxy[i])
    
    
    for i, coord in enumerate(coords):
        x1, x2, y1, y2 = coord
        cv2.imwrite(f"Imgtemp/{i}.jpg", image[y1:y2, x1:x2])
        
    # xyxy 좌표값들 반환
    # 주의: 한 이미지에 여러 책이 검출 될 수 있음.
    # ex) coords = [(x1, y1, x2, y2), (xx1, yy1, xx2, yy2), ...]
    return coords
    

## 함수: 특정 폴더에 있는 이미지를 전부 읽어서 ocr을 통해 책 이름 찾기
def findbookname():
    bookname = ""
    
    result_temp = []
    for i in os.listdir("Imgtemp/"):
        # OCR 돌려서 여러책이 검출됐을경우를 대비해, 해당 좌표에 있는 이미지들을 읽어보는거임
        # 읽어봐서 OCR에 글자가 잡히는 것만 결과값 출력
        ocr = Pororo(task="ocr", lang="ko") # ko 해도 한글+영어 다 잡음
        temp = ocr(f"Imgtemp/{i}")
        if len(ocr) != 0:
            result_temp.append(temp)
    # for END
    
    for bookname_temp in result_temp:
        # 검출된 책들 중에 각각 글자가 있다면, 가장 긴걸로 선정
        if len(bookname) < bookname_temp: 
            bookname = bookname_temp
    
    return bookname
            


## 메인
if __name__ == "__main__":
    
    image_path = "대충/이미지/경로.jpg"
    
    ## findBook으로 책 좌표 찾은다음에 책 검출된 부분을 이미지로 저장
    coords = findBook(image_path)
    
    # 저장된 이미지 쪽으로 알아서 글자 검사
    # 글자가 있으면 그걸 결과값으로 가짐
    result = findbookname(image_path, coords)
    
    print(result if result != "" else "검출된 글자가 없음!") # 책 이름 출력
   
    
    