import cv2
import socket as sk
import numpy as np
s = sk.socket(sk.AF_INET, sk.SOCK_STREAM)
cap = cv2.VideoCapture('http://192.168.43.1:8080/video') #accessing mobile cam using ip webcam app
s.connect((sk.gethostbyname(sk.gethostname()),5000)) #establishing the connection
s.settimeout(5)

try:
      while True:
        ret, photo = cap.read()
        frame = cv2.flip(photo,1) #flipping
        frame_new = cv2.resize(frame,(540,430))  #resizing
        encdata = cv2.imencode(".jpg",frame_new)[1].tobytes()  #encoding
        s.sendall(encdata)  #sending data
        data = s.recv(90456)  #receiving connection
        npdata = np.fromstring(data, np.uint8)  #converting to numpy array
        decdata = cv2.imdecode(npdata, cv2.IMREAD_COLOR)  #decoding
        cropimg = cv2.resize(frame,(200,150),3)  #resizing
        if type(decdata) is type(None):
            count = count + 1
        else:
            decdata[:150,:200] = cropimg
            cv2.imshow('Person1',decdata)  #display
            count = 0
            if cv2.waitKey(1) == 13:  #exiting with enter
                cv2.destroyAllWindows()
                cap.release()
                s.close()
                break

except:
    cv2.destroyAllWindows()
    cap.release()
    s.close()
    print("connection closed by server")