import cv2
import mediapipe as mp
import numpy as np


# 출처
# https://youtu.be/01sAkU_NvOY?t=2961


# 객체 선언
mpHands = mp.solutions.hands
hands = mpHands.Hands()
mpDraw = mp.solutions.drawing_utils

# 비디오 캡쳐
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

                print(cx, cy)
                if id == 8:
                    cv2.circle(src, (cx, cy), 15, (0, 255, 0), cv2.FILLED)


            mpDraw.draw_landmarks(src, handLms)


    if ret:
        cv2.imshow('cap', src)


    if cv2.waitKey(1) & 0xFF == ord('q'):
        break


cap.release()
cv2.destroyAllWindows()

