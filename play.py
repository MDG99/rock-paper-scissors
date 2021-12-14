from tkinter import *
from PIL import Image
from PIL import ImageTk
import imutils
import time
import tkinter.font as TkFont
import numpy as np
import torch
import cv2
import random
from torchvision import transforms
import time
from threading import Timer,Thread,Event


classes = ["Empezar", "Terminar", "Piedra", "Papel", "Tijera"]
cap = None
victorias = 0
empates = 0
derrotas = 0
th = 5
x, y = 150, 50
w = 300


class gui_play:
    def __init__(self, file):

        self.ventana = Tk()
        #self.ventana.geometry("1100x600")
        self.ventana.title("Juego")

        #Componentes del GUI
        self.fontformat_title =TkFont.Font(family="Arial", size=15, weight="bold")
        self.fontformat_sub = TkFont.Font(family="Arial", size=12)

        self.btnCapturar = Button(self.ventana, text="Jugar", width=20, command=self.Jugar)
        self.btnCapturar.grid(column=3, row=6, padx=5, pady=5)

        self.Video = Label(self.ventana)
        self.Video.grid(column=1, row=1, padx=5, pady=5, rowspan=4)

        self.lblVideo = Label(self.ventana, text="Jugador", font=self.fontformat_title)
        self.lblVideo.grid(column=1, row=0)

        self.txt1 = Label(self.ventana, text="Jugada del CPU", font=self.fontformat_title)
        self.txt1.grid(column=2, row=0)

        self.lblImg1 = Label(self.ventana)
        self.lblImg1.grid(column=2, row=1, padx=5, pady=5, rowspan=4)

        self.txtaux = Label(self.ventana, text="Puntaje", font=self.fontformat_title)
        self.txtaux.grid(column=3, row=1, columnspan=2)

        global victorias, empates, derrotas
        self.txt3 = Label(self.ventana, text=f"Victorias: {victorias}", font=self.fontformat_sub)
        self.txt3.grid(column=3, row=2)

        self.txt4 = Label(self.ventana, text=f"Derrotas: {empates}", font=self.fontformat_sub)
        self.txt4.grid(column=3, row=3)

        self.txt5 = Label(self.ventana, text=f"Empates: {derrotas}", font=self.fontformat_sub)
        self.txt5.grid(column=3, row=4)

        self.txtplayer = Label(self.ventana, text="", font=self.fontformat_sub)
        self.txtplayer.grid(column=1, row=6)

        self.txtCPU = Label(self.ventana, text="", font=self.fontformat_sub)
        self.txtCPU.grid(column=2, row=6)

        #Definición de transformaciones
        self.transform = transforms.Compose([
            transforms.ToPILImage(),
            transforms.Resize((227, 227)),
            transforms.ToTensor()
        ])

        #Definición del modelo
        self.my_net = torch.load(file)
        print("Modelo Cargado")

        global cap
        cap = cv2.VideoCapture(2)

        #Bandera indicadora del comienzo del juego
        self.iniciado = False

        #Imagen de inicio del juego
        image1 = cv2.imread("imgs/Empezar.jpeg", cv2.IMREAD_COLOR)
        image1 = cv2.resize(image1, (480, 480), cv2.INTER_LINEAR)
        image1 = cv2.cvtColor(image1, cv2.COLOR_BGR2RGB)
        im1 = Image.fromarray(image1)
        img1 = ImageTk.PhotoImage(image=im1)
        self.lblImg1.configure(image=img1)
        self.lblImg1.image = img1

        self.visualizar()

    def visualizar(self):
        global cap
        global x, y, w, th

        if cap is not None:
            ret, frame = cap.read()
            if ret == True:
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                cv2.rectangle(frame, (x-th, y-th), (x+w+th, y+w+th), (255, 0, 0), 5)
                im = Image.fromarray(frame)
                img = ImageTk.PhotoImage(image=im)
                self.Video.configure(image=img)
                self.Video.image = img
                self.Video.after(10, self.visualizar)
            else:
                self.lblVideo.image = ""
                cap.release()

    def Jugar(self):

        global cap, inicio
        global classes
        global x, y, w

        ret, frame = cap.read()
        imCrop = frame[y:y+w, x:x+w] #ROI
        cv2.imwrite("jugada.jpg", imCrop)

        # Predicción usando el modelo
        raw = self.transform(imCrop).float()
        raw = raw.unsqueeze(0)
        # input_test = Variable(row)
        output = self.my_net(raw)
        idx = output.data.cpu().numpy().argmax()
        print(f'La predicción fue {classes[idx]} idx: {idx}')

        # row_prediction = output.data.cpu().numpy()
        # print(f"Row prediction: {row_prediction}")

        if idx == 0:
            self.iniciado = True
            inicio = time.time()
            self.temporizador(2)

            #Vuelves a hacer la predicción
            ret, frame = cap.read()
            imCrop = frame[y:y + w, x:x + w]  # ROI
            cv2.imwrite("jugada.jpg", imCrop)

            # Predicción usando el modelo
            raw = self.transform(imCrop).float()
            raw = raw.unsqueeze(0)
            # input_test = Variable(row)
            output = self.my_net(raw)
            idx = output.data.cpu().numpy().argmax()
            print(f'La predicción fue {classes[idx]} idx: {idx}')

        if idx == 1:
            self.iniciado = False
            # Se abre la imagen de juego finalizado
            image1 = cv2.imread("imgs/Finalizado.jpeg", cv2.IMREAD_COLOR)
            image1 = cv2.resize(image1, (480, 480), cv2.INTER_LINEAR)
            image1 = cv2.cvtColor(image1, cv2.COLOR_BGR2RGB)
            im1 = Image.fromarray(image1)
            img1 = ImageTk.PhotoImage(image=im1)
            self.lblImg1.configure(image=img1)
            self.lblImg1.image = img1

        if self.iniciado:
            #fin = time.time()

            #if inicio == 0:
            #    inicio = time.time()
            #    self.temporizador(2)

            #if fin - inicio > 1.0:
            #    self.temporizador(1)
            #elif fin - inicio > 2.0:
            #    self.temporizador(0)
            #elif fin - inicio > 3.0:
            #    inicio = 0

            # Elección de la jugada por parte del CPU
            jugada_cpu = random.randint(2, 4)
            opciones_str = ["imgs/Piedra.jpeg", "imgs/Papel.jpeg", "imgs/Tijera.jpeg"]
            jugada_cpu_str = opciones_str[jugada_cpu - 2]
            print(f'La jugada del CPU fue {classes[jugada_cpu]} idx : {jugada_cpu}')

            # Se elige una imagen para la jugada del CPU
            image1 = cv2.imread(jugada_cpu_str, cv2.IMREAD_COLOR)
            image1 = cv2.resize(image1, (480, 480), cv2.INTER_LINEAR)
            image1 = cv2.cvtColor(image1, cv2.COLOR_BGR2RGB)

            # Se muestra la imagen seleccionada por la CPU
            im1 = Image.fromarray(image1)
            img1 = ImageTk.PhotoImage(image=im1)
            self.lblImg1.configure(image=img1)
            self.lblImg1.image = img1

            self.txtplayer['text'] = f'Player: {classes[idx]}'
            self.txtCPU['text'] = f'CPU: {classes[jugada_cpu]}'

            # Ejecutamos la jugada
            self.logica(player=idx, cpu=jugada_cpu)


    def logica(self, player, cpu):
        global victorias, empates, derrotas

        #Piedra 2
        #Papel 3
        #Tijera 4

        #Empate
        if player == cpu:
            empates += 1

        # Piedra vs Tijera
        elif player == 2 and cpu == 4:
            victorias += 1

        # Papel vs Piedra
        elif player == 3 and cpu == 2:
            victorias += 1

        # Tijera vs Papel
        elif player == 4 and cpu == 3:
            victorias += 1

        else:
            derrotas += 1

        #Actualizamos le puntaje
        self.txt3['text'] = f"Victorias: {victorias}"
        self.txt4['text'] = f"Derrotas: {derrotas}"
        self.txt5['text'] = f"Empates: {empates}"

    def temporizador(self, idx):  # runs in main thread
        imagenes = ["imgs/1.jpeg", "imgs/2.jpeg", "imgs/3.jpeg"]
        image1 = cv2.imread(imagenes[idx], cv2.IMREAD_COLOR)
        image1 = cv2.resize(image1, (480, 480), cv2.INTER_LINEAR)
        #cv2.imshow("Cuenta Regresiva", image1)
        #cv2.waitKey(0)
        #image1 = cv2.cvtColor(image1, cv2.COLOR_BGR2RGB)

        # Se muestra la imagen seleccionada por la CPU
        im1 = Image.fromarray(image1)
        img1 = ImageTk.PhotoImage(image=im1)
        self.lblImg1.configure(image=img1)
        self.lblImg1.image = img1



file = 'modelos/Modelo_20211214_011643.pt'
my_app = gui_play(file)
my_app.ventana.mainloop()
