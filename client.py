import cv2
import socket as sk
import numpy as np

cap = cv2.VideoCapture(0)  # capturing laptop cam
s = sk.socket(sk.AF_INET, sk.SOCK_STREAM)  # creating a socket
s.bind((sk.gethostbyname(sk.gethostname()), 5000))  # binding
s.listen(10)  # listening
conn, addr = s.accept()  # accepting the connection
print(conn)

try:
    while True:
        data = conn.recv(90456)  # receiving connection
        npdata = np.fromstring(data, np.uint8)  # converting to numpy array
        decdata = cv2.imdecode(npdata, cv2.IMREAD_COLOR)  # decoding
        ret, photo = cap.read()
        frame = cv2.flip(photo, 1)  # flipping
        cropimg = cv2.resize(frame, (200, 150), 3)  # resizing
        framesend = cv2.imencode('.jpg', frame)[1].tobytes()
        conn.sendall(framesend)  # sending data
        if type(decdata) is type(None):
            pass
        else:
            decdata[:150, :200] = cropimg
            cv2.imshow('Person2', decdata)  # display
            if cv2.waitKey(1) == 13:  # exiting with enter
                cv2.destroyAllWindows()
                cap.release()
                s.close()
                break

except:
    cv2.destroyAllWindows()
    cap.release()
    s.close()
    print("connection closed by client")