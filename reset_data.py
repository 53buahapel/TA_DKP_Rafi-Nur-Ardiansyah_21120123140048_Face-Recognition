import tkinter as tk
from tkinter import messagebox
import os
import pyfiglet

class ResetDataApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Reset Data Confirmation")
        self.root.geometry("400x200")

        self.create_widgets()

    def create_widgets(self):

        self.question_label = tk.Label(self.root, text="Are you sure you want to reset all data?")
        self.question_label.pack(pady=10)

        self.button_frame = tk.Frame(self.root)
        self.button_frame.pack(pady=10)

        self.yes_button = tk.Button(self.button_frame, text="Yes", command=self.reset_data)
        self.yes_button.grid(row=0, column=0, padx=10)

        self.no_button = tk.Button(self.button_frame, text="No", command=self.root.destroy)
        self.no_button.grid(row=0, column=1, padx=10)

    def reset_data(self):
        directories = ['dataset', 'trainer']
        files = ['names.txt']

        for directory in directories:
            if os.path.exists(directory) and os.path.isdir(directory):
                for filename in os.listdir(directory):
                    file_path = os.path.join(directory, filename)
                    try:
                        if os.path.isfile(file_path):
                            os.remove(file_path)
                            print(f'[+] Deleted file: {file_path}')
                    except Exception as e:
                        print(f'[!] Error deleting file {file_path}: {e}')
            else:
                print(f'[!] Directory {directory} does not exist.')

        try:
            with open('names.txt', 'w') as f:
                f.write('None')
            messagebox.showinfo("Success", "Data has been reset successfully.")
        except Exception as e:
            print(f'[!] Error resetting names.txt: {e}')
            messagebox.showerror("Error", f"Error resetting names.txt: {e}")

        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = ResetDataApp(root)
    root.mainloop()
