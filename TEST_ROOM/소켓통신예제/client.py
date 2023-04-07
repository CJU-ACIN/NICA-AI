import socket, cv2, pickle, struct
import time

while True:
    # Create Socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    host_ip = '203.252.240.67'
    port = 9999

    print(f"{host_ip = }")

    socket_address = (host_ip, port)

    # Socket Bind
    server_socket.bind(socket_address)

    # Socket Listen
    server_socket.listen(1)
    print(f"Listening at : {socket_address}")


    try:
        # Socket Accept
        while True:
            client_socket, addr = server_socket.accept()
            print(f'GOT CONNECTION FROM: {addr}')
            if client_socket:
                vid = cv2.VideoCapture(0) # w*h: 640*480
                print(f"width: {vid.get(cv2.CAP_PROP_FRAME_WIDTH)}, ", end='')# float `width`
                print(f"height: {vid.get(cv2.CAP_PROP_FRAME_HEIGHT)}" )# float `height`
                while(vid.isOpened()):
                    img, frame = vid.read()
                    a = pickle.dumps(frame)
                    message = struct.pack("Q", len(a)) + a
                    client_socket.sendall(message)

                    frame = cv2.rectangle(frame, (0, 0), (150, 40), (0, 0, 255), -1)
                    frame = cv2.putText(frame, "CLIENT", (15, 27), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 255, 255), 2)

                    cv2.imshow("CLIENT", frame)

                    key = cv2.waitKey(1) & 0xFF
                    if key == ord('q'):
                        client_socket.close()
    
    # Exception Handling - client
    except ConnectionResetError:
        cv2.destroyAllWindows()
        pass

    except ConnectionAbortedError:
        cv2.destroyAllWindows()
        pass