import tkinter
import numpy as np
from tkinter import *
from capturador import capture_dataset
from play import gui_play
from PIL import Image


# from model import fit

# Este archivo desplegará un menú para seleccionar el tipo de acción que se realizará

def open_capture():
   capture_dataset()
    

def quite_program():
    window.destroy()


def start_game():
    file = 'modelos/Modelo_20211214_011643.pt'
    gui_play(file)
    
# def trainModel():
#    fit()


class MainApp:

    def __init__(self, window):
        # Paddings
        button_padx = 24
        labels_pady = 16
        frame_pad = 16

        # Colors
        wind_bg = "#0099FF"
        white = "#fff"
        black = "#000"
        gray_light = "#dedede"
        button_color = "#00FFE5"

        # Init window
        self.wind = window
        self.wind.title('Rock, paper or scissors')
        self.wind.configure(bg=wind_bg)

        # Title
        title_text = 'Welcome back my friend!'
        title_label = tkinter.Label(self.wind, text=title_text, pady=24, padx=24, fg="#fff",
                                    bg="#FF9900", font=("Lato", 36, "bold"))
        title_label.grid(row=0, column=0)

        # Frame Container
        frame_text = "Select an option"
        frame = tkinter.LabelFrame(self.wind, text=frame_text, bd=4, bg=wind_bg,
                                   padx=frame_pad, foreground=white, font=("Lato", 11))
        frame.grid(row=1, column=0, pady=frame_pad)

        # Play option
        play_text = 'Engage in an exciting battle against the machine.'
        play_label = tkinter.Label(frame, text=play_text, padx=24, bg=wind_bg,
                                   pady=labels_pady, foreground=white, font=("Heveltica", 10),
                                   command=start_game)
        play_label.grid(row=3, column=0, sticky="w")

        play_button = tkinter.Button(frame, text='PLAY', bg=button_color, foreground=black,
                                     padx=button_padx, pady=4, font=("Heveltica", 8, "bold"))
        play_button.grid(row=3, column=1, sticky="we")

        # Train option
        train_text = 'Too easy? Train the machine and make it invincible!'
        train_label = tkinter.Label(frame, text=train_text, padx=24, bg=wind_bg,
                                    pady=labels_pady, foreground=white, font=("Heveltica", 10))
        train_label.grid(row=4, column=0, sticky="w")

        train_button = tkinter.Button(frame, text='TRAIN', bg=button_color, foreground=black,
                                      padx=button_padx, pady=4, font=("Heveltica", 8, "bold"))
        train_button.grid(row=4, column=1, sticky="we")

        # Capture option
        capture_text = 'To train you will need equipment. Capture your photos now.'
        capture_label = tkinter.Label(frame, text=capture_text, padx=24, bg=wind_bg,
                                      pady=labels_pady, foreground=white, font=("Heveltica", 10))
        capture_label.grid(row=5, column=0, sticky="w")

        capture_button = tkinter.Button(frame, text='CAPTURE',
                                        bg=button_color, foreground=black, 
                                        command=open_capture, padx=button_padx,
                                        pady=4, font=("Heveltica", 8, "bold"))
        capture_button.grid(row=5, column=1, sticky="we")

        # Animation
        file = 'animation_game.gif'
        info = Image.open(file)
        frames = info.n_frames

        im = [tkinter.PhotoImage(file=file, format=f'gif -index {i}') for i in range(frames)]

        count = 0

        def animation(count):
            im2 = im[count]
            tkinter.Label(self.wind, image=im2, bg=wind_bg).grid(row=6, column=0, sticky="we")

            count += 1
            if count == frames:
                count = 0

            self.wind.after(250, lambda: animation(count))
            
        
        
        # Exit button
        exit_button = tkinter.Button(self.wind, text='EXIT', command=quite_program,
                                     bg="#002b91", foreground="#fff", font=("Heveltica", 8, "bold"))
        exit_button.grid(row=7, column=0, sticky="we")


if __name__ == '__main__':
    window = tkinter.Tk()
    application = MainApp(window)
    window.mainloop()
