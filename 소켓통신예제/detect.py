from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

import face_recognition
import cv2
import numpy as np
from datetime import datetime
import time, os, shutil

class Detect(FileSystemEventHandler):
    def event_detect(self, event): # detect face
        img_path = event.src_path
        time.sleep(0.1) # detects when Image is not fully saved

        # Get Iamge
        image = face_recognition.load_image_file(img_path)

        # then check who it is

        try: # Check if there are faces
            face_locations = face_recognition.face_locations(image)
            print(f"{face_locations = }")
            face_encoding = face_recognition.face_encodings(image, face_locations)
            
            results = []
            for fe in face_encoding:
                results.append(face_recognition.compare_faces(known_encodings, fe, tolerance=0.5))
        
            # prints who is in the picture
            print(f"{results = }")
            detected_faces = [known_names[i] for i, x in enumerate(results) if x]
            if len(detected_faces) > 0:
                print()
                print(*detected_faces, sep=' ')
                print()
            else:
                print("@@@ UNKNOWN @@@")
        
        except IndexError:
            print("no face was detected")
            pass

        os.remove(img_path)



    def on_created(self, event): # EVENT
        print("DETECTED IMAGES...")
        self.event_detect(event)
        
if __name__ == "__main__":
    known_faces = [face_recognition.load_image_file(f"known_faces/{x}") for x in sorted(os.listdir('known_faces/'))] # known faces

    global known_encodings # train face
    known_encodings = [face_recognition.face_encodings(x)[0] for x in known_faces]
    print(f'{len(known_encodings) = }')

    global known_names
    known_names = [x.split('.')[0] for x in sorted(os.listdir('known_faces/'))]
    print(f'{known_names = }')

    # check if file exists
    event_handler = Detect()
    observer = Observer()
    observer.schedule(event_handler, path='saved_imgs/', recursive=True)
    observer.start()

    try:
        while observer.is_alive():
            observer.join(1) # watches Every 1 sec
            now = datetime.now()
            print(f"detect.py is watching...{now.hour:02d}:{now.minute:02d}:{now.second:02d}")
    
    finally: # when event stops and continue
        observer.stop()
        observer.join()