import cv2
import pyfiglet
import numpy as np
from PIL import Image
import os
from halo import Halo

def create_dataset(count):
    while(True):

        ret, img = cam.read()
        
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = face_detector.detectMultiScale(gray, 1.3, 5)

        for (x,y,w,h) in faces:

            cv2.rectangle(img, (x,y), (x+w,y+h), (255,0,0), 2)     
            count += 1

            # Save the captured image into the datasets folder
            cv2.imwrite("dataset/User." + str(face_id) + '.' + str(count) + ".jpg", gray[y:y+h,x:x+w])

            cv2.imshow('image', img)

        k = cv2.waitKey(100) & 0xff # Press 'ESC' for exiting video
        if k == 27:
            break
        elif count >= 100:
            break
    cam.release()
    cv2.destroyAllWindows()
    send.info('[+] Sampel wajah anda telah diambil.')
    send.succeed('[+] Pengambilan sampel wajah selesai.')

# function to get the images and label data
def getImagesAndLabels(path):

    imagePaths = [os.path.join(path,f) for f in os.listdir(path)]     
    faceSamples=[]
    ids = []

    for imagePath in imagePaths:

        PIL_img = Image.open(imagePath).convert('L') # convert it to grayscale
        img_numpy = np.array(PIL_img,'uint8')

        id = int(os.path.split(imagePath)[-1].split(".")[1])
        faces = face_detector.detectMultiScale(img_numpy)

        for (x,y,w,h) in faces:
            faceSamples.append(img_numpy[y:y+h,x:x+w])
            ids.append(id)

    return faceSamples,ids

if __name__ == "__main__":

    names = open('names.txt', 'r').read().split(',')
    cam = cv2.VideoCapture(0)
    cam.set(3, 640) # set video width
    cam.set(4, 480) # set video height
    face_detector = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
    path = 'dataset'

    print(pyfiglet.figlet_format("gate enterance"))
    while True:
        name = input('[?] Masukan nama anda: ')
        
        if name.lower() in [n.lower() for n in names]:
            print("Nama sudah ada dalam daftar. Silakan masukkan nama lain.")
        else:
            break

    face_id = len(names)

    with Halo(text='[+] Pengambilan sampel, pastikan wajah anda terlihat pada kamera ...', spinner='dots') as send:
        create_dataset(0)

    with Halo(text='[+] Training wajah anda. Mohon tunggu ...', spinner='dots') as send:
        recognizer = cv2.face.LBPHFaceRecognizer_create()
        faces,ids = getImagesAndLabels(path)
        recognizer.train(faces, np.array(ids))

        # Save the model into trainer/trainer.yml
        recognizer.write('trainer/trainer.yml') # recognizer.save() worked on Mac, but not on Pi
        send.succeed("[+] {0} wajah telah ter training.".format(len(np.unique(ids))))
    open('names.txt', 'a').write(',{0}'.format(name))
    
    