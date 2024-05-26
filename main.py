import tkinter as tk
import os

class Application:
    def __init__(self, root):
        self.root = root
        self.root.title("Main Menu")
        self.root.geometry("480x360")
        self.root.iconbitmap('icon.ico')

        first_label = tk.Label(self.root, text="Face Recognition App", font=10)
        first_label.pack(pady=2, padx=2)

        self.create_widgets()

    def create_widgets(self):
        button_style = {
            'width': 20,
            'height': 2
        }

        self.btn1 = tk.Button(self.root, text="Registration", command=self.launch_pendaftaran, **button_style)
        self.btn1.pack(pady=5)

        self.btn2 = tk.Button(self.root, text="Start", command=self.start_py, **button_style)
        self.btn2.pack(pady=5)

        self.btn3 = tk.Button(self.root, text="Reset", command=self.reset_py, **button_style)
        self.btn3.pack(pady=5)

    def launch_pendaftaran(self):
        os.system('python pendaftaran.py')

    def start_py(self):
        os.system('python start.py')

    def reset_py(self):
        os.system('python reset_data.py')


if __name__ == '__main__':
    root = tk.Tk()
    app = Application(root)
    root.mainloop()
