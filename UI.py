import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
import requests
import json

class App:
    def __init__(self, master):
        self.master = master
        self.img = None
        self.filepath = None
        self.text = None
        self.create_widgets()

    def create_widgets(self):
        self.select_button = tk.Button(self.master, text="Select Image", command=self.select_image)
        self.select_button.pack()

        self.canvas = tk.Canvas(self.master, width=700, height=700)
        self.canvas.pack()

        self.extract_button = tk.Button(self.master, text="Extract Text", command=self.extract_text)
        self.extract_button.pack()

        #self.canvas2 = tk.Canvas(self.master, width=300, height=800)
        #self.canvas2.pack()

        self.text_label = tk.Label(self.master, text="")
        self.text_label.pack()

    def select_image(self):
        self.filepath = filedialog.askopenfilename()
        print(self.filepath)
        if self.filepath:
            self.img = Image.open(self.filepath)
            self.imgg = self.img.resize((300, 300))
            self.imgg = ImageTk.PhotoImage(self.imgg)
           # self.canvas.create_image(0, 0, anchor=tk.NW, image=self.imgg)

    def extract_text(self):
        if self.img:
            '''pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
            self.text = pytesseract.image_to_string(self.img)'''

            url = "http://127.0.0.1:5000/prescriptiondetails"
            files = {
            'image': open(self.filepath, 'rb'),
            }

            response = requests.post(url, files=files)
            print(response.json())
            for k in response.json():
                    text.insert(tk.END, '{} = {}\n'.format(k,response.json()[k]))
            text.config(state = tk.DISABLED)

            '''self.text=response.json()
            arr=self.text.split("\n");
            for text in arr:
                self.canvas.create_text(10,10,text=text,offset=20)'''

root = tk.Tk()
app = App(root)
root.mainloop()