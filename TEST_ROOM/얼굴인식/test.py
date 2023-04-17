import os
import numpy as np
import face_recognition


if __name__ == "__main__":
    # WARNING
    # keep in mind you need to sort the Image files

    # collect known faces
    known_faces = [face_recognition.load_image_file(f"known_faces/{x}") for x in sorted(os.listdir('known_faces/'))]
    
    # encode known faces
    known_encodings = [face_recognition.face_encodings(x)[0] for x in known_faces]

    known_names = [x.split('.')[0] for x in sorted(os.listdir('known_faces/'))]

    # load 5 test images
    image1 = face_recognition.load_image_file("test_image/OBAMA.jpg") # 1 known face
    image2 = face_recognition.load_image_file("test_image/TRUMP+OBAMA.jpg") # 2 known faces
    image3 = face_recognition.load_image_file("test_image/unknown.jpg") # 1 unknown face
    image4 = face_recognition.load_image_file("test_image/OBAMA+unknown.jpg") # 1 known face + 1 unknown face
    image5 = face_recognition.load_image_file("test_image/unknown1+unknown2.jpg") # 2 unknown faces

    # choose your image
    select_image = image5
    try:
        # check if image has face
        test_image_face_locations = face_recognition.face_locations(select_image)

        # encode test image
        test_image_face_encoding = face_recognition.face_encodings(select_image, test_image_face_locations)

        result_boolean = []
        for fe in test_image_face_encoding:
            # put list of arrays
            # if simularity >= 50%, it returns true
            result_boolean.append(face_recognition.compare_faces(known_encodings, fe, tolerance=0.5))

        print(result_boolean) # ex) [[True, False]] or [[True, False], [False, False]]

        result_name = []
        for res in result_boolean:
            # if [[False, False]]
            if sum(res) == 0:
                result_name.append("@@UNKNOWN@@")

            else:
                result_name.append(known_names[np.argmax(res)])
        
        print(result_name) # ex) [OBAMA] or [OBAMA, TRUMP]

    except IndexError:
        print("NO FACE WAS DETECED")
        pass

