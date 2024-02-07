import pygetwindow as gw
import pyautogui
import time
import cv2
import numpy as np
from PIL import Image



num_webcam = 1 #este puede ser 0 o 1 




def CapturaImagen_Webcam():
    # Iniciar la cámara
    cap = cv2.VideoCapture(num_webcam)  # El argumento '0' indica que se utilizará la cámara predeterminada

    ret, frame = cap.read()# Leer un frame de la cámara    
    cv2.imshow('Cámara Web', frame)# Mostrar el frame en una ventana
    cap.release() #libera la cámara ya que no la utilice
    cv2.waitKey(0) # Espera
    cv2.destroyAllWindows()
### end de la captura de imagen


def CapturaImagen_Wyze_Cam_v3():
    # 1) Busca la ventana donde está BlueStacks App Player
    ventana_activa = gw.getWindowsWithTitle('BlueStacks App Player')[0]# Encuentra la ventana de la aplicación que deseas capturar
    ventana_activa.maximize()# Maximisa la ventana de la aplicación
    ventana_activa.activate() #Pone fullscreen como principal
    pyautogui.sleep(1)# Espera un momento para asegurarte de que la ventana está completamente activa
    screenshot = pyautogui.screenshot(region=(ventana_activa.left, ventana_activa.top, ventana_activa.width, ventana_activa.height))
    screenshot.save('captura_de_pantalla.png')# Guarda la captura de pantalla

    time.sleep(0.1)

    # 2) Recorta la imagen para que encaje lo de la pantalla
    ancho, alto = screenshot.size # Obtener el ancho y alto
    x_0 = int(ancho * 0.05019191) 
    y_0 = int(alto * 0.3338888)
    x_1 = int(ancho - (ancho * 0.023619722))
    y_1 = int(alto - (alto * 0.0611111))

    coordenadas = (y_0, x_0, x_1, y_1)  # Ejemplo: recorta un cuadrado de (100, 100) a (300, 300)
    imagen_recortada = screenshot.crop(coordenadas)# Recortar la imagen
    imagen_recortada.save('recorte.png')# Guardar la imagen recortada

    # 3) Mostrar la imagen recortada usando OpenCV
    imagen_recortada_cv2 = cv2.cvtColor(np.array(imagen_recortada), cv2.COLOR_RGB2BGR)
    cv2.imshow('Imagen Recortada', imagen_recortada_cv2)
    cv2.waitKey(0) # Espera
    cv2.destroyAllWindows()
##end de CapturaImagen


tipo = 2
if tipo == 1:
    # Para la captura por bluestacks
    CapturaImagen_Wyze_Cam_v3()
elif tipo == 2:
    # para la captura por webcam
    CapturaImagen_Webcam()
elif tipo == 3:
    # para la captura por https://view.wyze.com/live
    
    pass
####

















'''
while True:
    # Muestra la imagen
    cv2.imshow('Imagen en tiempo real', imagen_recortada)
    time.sleep(0.1)# Espera 0.1 segundos (100 milisegundos)
    if cv2.waitKey(1) & 0xFF == ord('q'): # Si se presiona la tecla 'q', termina el bucle
        break
    ####
###

cv2.destroyAllWindows() # Cierra las ventanas de OpenCV
'''


print("Código finalizado")