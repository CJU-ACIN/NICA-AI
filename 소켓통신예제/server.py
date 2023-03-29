# for socket stream
import socket, cv2, pickle, struct

#etc
import os, uuid
from datetime import datetime

# for yolo
import torch
import numpy as np
from ultralytics import YOLO



# Load Pre-trained model
model = YOLO("yolov8m.pt")

# Create Socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host_ip = '203.252.240.67'
port = 9999

client_socket.connect((host_ip, port))
data = b""
payload_size = struct.calcsize("Q")

# check if file exists
img_dir = "saved_imgs"
if os.listdir(img_dir):
    for file in os.listdir(img_dir):
        os.remove(f"{img_dir}/{file}")


c = True
while True:
    while len(data) < payload_size:
        packet = client_socket.recv(4*1024) # 4k
        if not packet: break

        data += packet
    
    packed_msg_size = data[:payload_size]
    data = data[payload_size:]
    msg_size = struct.unpack("Q", packed_msg_size)[0]

    while len(data) < msg_size:
        data += client_socket.recv(4*1024) # 4*1024
    
    frame_data = data[:msg_size]
    data = data[msg_size:]

    frame = pickle.loads(frame_data)
    # yolo results
    results = model.predict(source=frame, show=False)

    # print(results[0].boxes.boxes)
    # for c in results[0].boxes.cls: # class list
    #    print(model.names[int(c)]) # 0: person

    # for box in results[0].boxes:
    #    print(box.xywh)
    
    xyxy = [] # initialize
    for i, box in enumerate(results[0].boxes):
        if int(box.cls) == 0:
            # print(box.cls)
            # print(box.xywh)
            xyxy.append(tuple(map(int, box.xyxy.tolist()[0])))
    
    # print(xyxy, type(xyxy))

    now = datetime.now()
    t1 = now.second
    if c:
        t2 = t1
        c = False
    
    # print(t1, t2)
    delay = 0
    if t1+delay != t2:
        print("READY TO SAVE...")
        if len(xyxy):
            for i, cord in enumerate(xyxy):
                x1, y1, x2, y2 = cord

                cv2.imwrite(f"saved_imgs/{now.month}_{now.day}_{now.hour}_{now.minute}_{now.second}.png", frame[y1:y2, x1:x2])
                print("PERSON... SAVED!")
                t2 = t1
        
        else:
            print("PERSON WAS NOT DETECTED...")


    for cord in xyxy:
        x1, y1, x2, y2 = cord
        frame = cv2.rectangle(frame, (x1, y1), (x2, y2), color=(0,255,255), thickness=2)

    frame = cv2.rectangle(frame, (0, 0), (150, 40), (0, 0, 255), -1)
    frame = cv2.putText(frame, "SERVER", (15, 27), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 255, 255), 2)

    cv2.imshow("CLIENT", frame)
    

    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):
        break

client_socket.close()