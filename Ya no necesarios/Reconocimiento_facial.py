import cv2

# Cargar el clasificador de rostros pre-entrenado
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')


# Cargar una imagen desde el archivo
imagen = cv2.imread('nombre_de_la_imagen.jpg')

# Iniciar la cámara (si no tienes una, puedes probar con un video)
cap = cv2.VideoCapture(0)

while True:
    # Leer un frame de la cámara
    ret, frame = cap.read()

    # Convertir a escala de grises para el reconocimiento facial
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    # Detectar rostros en el frame
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

    # Dibujar un rectángulo alrededor de cada rostro detectado
    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)

    # Mostrar el frame con los rostros detectados
    cv2.imshow('Reconocimiento Facial', frame)

    # Si se presiona la tecla 'q', salir del bucle
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Liberar la cámara y cerrar las ventanas de OpenCV
cap.release()
cv2.destroyAllWindows()