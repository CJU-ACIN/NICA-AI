# 손끝점 물체탐지_예제

`checkObject.py`: 그냥 캠 꼽고 실행하면 무슨 객체 잡는지 알려줌 (손끝점 아님)

`Example.py`: 그냥 캠 꼽고 실행하면 **손끝점(빨간색 점으로 나옴)**이 뭘 가리키는지 알려줌

<br><br>

# 준비

가상환경 생성하고, yolov8 설치
```
pip install ultralytics
```

mediapipe 설치(손가락 끝점)
```
pip install mediapipe
```

<br><br><br>


# 사용법

이 함수 그냥 쓰면 됨

매개변수만 잘 넣으면 됨

<br>

**image**: 손 끝점(빨간점) 없는 원본 이미지 

**xy_tuple**: 손 끝점(빨간점) 좌표



<br><br>

```python
from ultralytics import YOLO

# 이거 함수만 나중에 떼서 쓰면 될듯
def whatIsThat(image, xy_tuple):
    # image: 이미지(손끝점(빨간색 점) 안 찍혀있는 원본 이미지로 )
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


```