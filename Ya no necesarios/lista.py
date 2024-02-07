import cv2

def detect_cameras(max_cameras=10):
    """
    Intenta abrir cámaras desde el índice 0 hasta el índice max_cameras-1.
    Devuelve una lista de los índices de las cámaras que pudo abrir.
    """
    cameras_detected = []
    for index in range(max_cameras):
        cap = cv2.VideoCapture(index)
        if cap is None or not cap.isOpened():
            cap.release()
            break
        cameras_detected.append("Camara "+str(index+1))
        cap.release()
    return cameras_detected

cameras = detect_cameras()
print("Cámaras detectadas:")
for index in cameras:
    print(f"Cámara índice: {index}")