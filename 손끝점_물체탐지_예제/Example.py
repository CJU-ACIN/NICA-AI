import mediapipe as mp
import cv2, math
from ultralytics import YOLO

def handPoint(where_hand) :

    if x1 == x2 :
        grad = 0
    else : 
        grad = round((y2 - y1) / (x2 - x1),1)

    d = int((math.sqrt((x2 - x1)**2 + (y2 - y1)**2))/2)

    if where_hand == True :  # 오른손
        x = x1 - d
    else :                   # 왼손
        x = x1 + d

    y = int(grad * (x - x1) + y1)

    cv2.line(src, (x1, y1), (x2, y2), (0, 255, 0), 3)
    cv2.circle(src, (x, y), 3, (0, 0, 255), cv2.FILLED)

    return (x, y)

# 이거 함수만 나중에 떼서 쓰면 될듯
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
            

mpHands = mp.solutions.hands
hands = mpHands.Hands()
mpDraw = mp.solutions.drawing_utils

cap = cv2.VideoCapture(0)

while cap.isOpened():

    ret, org = cap.read()


    if ret:
        src = org.copy() # 원본 이미지 복제
        dst = cv2.cvtColor(src, cv2.COLOR_BGR2RGB)
        result = hands.process(dst)
        if result.multi_hand_landmarks:
            for handLms in result.multi_hand_landmarks:
                for id, lm in enumerate(handLms.landmark):

                    h, w, c = src.shape
                    cx, cy = int(lm.x * w), int(lm.y * h)

                    if id == 8 :
                        x1, y1 = cx, cy
                    elif id == 7 :
                        x2, y2 = cx, cy

            if x1<x2 :
                xy_tuple = handPoint(True)
                reuslt_text = whatIsThat(org, xy_tuple) # 아예 이미지 원본값. 점이 찍혀있는 이미지면 안되니깐
                print(reuslt_text)

            else :
                xy_tuple = handPoint(False)
                reuslt_text = whatIsThat(org, xy_tuple) # 아예 이미지 원본값. 점이 찍혀있는 이미지면 안되니깐
                print(reuslt_text)

        
            dst = src.copy()
            cv2.imshow('cap', src)
            
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

cap.release()
cv2.destroyAllWindows()