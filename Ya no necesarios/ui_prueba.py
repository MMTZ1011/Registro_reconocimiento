import cv2
import tkinter as tk
from tkinter import filedialog
import csv
from PIL import Image, ImageTk





class Aplicacion:
    def __init__(self):

        ## Configura el inicio de la ventana
        ventana = tk.Tk()
        ventana.title("Present PhotoID By iLabTDI")
        ventana.geometry("750x540")
        ventana.resizable(False, False)
        self.Ventana = ventana # Guarda esto como propiedad

        self.Pagina_Registro() # Carga la pagina Registro

        #self.Pagina_Inicio()# Carga la pagina de inicio
        
        ventana.mainloop()# Iniciar el bucle principal
    ## end init


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
        tk.Button(ventana, text="Seleccionar Imagen", command=agregar_imagen).grid(row=3, column=0, columnspan=2)
        tk.Button(ventana, text="Guardar Registro", command=guardar_registro).grid(row=4, column=0, columnspan=2)

    ## Ventana 


    def Pagina_Inicio(self):
        # Crear la ventana principal
        ventana = self.Ventana

        def registrar_alumnos():
            print("Acción: Registrar alumnos")
        ###

        def configuracion():
            print("Acción: Configuración")
        ###

        def ver_camara():
            print("Acción: Ver cámara")
        ###
        

        # Crear dos Frames: uno para los botones a la izquierda y otro para los botones a la derecha
        frame_informacion = tk.Frame(ventana)
        frame_informacion.pack(pady=5, side=tk.TOP)
        frame_video = tk.Frame(ventana)
        frame_video.pack(pady=5, side=tk.TOP)
        frame_opciones = tk.Frame(ventana)
        frame_opciones.pack(pady=5, side=tk.TOP)

        
        # Letras de información 
        Label_Salon = tk.Label(frame_informacion, text="Clase: iLabTDI", font=("Helvetica", 20))
        Label_Salon.pack()
        Label_Hora = tk.Label(frame_informacion, text="Hora: 16:30:00", font=("Helvetica", 12))
        Label_Hora.pack()


        # Botón para registrar alumnos (Empaquetado a la izquierda)
        btn_listaAlumnos = tk.Button(frame_opciones, text="👤 Lista de Alumnos", width=15, command=registrar_alumnos)
        btn_ListaAsistencia = tk.Button(frame_opciones, text="✅ Registro de Asistencia", width=20, command=configuracion)
        btn_logs = tk.Button(frame_opciones, text="📋 Ver Logs", width=10,command=ver_camara)
        btn_add_alumno = tk.Button(frame_opciones, text="➕ Añadir Alumno", width=15,command=ver_camara)
        btn_configuracion = tk.Button(frame_opciones, text="⚙️ Configuración", width=15,command=ver_camara)
        
        # botones
        btn_listaAlumnos.pack(side=tk.LEFT, padx=(5, 0), pady=(2,0),anchor='n')
        btn_ListaAsistencia.pack(side=tk.LEFT, padx=(5, 0), pady=(2,0),anchor='n')
        btn_logs.pack(side=tk.LEFT, padx=(40, 0), pady=(2,0),anchor='n')
        btn_add_alumno.pack(side=tk.LEFT, padx=(5, 0), pady=(2,0),anchor='n')
        btn_configuracion.pack(side=tk.LEFT, padx=(5, 0), pady=(2,0),anchor='n')


        # Imagen (Empaquetada a la derecha)
        imagen_pil = Image.open("Images/prueba_2.png")
        imagen_pil = imagen_pil.resize((640, 360), Image.LANCZOS)
        imagen_tk = ImageTk.PhotoImage(imagen_pil)
        label = tk.Label(frame_video, image=imagen_tk)
        label.pack(pady=10)

        src=  "/Images/prueba.png"

        ventana.mainloop()# Iniciar el bucle principal
    ### Pagina de Inicio
## class 




App_Obj = Aplicacion()