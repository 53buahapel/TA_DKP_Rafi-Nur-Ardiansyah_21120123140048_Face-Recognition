import tkinter as tk
from tkinter import messagebox
import cv2
import numpy as np
from PIL import Image
import os
from halo import Halo
import threading

class FaceRecognitionApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Face Recognition")
        self.root.geometry("400x180")

        self.face_detector = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
        self.path = 'dataset'
        self.names = open('names.txt', 'r').read().split(',')
        
        self.create_widgets()

    def create_widgets(self):
        self.title_label = tk.Label(self.root, text="Gate Entrance", font=("Helvetica", 16))
        self.title_label.pack(pady=10)

        self.name_label = tk.Label(self.root, text="Enter your name:")
        self.name_label.pack(pady=5)

        self.name_entry = tk.Entry(self.root)
        self.name_entry.pack(pady=5)

        self.start_button = tk.Button(self.root, text="Start", command=self.start_recognition)
        self.start_button.pack(pady=20)

        self.output_text = tk.Text(self.root, height=10, state='disabled')
        self.output_text.pack(pady=10)

    def start_recognition(self):
        name = self.name_entry.get()
        if not name:
            messagebox.showerror("Input Error", "Please enter a name.")
            return

        if name.lower() in [n.lower() for n in self.names]:
            messagebox.showerror("Name Error", "Name already exists. Please enter a different name.")
            return

        self.face_id = len(self.names)
        self.output_text.configure(state='normal')
        self.output_text.configure(state='disabled')

        # Start the dataset creation and training in a new thread to avoid freezing the GUI
        threading.Thread(target=self.create_dataset_and_train, args=(name,)).start()

    def create_dataset_and_train(self, name):
        with Halo(text='[+] Pengambilan sampel, pastikan wajah anda terlihat pada kamera ...', spinner='dots') as send:
            self.create_dataset(0)
            send.succeed('[+] Pengambilan sampel wajah selesai.')

        with Halo(text='[+] Training wajah anda. Mohon tunggu ...', spinner='dots') as send:
            recognizer = cv2.face.LBPHFaceRecognizer_create()
            faces, ids = self.getImagesAndLabels(self.path)
            recognizer.train(faces, np.array(ids))

            # Save the model into trainer/trainer.yml
            recognizer.write('trainer/trainer.yml')
            send.succeed("[+] {0} wajah telah ter training.".format(len(np.unique(ids))))

        open('names.txt', 'a').write(',{0}'.format(name))
        self.names.append(name)
        self.output_text.configure(state='normal')
        self.output_text.insert(tk.END, f"Training completed for {name}\n")
        self.output_text.configure(state='disabled')
        messagebox.showinfo("Success", "Training completed successfully.")

    def create_dataset(self, count):
        cam = cv2.VideoCapture(0)
        cam.set(3, 640)  # set video width
        cam.set(4, 480)  # set video height

        while True:
            ret, img = cam.read()
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            faces = self.face_detector.detectMultiScale(gray, 1.3, 5)

            for (x, y, w, h) in faces:
                cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
                count += 1
                cv2.imwrite("dataset/User." + str(self.face_id) + '.' + str(count) + ".jpg", gray[y:y + h, x:x + w])
                cv2.imshow('image', img)

            k = cv2.waitKey(100) & 0xff  # Press 'ESC' for exiting video
            if k == 27:
                break
            elif count >= 100:
                break

        cam.release()
        cv2.destroyAllWindows()

    def getImagesAndLabels(self, path):
        imagePaths = [os.path.join(path, f) for f in os.listdir(path)]
        faceSamples = []
        ids = []

        for imagePath in imagePaths:
            PIL_img = Image.open(imagePath).convert('L')  # convert it to grayscale
            img_numpy = np.array(PIL_img, 'uint8')
            id = int(os.path.split(imagePath)[-1].split(".")[1])
            faces = self.face_detector.detectMultiScale(img_numpy)

            for (x, y, w, h) in faces:
                faceSamples.append(img_numpy[y:y + h, x:x + w])
                ids.append(id)

        return faceSamples, ids

if __name__ == '__main__':
    root = tk.Tk()
    app = FaceRecognitionApp(root)
    root.mainloop()