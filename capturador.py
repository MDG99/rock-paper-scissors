import cv2
import csv
from datetime import datetime
from tkinter import *
from PIL import Image
from PIL import ImageTk
import tkinter.font as TkFont

cap = None

# La función Caoture_dataset te permite caoturar una imagen para tu dataset y guardarla clasificarla como se debe
# b -> Instrucción para empezar el juego [0]
# m -> Instrucción para acabar el juego [1]
# r -> Piedra [2]
# p -> Papel [3]
# t -> Tijera [4]
# q -> Termina la captura


class gui_capturador():
    def __init__(self):

        self.f = None
        self.camara = 0
        self.PATH = 'dataset/'
        self.NAME = 'game.csv'
        self.FULL_NAME = self.PATH + self.NAME
        self.writer = None
        self.ROI = None
        self.ventana = Tk()
        self.ventana.title("Imágenes de entrenamiento")

        # Componentes del GUI
        self.fontformat_title = TkFont.Font(family="Arial", size=15, weight="bold")
        self.fontformat_sub = TkFont.Font(family="Arial", size=12)

        #Cámara
        self.Video = Label(self.ventana)
        self.Video.grid(column=1, row=1, padx=5, pady=5, rowspan=7)

        #Instrucciones
        self.txt1 = Label(self.ventana, text="Instrucciones", font=self.fontformat_title)
        self.txt1.grid(column=2, row=1, columnspan=2)

        self.txt2 = Label(self.ventana, text="Empezar", font=self.fontformat_sub)
        self.txt2.grid(column=2, row=2)
        self.btn1 = Button(self.ventana, text="Ok", width=5, command=self.save1)
        self.btn1.grid(column=3, row=2, padx=5, pady=5)

        self.txt3 = Label(self.ventana, text="Terminar", font=self.fontformat_sub)
        self.txt3.grid(column=2, row=3)
        self.btn2 = Button(self.ventana, text="Ok", width=5, command=self.save2)
        self.btn2.grid(column=3, row=3, padx=5, pady=5)

        self.txt4 = Label(self.ventana, text="Piedra", font=self.fontformat_sub)
        self.txt4.grid(column=2, row=4)
        self.btn3 = Button(self.ventana, text="Ok", width=5, command=self.save3)
        self.btn3.grid(column=3, row=4, padx=5, pady=5)

        self.txt5 = Label(self.ventana, text="Papel", font=self.fontformat_sub)
        self.txt5.grid(column=2, row=5)
        self.btn4 = Button(self.ventana, text="Ok", width=5, command=self.save4)
        self.btn4.grid(column=3, row=5, padx=5, pady=5)

        self.txt6 = Label(self.ventana, text="Tijera", font=self.fontformat_sub)
        self.txt6.grid(column=2, row=6)
        self.btn5 = Button(self.ventana, text="Ok", width=5, command=self.save5)
        self.btn5.grid(column=3, row=6, padx=5, pady=5)

        self.txt7 = Label(self.ventana, text="Quitar", font=self.fontformat_sub)
        self.txt7.grid(column=2, row=7)
        self.btn6 = Button(self.ventana, text="Ok", width=5, command=self.salir)
        self.btn6.grid(column=3, row=7, padx=5, pady=5)

        global cap
        cap = cv2.VideoCapture(0)
        self.visualizar()

    def visualizar(self):
        global cap

        font = cv2.FONT_HERSHEY_COMPLEX
        fontScale = 1
        color = (0, 0, 255)
        thickness = 1

        x, y = 300, 100
        w, h = 300, 300
        th = 10  # Factor para que no aparezca el rectángulo al guardar la imagen

        self.f = open(self.FULL_NAME, 'a', newline='')
        self.writer = csv.writer(self.f)

        if cap is not None:
            ret, frame = cap.read()

            if ret == True:
                frame = cv2.flip(frame, 1)
                self.ROI = frame[y:y + h, x:x + w]

                # Dibujamos el ROI
                cv2.rectangle(frame, (x - th, y - th), (x + w + th, y + h + th), color, thickness=5)
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                im = Image.fromarray(frame)
                img = ImageTk.PhotoImage(image=im)
                self.Video.configure(image=img)
                self.Video.image = img
                self.Video.after(10, self.visualizar)
            else:
                self.f.close()
                print('No se pudo conectar con la cámara')

    def save1(self):
        # Definiendo el nombre de la imagen
        # El formato de tiempo para guardar la imagen será: YY/MM/DD_H:M:S
        now = datetime.now()
        dt_str = now.strftime("%Y%m%d_%H%M%S")
        name = f'{dt_str}.jpg'
        dim = (300, 300)
        self.ROI = cv2.resize(self.ROI, dim, interpolation=cv2.INTER_LINEAR)
        cv2.imwrite(self.PATH + name, self.ROI)
        data = [name, 0]
        self.writer.writerow(data)
        print('Instrucción Empezar guardada con éxito')

    def save2(self):
        # Definiendo el nombre de la imagen
        # El formato de tiempo para guardar la imagen será: YY/MM/DD_H:M:S
        now = datetime.now()
        dt_str = now.strftime("%Y%m%d_%H%M%S")
        name = f'{dt_str}.jpg'
        dim = (300, 300)
        self.ROI = cv2.resize(self.ROI, dim, interpolation=cv2.INTER_LINEAR)
        cv2.imwrite(self.PATH + name, self.ROI)
        data = [name, 1]
        self.writer.writerow(data)
        print('Instrucción Terminar guardada con éxito')

    def save3(self):
        # Definiendo el nombre de la imagen
        # El formato de tiempo para guardar la imagen será: YY/MM/DD_H:M:S
        now = datetime.now()
        dt_str = now.strftime("%Y%m%d_%H%M%S")
        name = f'{dt_str}.jpg'
        dim = (300, 300)
        self.ROI = cv2.resize(self.ROI, dim, interpolation=cv2.INTER_LINEAR)
        cv2.imwrite(self.PATH + name, self.ROI)
        data = [name, 2]
        self.writer.writerow(data)
        print('Instrucción Piedra guardada con éxito')

    def save4(self):
        # Definiendo el nombre de la imagen
        # El formato de tiempo para guardar la imagen será: YY/MM/DD_H:M:S
        now = datetime.now()
        dt_str = now.strftime("%Y%m%d_%H%M%S")
        name = f'{dt_str}.jpg'
        dim = (300, 300)
        self.ROI = cv2.resize(self.ROI, dim, interpolation=cv2.INTER_LINEAR)
        cv2.imwrite(self.PATH + name, self.ROI)
        data = [name, 3]
        self.writer.writerow(data)
        print('Instrucción Papel guardada con éxito')

    def save5(self):
        # Definiendo el nombre de la imagen
        # El formato de tiempo para guardar la imagen será: YY/MM/DD_H:M:S
        now = datetime.now()
        dt_str = now.strftime("%Y%m%d_%H%M%S")
        name = f'{dt_str}.jpg'
        dim = (300, 300)
        self.ROI = cv2.resize(self.ROI, dim, interpolation=cv2.INTER_LINEAR)
        cv2.imwrite(self.PATH + name, self.ROI)
        data = [name, 4]
        self.writer.writerow(data)
        print('Instrucción Tijera guardada con éxito')

    def salir(self):
        self.f.close()
        cv2.destroyAllWindows()
        self.ventana.destroy()


def capture_dataset():
    my_app = gui_capturador()
    my_app.ventana.mainloop()

capture_dataset()