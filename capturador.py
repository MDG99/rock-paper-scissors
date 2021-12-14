import cv2
import csv
from datetime import datetime

# La función Caoture_dataset te permite caoturar una imagen para tu dataset y guardarla clasificarla como se debe
# b -> Instrucción para empezar el juego [0]
# m -> Instrucción para acabar el juego [1]
# r -> Piedra [2]
# p -> Papel [3]
# t -> Tijera [4]
# q -> Termina la captura


def capture_dataset():
    camera = 2  # Webcam USB
    cap = cv2.VideoCapture(camera, )
    modo_captura = True
    PATH = 'dataset/'
    NAME = 'game.csv'
    FULL_NAME = PATH + NAME

    font = cv2.FONT_HERSHEY_COMPLEX
    fontScale = 1
    color = (0, 0, 255)
    thickness = 1

    x, y = 300, 100
    w, h = 300, 300
    th = 10 #Factor para que no aparezca el rectángulo al guardar la imagen

    f = open(FULL_NAME, 'a', newline='')
    writer = csv.writer(f)

    while modo_captura:
        try:
            ret, frame = cap.read()
            frame = cv2.flip(frame, 1)
            ROI = frame[y:y + h, x:x + w]

            # Escribimos las instrucciones
            frame = cv2.putText(frame, 'Empezar  [b]', (10, 50), font, fontScale, color, thickness)
            frame = cv2.putText(frame, 'Terminar [m]', (10, 100), font, fontScale, color, thickness)
            frame = cv2.putText(frame, 'Piedra   [r]', (10, 150), font, fontScale, color, thickness)
            frame = cv2.putText(frame, 'Papel    [p]', (10, 200), font, fontScale, color, thickness)
            frame = cv2.putText(frame, 'Tijera   [t]', (10, 250), font, fontScale, color, thickness)
            frame = cv2.putText(frame, 'Quitar   [q]', (10, 300), font, fontScale, color, thickness)

            # Dibujamos el ROI
            cv2.rectangle(frame, (x - th, y - th), (x + w + th, y + h + th), color, thickness=5)


            cv2.imshow("Dataset", frame)

            key = cv2.waitKey(1)


            if key == ord('q'):
                modo_captura = False
                f.close()
                cv2.destroyAllWindows()
            else:
                # Definiendo el nombre de la imagen
                # El formato de tiempo para guardar la imagen será: YY/MM/DD_H:M:S
                now = datetime.now()
                dt_str = now.strftime("%Y%m%d_%H%M%S")
                name = f'{dt_str}.jpg'

                if key == ord('b'):
                    # Empezar el Juego
                    dim = (300, 300)
                    ROI = cv2.resize(ROI, dim,  interpolation=cv2.INTER_LINEAR)
                    cv2.imwrite(PATH + name, ROI)
                    data = [name, 0]
                    writer.writerow(data)
                    print('Instrucción Empezar guardada con éxito')

                elif key == ord('m'):
                    # Terminar el Juego
                    cv2.imwrite(PATH + name, ROI)
                    data = [name, 1]
                    writer.writerow(data)
                    print('Instrucción Terminar guardada con éxito')


                elif key == ord('r'):
                    # Piedra
                    cv2.imwrite(PATH + name, ROI)
                    data = [name, 2]
                    writer.writerow(data)
                    print('Instrucción Piedra guardada con éxito')

                elif key == ord('p'):
                    # Papel
                    cv2.imwrite(PATH + name, ROI)
                    data = [name, 3]
                    writer.writerow(data)
                    print('Instrucción Papel guardada con éxito')

                elif key == ord('t'):
                    # Tijera
                    cv2.imwrite(PATH + name, ROI)
                    data = [name, 4]
                    writer.writerow(data)
                    print('Instrucción Tijera guardada con éxito')
        except:
            modo_captura = False
            print('No se pudo conectar con la cámara')

