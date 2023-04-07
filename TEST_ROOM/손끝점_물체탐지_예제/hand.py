import mediapipe as mp
import cv2, math


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


mpHands = mp.solutions.hands
hands = mpHands.Hands()
mpDraw = mp.solutions.drawing_utils

cap = cv2.VideoCapture(0)

while cap.isOpened():

    ret, src = cap.read()

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
            handPoint(True)

        else :
            handPoint(False)

    if ret:
        cv2.imshow('cap', src)
        
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()