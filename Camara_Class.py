import time
import os
import csv
import cv2
import face_recognition
from  time import sleep

import DataBase_Class
Procesar_imagen_sincrona = True

tolerancia_ia = 0.45
# tolerancia_ia = 0.4 
# con el 0.35 jala chido.









Mostrar_video = True # ESTE NO SE MODIFICA


def Procesar_Frame_update(Camara, frame_original):
    
    # aqui reduce la resolución de frame_cap para que vaya mas rapido y no a su resolución total.
    division = 2 
    frame_cap = cv2.resize(frame_original, (   round(Camara._ancho/division)  , round(Camara._alto/division))) #lo reduce para que vaya en putiza

    # Encuentra todas las caras del frame_actual
    face_locations = face_recognition.face_locations(frame_cap)
    num_caras = len(face_locations)
    if num_caras > 0 and Procesar_imagen_sincrona:# si hay caras
        face_encodings = face_recognition.face_encodings(frame_cap, face_locations)


        # almacenamientos:
        face_names = [] # aqui almacena los nombres de los weyes estos.
        face_codigos = [] # aqui almacena los codigos
        quien_es_quien = [] # aqui almacena la index de los weyes estos.

        # for de cada cara
        for i_face_encoding, i_face_location in  zip(face_encodings, face_locations):
            Coincidencias = face_recognition.compare_faces(Camara.known_face_encodings, i_face_encoding, tolerance=tolerancia_ia)        
            # las coincidencias imprime por cada cara en la foto un array algo así: [ False, True, False, False, False] 
            indices_true = []
            for i, valor in enumerate(Coincidencias):
                if valor:
                    indices_true.append(i) #le mete al array el indice donde hay un True
                # if donde es true
            #FOR i, valor 

            cantidad_true = len(indices_true)
            if cantidad_true== 1: # si solo hay uno entonces sin pedos nada mas agarra donde esta el primer true
                index_del_wey = indices_true[0]

                i_nombre = Camara.known_vatos_info[index_del_wey]
                i_codigo = Camara.known_codigos_info[index_del_wey]
                
                # PASO IMPORTANTE
                DataBase_Class.Deteccion_persona_Conocida( int( i_codigo)) # Envia esto a la de base de datos para que procese a que wey detectó
                
                face_names.append(i_nombre)
                face_codigos.append(i_codigo)
                quien_es_quien.append(index_del_wey) # guarda el index
            else: 
                # PASO IMPORTANTE   

                division1 = 3
                frame_cap_unknown_reducido = cv2.resize(frame_original, (   round(Camara._ancho/division1)  , round(Camara._alto/division1))) #lo reduce para que vaya en putiza

                DataBase_Class.Deteccion_Desconocido(frame_cap_unknown_reducido) # Envia esto a la de base de datos para que procese a que wey detectó
                
                face_names.append("Unknown")
                face_codigos.append("Unknown")
                quien_es_quien.append("Unknown") #no detectó el index es desconocido el vatillo
            ##IF de cantidad de true 

        ## FOR Face Encoding

        
        # ESTE ES EL FOR FINAL QUE DICE a quien encontró en la foto
        # Ahora imprime en la imagen las localizaciones de quien es cada wey
        for i_location, i_name, i_codigo, i_quien_es in zip(face_locations, face_names, face_codigos, quien_es_quien):
            color =  (50, 50, 255) #color rojillo
            if i_quien_es != "Unknown": # si no es un unknown
                color = (125, 220, 0) # color verdecillo
            ###end de quien es no es nul

            #print(i_quien_es)
            # pone los rectangulos de a quienes encontró.
            if Mostrar_video:
                cv2.rectangle(frame_original, (i_location[3]*division, i_location[2]*division), (i_location[1]*division, i_location[2]*division + 30), color, -1)
                cv2.rectangle(frame_original, (i_location[3]*division, i_location[0]*division), (i_location[1]*division, i_location[2]*division), color, 2)
                cv2.putText(frame_original, i_name, (i_location[3]*division, i_location[2]*division + 20), 2, 0.7, (255, 255, 255), 1)
            ### si se puede mostrar el video



        ### for de i_location, i_name, i_quien_es
    ##IF del numero de caras >0 
    
    ## aca hace las configuraciones para poner la imagen en el frame
    frame_original = cv2.cvtColor(frame_original, cv2.COLOR_BGR2RGB)
    frame_original = cv2.resize(frame_original, (   round(Camara._ancho)  , round(Camara._alto)))# lo regresa a su resolución original por si se redujo para acelerar el procesamiento
    
    return frame_original
### end de procesar_frame_ret







def Obtener_Camaras_on_pc(max_cameras=10):
    detected_cameras_name = []
    detected_cameras_index = []
    cam_Caps = []

    contador_camaras = 0
    for index in range(max_cameras): # hace la iteracion hasta el maximo que colocamos
        cap = cv2.VideoCapture(index)
        

        if cap is None or not cap.isOpened(): # esto se ejecuta si no pudo abrir la camara osea que no encontró ninguna
            cap.release()
            break
        # end
        # Si pudo abrir la cámara, la añade a la lista y la libera        
        detected_cameras_name.append("Cámara "+ str(index + 1))
        detected_cameras_index.append(index)

        if contador_camaras == 0: # si no es cero entonces hace relase.
            cap_0 = cap #no le hace relase, la guarda para enviarla en el return
        else:
            cap.release()
        ### end de contador_camaras == 0

        contador_camaras += 1
    return detected_cameras_index, detected_cameras_name, cap_0
### end de obtener camaras en la pc





# Clase de la camarita
class CamaraObj:



    def __init__(self, tipo, parametro_1, obj):  
        
        obj.set_texto_progress(  "2/2"  +" Cargando Cámara/s...")
        obj.set_num_texto_progress(  "Le va tomar unos segundos " )

        self._NumCamera = 0 
        self._Estado = "Detenida"
        self._CargaFoto = [] # Esto se llena si es de tipo imagen
        self._ancho= "null" #La resolución de la camara
        self._alto = "null"
        self._cambiando_camara = False

        # Acá la info de encodings
        self.known_face_encodings = []
        self.known_vatos_info = []
        self.known_codigos_info = []
        
        # inicializa del tipo
        if tipo == "webcam":
            self._tipo = "webcam"
            self._NumCamera = parametro_1
            print("Inicializando cámara #"+ str(parametro_1)+ "...")
            t_0 = time.time()
            detected_cameras_index, detected_cameras_name,cap_0 = Obtener_Camaras_on_pc()

            self._webcam_Control = cap_0
            # Obtiene la resolución que tenemos para nuestra camarita para después utilizarla para reducir la resolución y vaya mas rapido
            self._ancho = int(self._webcam_Control.get(cv2.CAP_PROP_FRAME_WIDTH))
            self._alto = int(self._webcam_Control.get(cv2.CAP_PROP_FRAME_HEIGHT))

            # aca toma el tiempo:
            t_1 = time.time()
            dt = t_1 - t_0
            print("Camara #"+ str(parametro_1) +" cargada. "+ "Le tomó "+ str(round(dt, 2))+ " segundos en cargar")

            ## aqui empieza a cargar la camara:
            
            self._detected_cameras_index = detected_cameras_index #lo guarda el index
            self._detected_cameras_name = detected_cameras_name # lo guarda el name

        elif tipo == "bluestacks":
            self._tipo = "bluestacks"
        elif tipo == "browser":
            self._tipo = "browser"
        elif tipo == "imagen":
            self._tipo = "imagen"
            self._CargaFoto = parametro_1
        ### if elses del tipo de camara que se inicializa

        obj.set_texto_progress(  "")
        obj.set_num_texto_progress(  "Listo" )
        obj.set_progress_barra(100)
    ### fx inicialización 


    def selecciona_camara(self, numcamara=0):
        
        self._cambiando_camara = True

        self._webcam_Control = cv2.VideoCapture(numcamara, cv2.CAP_DSHOW) # Se usa la camara del parametro (inicia desde 0 el index de las camáronas)
        self._ancho = int(self._webcam_Control.get(cv2.CAP_PROP_FRAME_WIDTH))
        self._alto = int(self._webcam_Control.get(cv2.CAP_PROP_FRAME_HEIGHT))
        self._cambiando_camara = False
    ### end de selecciona de camara:


    def Tomar_Captura(self):
        # HACE UN RETURN DE UN TRUE y una imagen si es valida
        if self._tipo == "webcam":
            ## si es la webcam entonces procesa la imagen de la siguiente manera:
            return self._webcam_Control.read()# Captura un fotograma del video
            #return True, cv2.imread("ImagesSrc/Foto_3aaa.png")# Captura un fotograma del video
        elif self._tipo == "bluestacks":
            pass
        elif self._tipo == "browser":
            pass
        elif self._tipo == "imagen":
            return cv2.imread(self._CargaFoto) # debe cargarla desde cero cada vez sino estará sobreescribiendo lo mismo y se verá bien raro
        ### del tipo de camara
    ####

    


    def start(self):
        self._Estado = "Grabando"
        while True:
            if self._tipo == "webcam":
                ## si es la webcam entonces procesa la imagen de la siguiente manera:
                ret, frame = self._webcam_Control.read()# Captura un fotograma del video
            elif self._tipo == "bluestacks":
                pass
            elif self._tipo == "browser":
                pass
            elif self._tipo == "imagen":
                ret = True #por defecto debería ser valida
                frame = cv2.imread(self._CargaFoto) # debe cargarla desde cero cada vez sino estará sobreescribiendo lo mismo y se verá bien raro
            ### del tipo de camara

            if ret:# Si la captura es exitosa procesa:    
                cv2.putText(frame, '', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)# Procesa cada frame (en este caso, agrega un texto)
                titulo_implot = 'Video Stream | Camara #'+ str(self._NumCamera) + " | " + 'Presiona la tecla "q" para salir'
                face_locations, face_names, quien_es_quien = Procesar_Imagen(frame) #le envia el frame a que lo procese
                # Ahora imprime en la imagen las localizaciones de quien es cada wey
                for i_location, i_name, i_quien_es in zip(face_locations, face_names, quien_es_quien):
                    color =  (50, 50, 255) #color rojillo
                    if i_quien_es != "Null":
                        color = (125, 220, 0)
                    ###end de quien es no es nul
                    print(i_quien_es)
                    # pone los rectangulos de a quienes encontró.
                    cv2.rectangle(frame, (i_location[3], i_location[2]), (i_location[1], i_location[2] + 30), color, -1)
                    cv2.rectangle(frame, (i_location[3], i_location[0]), (i_location[1], i_location[2]), color, 2)
                    cv2.putText(frame, i_name, (i_location[3], i_location[2] + 20), 2, 0.7, (255, 255, 255), 1)
                ### for de i_location, i_name, i_quien_es
                print("Iterando imagen:")
                cv2.imshow( titulo_implot , frame)# Muestra el frame en una ventana
            ### del if de captura exitosa

            if cv2.waitKey(1) & 0xFF == ord('q'): # Verifica si se presiona la tecla 'q' para salir del bucle
                self.stop()
                break
            ### del if de tecla
    ### fx Start







    def stop(self):
        if self._tipo == "webcam":
            self._webcam_Control.release()
            cv2.destroyAllWindows()
        elif self._tipo == "bluestacks":
            pass
        elif self._tipo == "browser":
            pass
        elif self._tipo == "imagen":
            pass
        ### del tipo de camara

        self._Estado = "Detenida"
    #### fx Stop
### de la Clase_Camara
