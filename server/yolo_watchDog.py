import os
import time
import re
import shutil
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

from ultralytics import YOLO
import cv2, math


def whatIsThat(image, xy_tuple):
    # src: 이미지
    # xy_tuple: 손 끝 좌표 값
    model = YOLO('yolov8n-seg.pt')
    
    # 길쭉해요
    classes = {0: 'person', 1: 'bicycle', 2: 'car', 3: 'motorcycle', 4: 'airplane', 5: 'bus', 6: 'train', 7: 'truck', 8: 'boat', 9: 'traffic light', 10: 'fire hydrant', 11: 'stop sign', 12: 'parking meter', 13: 'bench', 14: 'bird', 15: 'cat', 16: 'dog', 17: 'horse', 18: 'sheep', 19: 'cow', 20: 'elephant', 21: 'bear', 22: 'zebra', 23: 'giraffe', 24: 'backpack', 25: 'umbrella', 26: 'handbag', 27: 'tie', 28: 'suitcase', 29: 'frisbee', 30: 'skis', 31: 'snowboard', 32: 'sports ball', 33: 'kite', 34: 'baseball bat', 35: 'baseball glove', 36: 'skateboard', 37: 'surfboard', 38: 'tennis racket', 39: 'bottle', 40: 'wine glass', 41: 'cup', 42: 'fork', 43: 'knife', 44: 'spoon', 45: 'bowl', 46: 'banana', 47: 'apple', 48: 'sandwich', 49: 'orange', 50: 'broccoli', 51: 'carrot', 52: 'hot dog', 53: 'pizza', 54: 'donut', 55: 'cake', 56: 'chair', 57: 'couch', 58: 'potted plant', 59: 'bed', 60: 'dining table', 61: 'toilet', 62: 'tv', 63: 'laptop', 64: 'mouse', 65: 'remote', 66: 'keyboard', 67: 'cell phone', 68: 'microwave', 69: 'oven', 70: 'toaster', 71: 'sink', 72: 'refrigerator', 73: 'book', 74: 'clock', 75: 'vase', 76: 'scissors', 77: 'teddy bear', 78: 'hair drier', 79: 'toothbrush'}
    results = model.predict(image)
    
    # 결과값이 0, 4, 3 이런식으로 나오는데
    # 위에 선언한 classes 딕셔너리에서 value 따오기
    labels = list(map(int, results[0].boxes.cls.tolist()))
    xy_coord = [x for x in results[0].masks.xy]

    result_object = ""
    for num, points in enumerate(xy_coord):
        temp = cv2.pointPolygonTest(points, xy_tuple, False)
        
        # 안에 있으면
        if temp >= 0:
            result_object = classes[labels[num]]
    
    # 해당 좌표가 객체 어디에도 속하지 않는다면
    if result_object == "":
        result_object = "UNKNOWN"

    return result_object


class Target:
    watchDir = os.getcwd()
    print(f'실행 완료!\n탐지 경로 => {watchDir}')
    #watchDir에 감시하려는 디렉토리를 명시한다.

    def __init__(self):
        self.observer = Observer()   #observer객체를 만듦

    def run(self):
        event_handler = Handler()
        self.observer.schedule(event_handler, self.watchDir, 
                                                       recursive=True)
        self.observer.start()
        try:
            while True:
                time.sleep(1)
        except:
            self.observer.stop()
            print("Error")
            self.observer.join()

class Handler(FileSystemEventHandler):
#FileSystemEventHandler 클래스를 상속받음.
#아래 핸들러들을 오버라이드 함
    def on_created(self, event): #파일, 디렉터리가 생성되면 실행
        print(f'생성된 파일 : {event.src_path}')
        path = str(event.src_path)
        
        file_name = path.split('/')[5]
        xy_tuple = tuple(map(int, re.findall(r'\d+', file_name)))
        
        print(f'확인 : {file_name}, {xy_tuple}')
        
        org = cv2.imread(file_name)
    
        reuslt_text = whatIsThat(org, xy_tuple)
        print(f'인식한 결과 : {reuslt_text}')
        os.rename(file_name, f'{reuslt_text}.jpeg')
        shutil.move(f'{reuslt_text}.jpeg', f"./result/{reuslt_text}.jpeg")
        
        print("== 수행 완료 ==")
        
        #os.remove(f"./result/{reuslt_text}.jpeg")
        

        
if __name__ == '__main__' : #본 파일에서 실행될 때만 실행되도록 함
    w = Target()
    w.run()