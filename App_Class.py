import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from tkinter import PhotoImage, Label
import csv
from time import sleep
import datetime
from PIL import Image, ImageTk
import threading
import os
import subprocess
import numpy as np



############# ESTO
import Camara_Class
import Add_Alumnos_class
import DataBase_Class






def obtener_hora_actual():
    ahora = datetime.datetime.now()
    hora = ahora.hour
    minutos = ahora.minute
    segundos = ahora.second
    # Formateo con ceros a la izquierda para números menores a 10
    hora_str = str(hora).zfill(2)
    minutos_str = str(minutos).zfill(2)
    segundos_str = str(segundos).zfill(2)
    return f"{hora_str}:{minutos_str}:{segundos_str}"
# obtener la hora actual




def Abrir_Lista_CSV():
    archivo_original = "BaseDatos_caras/_ListaAlumnos.csv"
    archivo_temporal = "BaseDatos_caras/000temp_ListaAlumnos.csv"
    
    with open(archivo_original, 'rb') as source:# Copiamos el archivo de forma pythonica
        with open(archivo_temporal, 'wb') as target:
            target.write(source.read())
    # Intentamos abrirlo con Excel
    try:
        subprocess.run(["start", "excel", archivo_temporal], check=True, shell=True)
    except subprocess.CalledProcessError:
        os.system(f"notepad {archivo_temporal}")# Si no se pudo abrir con Excel, lo abrimos como un .txt que ahuevo debe tener notepad como minimo
    # Recuerda, este código mamalón asume que tienes Excel instalado. 
    # Si no lo tienes, irá directo a Notepad.
##end de abrir_Lista

def Abrir_Asistencias_CSV():
    archivo_original = "BaseDatos_caras/_Asistencias.csv.csv"
    archivo_temporal = "BaseDatos_caras/000temp_Asistencias.csv"
    
    with open(archivo_original, 'rb') as source:# Copiamos el archivo de forma pythonica
        with open(archivo_temporal, 'wb') as target:
            target.write(source.read())
    # Intentamos abrirlo con Excel
    try:
        subprocess.run(["start", "excel", archivo_temporal], check=True, shell=True)
    except subprocess.CalledProcessError:
        os.system(f"notepad {archivo_temporal}")# Si no se pudo abrir con Excel, lo abrimos como un .txt que ahuevo debe tener notepad como minimo
    # Recuerda, este código mamalón asume que tienes Excel instalado. 
    # Si no lo tienes, irá directo a Notepad.
##end de abrir_Lista

def Abrir_Asistencias_CSV():
    archivo_original = "BaseDatos_caras/_Asistencias.csv"
    archivo_temporal = "BaseDatos_caras/000temp_Asistencias.csv"
    
    with open(archivo_original, 'rb') as source:# Copiamos el archivo de forma pythonica
        with open(archivo_temporal, 'wb') as target:
            target.write(source.read())
    # Intentamos abrirlo con Excel
    try:
        subprocess.run(["start", "excel", archivo_temporal], check=True, shell=True)
    except subprocess.CalledProcessError:
        os.system(f"notepad {archivo_temporal}")# Si no se pudo abrir con Excel, lo abrimos como un .txt que ahuevo debe tener notepad como minimo
    # Recuerda, este código mamalón asume que tienes Excel instalado. 
    # Si no lo tienes, irá directo a Notepad.
##end de abrir_Lista


def Abrir_Logs_CSV():
    archivo_original = "BaseDatos_caras/_Logs.csv"
    archivo_temporal = "BaseDatos_caras/000temp_Logs.csv"
    
    with open(archivo_original, 'rb') as source:# Copiamos el archivo de forma pythonica
        with open(archivo_temporal, 'wb') as target:
            target.write(source.read())
    # Intentamos abrirlo con Excel
    try:
        subprocess.run(["start", "excel", archivo_temporal], check=True, shell=True)
    except subprocess.CalledProcessError:
        os.system(f"notepad {archivo_temporal}")# Si no se pudo abrir con Excel, lo abrimos como un .txt que ahuevo debe tener notepad como minimo
    # Recuerda, este código mamalón asume que tienes Excel instalado. 
    # Si no lo tienes, irá directo a Notepad.
##end de abrir_Lista





class Aplicacion:


    def __init__(self):
        ## Configura el inicio de la ventana
        ventana = tk.Tk()
        ventana.title("Present PhotoID By iLabTDI")
        ventana.geometry("750x700")
        ventana.resizable(True, True)
        self.Ventana = ventana # Guarda esto como propiedad

        self.Pagina_cargando() # Página principal carga

        def funcion_hilo():
            # 1) primero carga el registro de caras
            # VIEJO: Camara_Class.Cargar_Registro_Caras(self) # primero carga las caras, le envia el self para que use las funciones
            known_face_encodings, known_vatos_info, known_codigos_info = DataBase_Class.Cara_Carga_Registro(self)

            # 2) ahora carga las camaras:
            self.CamaraObj = Camara_Class.CamaraObj("webcam", 0, self) # carga la webcam, le envia el self para que use las funciones.

            # Los encodings e información carga en el paso 1 ahora la pasa a la camara recien creada previamente para que cada que procese la imagen
            # la tenga en cuenta
            self.CamaraObj.known_face_encodings = known_face_encodings
            self.CamaraObj.known_vatos_info = known_vatos_info
            self.CamaraObj.known_codigos_info = known_codigos_info
            
            
            # 3) ahora pone otra nueva pantalla
            self.Pagina_Inicio() #la pantalla de inicio
        ###
        
        # Crear un hilo y ejecutar la función en ese hilo
        thread = threading.Thread(target=funcion_hilo)
        thread.start()

        def funcion_hilo_2():
            self.Ventana_Add = Add_Alumnos_class.Crear(ventana)
        ###
        # Crear un hilo y ejecutar la función en ese hilo
        thread_2 = threading.Thread(target=funcion_hilo_2)
        thread_2.start()

        ventana.mainloop()# Iniciar el bucle principal
        
        
        
        #await asyncio.sleep(2)
        #self.CamaraObj = Camara_Class.CamaraObj("webcam", 0) 

        #self.Pagina_Registro() # Carga la pagina Registro
        #self.Pagina_Inicio()# Carga la pagina de inicio
        #### función adicional

        
    ## end del init que se ejecuta al creara
    def set_progress_barra(self, percentage):
        self._progress_bar ["value"] = percentage
    #### de set progress_barra

    def set_texto_progress(self,new_value):
        self._texto_progress.configure(text=new_value)
    ####

    def set_num_texto_progress(self,new_value):
        self._num_texto_progress.configure(text=new_value)
    ####

    def  Pagina_cargando(self):
        ventana = self.Ventana

        # Obtener el ancho y alto de la pantalla
        ancho_pantalla = ventana.winfo_screenwidth()
        alto_pantalla = ventana.winfo_screenheight()

        # Calcular las coordenadas x e y para que la ventana esté centrada
        x = (ancho_pantalla - 400) / 2
        y = (alto_pantalla - 200) / 2

        # Establecer la geometría de la ventana
        ventana.geometry(f'400x200+{int(x)}+{int(y)}')

        # Crear un marco para organizar los elementos
        frame_CARGANDO = ttk.Frame(ventana, padding=10)
        frame_CARGANDO.grid(row=0, column=0, padx=50, pady=25)
        ventana._frame_CARGANDO = frame_CARGANDO

        # Crear la barra de carga determinada
        num_texto_progress = ttk.Label(frame_CARGANDO, text="0/n")
        num_texto_progress.grid(row=0, column=0, columnspan=2, pady=1)

        # Crear la barra de carga determinada
        texto_progress = ttk.Label(frame_CARGANDO, text="1/2 Cargando Estudiantes...")
        texto_progress.grid(row=1, column=0, columnspan=2, pady=1)

        progress_bar = ttk.Progressbar(frame_CARGANDO, mode="determinate", length=200)
        progress_bar.grid(row=2, column=0, columnspan=2, pady=10)

        self._num_texto_progress = num_texto_progress
        self._texto_progress = texto_progress
        self._progress_bar = progress_bar


        
        # Entrada para establecer el porcentaje
        #percentage_entry = ttk.Entry(frame)
        #percentage_entry.grid(row=3, column=0, pady=10)

        # Botón para establecer el porcentaje
        #set_percentage_button = ttk.Button(frame, text="Establecer Porcentaje", command=lambda: set_progress_barra(float(percentage_entry.get())))
        #set_percentage_button.grid(row=3, column=1, pady=10)

        return num_texto_progress, texto_progress, progress_bar
    ### end de pagina_cargando (función definida)

    
    def Pagina_Registro(self):
        ventana = self.Ventana
        ###################################### FUNCIONES
        def agregar_imagen():
            ruta_imagen = filedialog.askopenfilename(title="Seleccionar Imagen", filetypes=[("Imágenes", "*.jpg *.png")])
            entrada_ruta.delete(0, tk.END)
            entrada_ruta.insert(0, ruta_imagen)
        ### de función de agragar imagen

        def guardar_registro():
            codigo = entrada_codigo.get()
            nombre = entrada_nombre.get()
            ruta_imagen = entrada_ruta.get()
            # Validar que los campos no estén vacíos
            if codigo and nombre and ruta_imagen:
                with open('registros.csv', mode='a', newline='') as archivo_csv:
                    escritor_csv = csv.writer(archivo_csv)
                    escritor_csv.writerow([codigo, nombre, ruta_imagen])
                    entrada_codigo.delete(0, tk.END)
                    entrada_nombre.delete(0, tk.END)
                    entrada_ruta.delete(0, tk.END)
                    print("Registro guardado correctamente.")
                # end del with open
            else:
                print("Todos los campos son obligatorios.")
            # end del if codigo, nombre and ruta
        # end de guardar registro


        ###################################### PAGINA ESQUELETON
        
        # Etiquetas y campos de entrada
        tk.Label(ventana, text="Código:").grid(row=0, column=0)
        entrada_codigo = tk.Entry(ventana)
        entrada_codigo.grid(row=0, column=1)

        tk.Label(ventana, text="Nombre:").grid(row=1, column=0)
        entrada_nombre = tk.Entry(ventana)
        entrada_nombre.grid(row=1, column=1)

        tk.Label(ventana, text="Ruta Imagen:").grid(row=2, column=0)
        entrada_ruta = tk.Entry(ventana)
        entrada_ruta.grid(row=2, column=1)

        ###################################### BOTONES E INTERACCIÓN
        ttk.Button(ventana, text="Seleccionar Imagen", command=agregar_imagen).grid(row=3, column=0, columnspan=2)
        ttk.Button(ventana, text="Guardar Registro", command=guardar_registro).grid(row=4, column=0, columnspan=2)
    ## Ventana 
    
    
    def on_combobox_select(self, event):
        global camara_seleccionada_num
        combo = event.widget
        index = combo.current()  # obtiene el índice seleccionado
        nombre = combo.get()  # obtiene el nombre seleccionado
        #print(f"Index: {index}, Nombre: {nombre}")
        
        if self.CamaraObj._NumCamera != index:
            self.CamaraObj.selecciona_camara(index)
        else:
            #print("es el mismo numero entonces no vale la pena poner nada.")
            pass
        ##end de el numero del index es diferente 

        self.CamaraObj._NumCamera = index
    ###on_combobox_select

    

    def Pagina_Inicio(self):
        # Crear la ventana principal
        ventana = self.Ventana

        def Lista_de_Alumnos():
            #print("Acción: Lista de Alumnos")
            Abrir_Lista_CSV()
        ###
        def Registro_de_Asistencia():
            #print("Acción: Registro de asistencia")
            Abrir_Asistencias_CSV()
        ###
        def Ver_Logs():
            #print("Acción: Ver Logs")
            Abrir_Logs_CSV()
        ###
        def Anadir_Alumno():
            self.Ventana_Add.Mostrar()
        ### end de cuando añade un alumno
            

        ###de anadir alumno
        def Configuracion():
            print("Acción: Configuracion")
        ###
        ventana._frame_CARGANDO.destroy() # destruye el que es cargando.

        frame_INICIO = ttk.Frame(ventana, padding=10) # lo mete 
        frame_INICIO.grid(row=0, pady=5)
        
        ancho_ventana = 750
        alto_ventana = 700

        ancho_pantalla = ventana.winfo_screenwidth()
        alto_pantalla = ventana.winfo_screenheight()

        centro_x = (ancho_pantalla - ancho_ventana) // 2
        centro_y = (alto_pantalla - alto_ventana) // 2

        ventana.geometry(f'{ancho_ventana}x{alto_ventana}+{centro_x}+{centro_y}')

        # Crear dos Frames: uno para los botones a la izquierda y otro para los botones a la derecha
        frame_informacion = tk.Frame(frame_INICIO)
        frame_informacion.grid(row=0, pady=5) #frame_informacion.pack(pady=5, side=tk.TOP)

        frame_video = tk.Frame(frame_INICIO)
        frame_video.grid(row=1, pady=5)

        frame_opciones = tk.Frame(frame_INICIO)
        frame_opciones.grid(row=2, pady=5)
        
        # Letras de información 
        Label_Salon = tk.Label(frame_informacion, text="Clase: iLabTDI", font=("Helvetica", 20))
        Label_Salon.grid(row=0, column=2, pady=5)
        Label_Hora = tk.Label(frame_informacion, text="Hora: 00:00:00", font=("Helvetica", 12))
        Label_Hora.grid(row=1, column=0, pady=5)

        Label_selector_camara = tk.Label(frame_informacion, text="Cámara:", font=("Helvetica", 12))
        Label_selector_camara.grid(row=1, column=1, pady=5)
        # Crear una lista desplegable
        combo = ttk.Combobox(frame_informacion, values=self.CamaraObj._detected_cameras_name, state='readonly')
        combo.grid(row=1, column=2, pady=5)
        combo.set(self.CamaraObj._detected_cameras_name[0])  # asigna esta por defecto

        # Vinculamos el evento de selección del combobox a una función que imprime el índice y el nombre
        combo.bind("<<ComboboxSelected>>", self.on_combobox_select)
        
        # Creando el checkbox y asignándole la variable
        # configuración de booleanvar
        var_mostrar_camara = tk.BooleanVar(value=True)
        def cambio_estado():
            Camara_Class.Mostrar_video = var_mostrar_camara.get()
        ####  cambio_estado

        checkbox = ttk.Checkbutton(frame_informacion, text='Mostrar Video', variable=var_mostrar_camara, command=cambio_estado)
        checkbox.grid(row=1, column=3, pady=5)


        #Label_Hora = tk.Label(frame_informacion, text="", font=("Helvetica", 12))
        #Label_Hora.grid(row=1, column=1, pady=5)
        

        # Botón para registrar alumnos (Empaquetado a la izquierda)
        btn_listaAlumnos = ttk.Button(frame_opciones, text="👤 Lista de Alumnos", width=20, command=Lista_de_Alumnos)
        btn_ListaAsistencia = ttk.Button(frame_opciones, text="✅ Registro de Asistencia", width=25, command=Registro_de_Asistencia)
        btn_logs = ttk.Button(frame_opciones, text="📋 Ver Logs", width=12,command=Ver_Logs)
        btn_add_alumno = ttk.Button(frame_opciones, text="➕ Añadir Alumno", width=18,command=Anadir_Alumno)
        btn_configuracion = ttk.Button(frame_opciones, text="⚙️ Configuración", width=18,command=Configuracion)
        
        # botones
        btn_listaAlumnos.grid(row=0, column=0, padx=(5, 0), pady=(2, 0), sticky='n')
        btn_ListaAsistencia.grid(row=0, column=1, padx=(5, 0), pady=(2, 0), sticky='n')
        btn_logs.grid(row=0, column=2, padx=(40, 0), pady=(2, 0), sticky='n')
        btn_add_alumno.grid(row=0, column=3, padx=(5, 0), pady=(2, 0), sticky='n')
        btn_configuracion.grid(row=0, column=4, padx=(5, 0), pady=(2, 0), sticky='n')

        
        #Vido que reproduce
        label = tk.Label(frame_video)
        label.pack(pady=10)

        

        def actualizar_frame():
            # se conecta con la cámara:
            # actualiza la pantalla que ve
            Camara = self.CamaraObj
            ret, frame_original = Camara.Tomar_Captura()
            if ret: #si cargó la imagen correctamente:

                frame_procesado = Camara_Class.Procesar_Frame_update(Camara, frame_original )

                # ahora lo pone en el label
                if Camara_Class.Mostrar_video:
                    imagen_tk = ImageTk.PhotoImage(Image.fromarray(frame_procesado))
                else:
                    imagen_blanca = np.zeros((2, 1, 3), dtype=np.uint8)
                    imagen_tk = ImageTk.PhotoImage(image=Image.fromarray(imagen_blanca))
                #### mostrar video

                label.config(image=imagen_tk)
                label.image = imagen_tk
            else:
                # revisa el numero de camaras.
                print(f"La cámara {self.CamaraObj._NumCamera} se desconectó o hubo un error.")



            ## si es valido el ret (no hay error)

            # actualiza la hora
            hora_actual = obtener_hora_actual()
            Label_Hora.config(text=f"{hora_actual}")
            #print(obtener_hora_actual())

            if ventana.winfo_height() < frame_INICIO.winfo_height() or ventana.winfo_width() < frame_INICIO.winfo_width() :
                ventana.geometry(f"{frame_INICIO.winfo_width()}x{frame_INICIO.winfo_height()}")
            #### si es menor para que no anden chingando

            ventana.after(10, actualizar_frame)
        ### actualizar frame

        actualizar_frame()# este actualiza el frame de la imagen para que la actualicé dentro de la app
        #ventana.mainloop()# Iniciar el bucle principal
        



    ### Pagina de Inicio
## class 
