import cv2
import numpy as np
import pyfiglet
import time
from halo import Halo
import numpy as np

def start(counter):
    try:
        while True:
            ret, img =cam.read()

            gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

            faces = faceCascade.detectMultiScale( 
                gray,
                scaleFactor = 1.2,
                minNeighbors = 5,
                minSize = (int(minW), int(minH)),
            )

            for(x,y,w,h) in faces:

                cv2.rectangle(img, (x,y), (x+w,y+h), (0,255,0), 2)

                id, confidence = recognizer.predict(gray[y:y+h,x:x+w])

                # Check if confidence is less them 100 ==> "0" is perfect match 
                if (confidence < 100):
                    id = names[id]
                    confidence = "  {0}%".format(round(100 - confidence))
                    counter += 1
                else:
                    id = "unknown"
                    confidence = "  {0}%".format(round(100 - confidence))

                if counter == 100:
                    cv2.destroyAllWindows()
                    cv2.putText(blank, "[+] Gate terbuka, silahkan masuk ", (20,240), font, 1, (255,255,255), 2)
                    send.info("[+] Gate terbuka, silahkan masuk")
                    cv2.imshow('gate', blank)
                    k = cv2.waitKey(10) & 0xff # Press 'ESC' for exiting video
                    if k == 27:
                        break
                    time.sleep(5)
                    send.fail("[+] Gate tertutup")
                    cv2.destroyAllWindows()
                    counter = 0
                
                cv2.putText(img, "Tahan wajah anda di depan kamera " + str((100-counter)//5), (5,25), font, 1, (255,255,255), 2)
                cv2.putText(img, str(id), (x+5,y-5), font, 1, (255,255,255), 2)
                cv2.putText(img, str(confidence), (x+5,y+h-5), font, 1, (255,255,0), 1)  
            
            cv2.imshow('camera',img)
            k = cv2.waitKey(10) & 0xff # Press 'ESC' for exiting video
            if k == 27:
                break

    except KeyboardInterrupt:
        send.fail("[+] Keluar Program")
        cam.release()
        cv2.destroyAllWindows()
        exit()



if __name__ == "__main__":
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    recognizer.read('trainer/trainer.yml')
    cascadePath = "haarcascade_frontalface_default.xml"
    faceCascade = cv2.CascadeClassifier(cascadePath)
    blank = np.zeros((480, 640, 3))
    font = cv2.FONT_HERSHEY_SIMPLEX

    #iniciate id counter
    id = 0

    # names related to ids: example ==> Marcelo: id=1,  etc
    names = open('names.txt', 'r').read().split(',')

    # Initialize and start realtime video capture
    cam = cv2.VideoCapture(0)
    cam.set(3, 640) # set video widht
    cam.set(4, 480) # set video height

    # Define min window size to be recognized as a face
    minW = 0.1*cam.get(3)
    minH = 0.1*cam.get(4)
    print(pyfiglet.figlet_format("gate enterance"))
    with Halo(text='[+] Mengambil gambar', spinner='dots') as send:
        start(0)

    # Do a bit of cleanup
    cam.release()
    cv2.destroyAllWindows()



