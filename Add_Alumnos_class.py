import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
import cv2
import os
import numpy as np
from PIL import Image, ImageTk
import face_recognition
from unidecode import unidecode


import DataBase_Class





## Textos defaults:
Codigoperfil_default_txt = "Código: --------"
nombreperfil_default_txt = "Nombre: -----"
Apellido_Paterno_perfil_default_txt = "Apellido Paterno: -----"
Apellido_Materno_perfil_default_txt = "Apellido Materno: -----"





def es_numero(P):
    if P == "":
        return True
    try:
        float(P)
        return True
    except ValueError:
        return False
    ####
#### end de si es número


def dividir_por_espacios(texto):
    palabras = texto.split()
    return palabras
#### end de dividir por espacios

def validar_nombre(P):
    # Personaliza tu validación aquí
    for char in P:
        if not (char.isalpha() or char.isspace()):
            return False
        else:
            nombre_separado = dividir_por_espacios(P)
            num_names = len(nombre_separado)
            if num_names>4:
                return False
            ####
        #####
    
    contador = 0
    for char in P:
        if char.isspace():
            contador += 1
        ####
    ####

    if contador >3:
        return False
    ####
    return True
##### end validar_nombre

def limpiar_string(texto):
    return unidecode(texto)


class Crear:



    def fx_evaluacion_guardar(self):
        if self.Bool_add_Nombre.get() and self.Bool_add_Codigo.get() and self.Bool_add_Imagen.get():
            self.btnguardar_registro.configure(state="normal")
        else:
            self.btnguardar_registro.configure(state="disabled")
        ###
    ####
    

    def fx_bool_nombre(self, *args):
        self.fx_evaluacion_guardar()
    ###
    def fx_bool_codigo(self, *args):
        self.fx_evaluacion_guardar()
    ###
    def fx_bool_imagen(self, *args):
        self.fx_evaluacion_guardar()
    ###

    def copiar_nombre(self, *args):
        contenido = self.nombre_alumno_str.get()
        if contenido:
            nombre_separado = dividir_por_espacios(contenido)
            num_names = len(nombre_separado)

            if num_names == 1 or num_names == 2:
                self.Nombre_perfil.config(text="Nombre: "+ contenido )
                self.ApellidoPaterno_perfil.config(text= Apellido_Paterno_perfil_default_txt)
                self.ApellidoMaterno_perfil.config(text=Apellido_Materno_perfil_default_txt)
                self.Bool_add_Nombre.set(False)
            elif num_names == 3:
                self.Nombre_perfil.config(text="Nombre: "+ nombre_separado[0] )
                self.ApellidoPaterno_perfil.config(text="Apellido Paterno: "+ nombre_separado[1])
                self.ApellidoMaterno_perfil.config(text="Apellido Materno: "+ nombre_separado[2])
                self.Bool_add_Nombre.set(True)
            elif num_names == 4:
                self.Nombre_perfil.config(text="Nombre: "+ nombre_separado[0]+ " "+ nombre_separado[1] )
                self.ApellidoPaterno_perfil.config(text="Apellido Paterno: "+ nombre_separado[2])
                self.ApellidoMaterno_perfil.config(text="Apellido Materno: "+ nombre_separado[3])
                self.Bool_add_Nombre.set(True)
                #### en del num_names                
            else:
                self.Nombre_perfil.config(text=nombreperfil_default_txt)
                self.ApellidoPaterno_perfil.config(text= Apellido_Paterno_perfil_default_txt)
                self.ApellidoMaterno_perfil.config(text= Apellido_Materno_perfil_default_txt)
                self.Bool_add_Nombre.set(False)
            ####
        ####
    ### end de copiar nombres


    

    def copiar_codigo(self, *args):
        contenido = self.codigo_alumno_int.get()
        if contenido:
            self.Codigo_perfil.config(text="Código: "+ contenido)
            self.Bool_add_Codigo.set(True)
        else:
            self.Codigo_perfil.config(text=Codigoperfil_default_txt)
            self.Bool_add_Codigo.set(False)
        ####
    #### end de 


    def guardar_registro(self):
        # ahora guarda la imagen que seleccionó

        # ahora guarda pero primero valida que todo esté bien
        if self.Bool_add_Nombre.get() and self.Bool_add_Codigo.get() and self.Bool_add_Imagen.get():
            
            e_student_code = limpiar_string( self.codigo_alumno_int.get() ) 
            e_student_name = limpiar_string( self.nombre_alumno_str.get() )
            e_imagen = self.imagen_global
                
            guardado_exitoso = DataBase_Class.Guardar_nuevo_alumno( e_student_code, e_student_name, e_imagen)

            if guardado_exitoso == True: # si lo pudo guardar exitosamente entonces lo que hace es borrar los campos y todo eso.
                # BORRA todo lo que está en los campos esos de ingresar texto a lo wey:
                self.entrada_nombre.delete(0, tk.END)
                self.entrada_codigo.delete(0, tk.END)
                self.entrada_ruta.configure(state="normal")
                self.entrada_ruta.delete(0, tk.END)
                self.entrada_ruta.configure(state="disabled")
                # quita las imagenes
                self.Anuncio_derecha.config(text="[Selecciona una imagen]")
                self.labelimg.config(image=None)
                self.labelimg.image = None  

                # del texto de la derecha:
                self.Codigo_perfil.config(text=Codigoperfil_default_txt)
                self.Nombre_perfil.config(text=nombreperfil_default_txt)
                self.ApellidoPaterno_perfil.config(text= Apellido_Paterno_perfil_default_txt)
                self.ApellidoMaterno_perfil.config(text= Apellido_Materno_perfil_default_txt)

                # esto ocurre al final casi para reajustar el tamaño de la imagen
                self.Auto_adjust_Geometry_de_esta_ventana()
            ## guardado exitoso
        ### del bool nombre and codigo and imagen
        
        
    # end de guardar registro

    def agregar_imagen(self):
        # carga las variables del self object
        seleccion_img = self.seleccion_img
        entrada_ruta = self.entrada_ruta


        seleccion_img.configure(state = "disabled")
        ruta_imagen = filedialog.askopenfilename(title="Seleccionar Imagen", filetypes=[("Imágenes", "*.jpg *.png")])
        seleccion_img.configure(state = "normal")

        self.Bool_add_Imagen.set(False)
                
        entrada_ruta.configure(state="normal")
        entrada_ruta.delete(0, tk.END)
        entrada_ruta.insert(0, ruta_imagen)
        entrada_ruta.icursor(tk.END)  
        entrada_ruta.configure(state="disabled")
        
        if ruta_imagen == "":
            # quita las imagenes
            self.Anuncio_derecha.config(text="[Selecciona una imagen]")
            self.labelimg.config(image=None)
            self.labelimg.image = None  

            # esto ocurre al final casi para reajustar el tamaño de la imagen
            self.Auto_adjust_Geometry_de_esta_ventana() # REAJUSTA TAMAÑO

            return "la imagen no es valida"
        ###

        # ahora carga la imagen 
        frame_original = cv2.imread(ruta_imagen)
        frame_original_editado = frame_original
        alto, ancho, canales = frame_original_editado.shape

        # Se pone un cuadro de imagen
        face_locations = face_recognition.face_locations(frame_original_editado)
        num_caras = len(face_locations)
        if num_caras == 0:
            self.Anuncio_derecha.config(text="Imagen Inválida ❌ No se detectó ningún rostro")
        elif num_caras > 1: #si es el caso de que hay mas de 2 caras en la camara
            self.Anuncio_derecha.config(text="Imagen Inválida ❌ Hay más de una cara")
        elif num_caras == 1: # caso CORRECTO donde solo hay una
            self.Anuncio_derecha.config(text="Imagen válida ✔️")
            face_location_1 = face_locations[0]

            self.imagen_global = np.copy(frame_original_editado) # crea esta copia para el guardado de la imagen sin el rectangulo verde de abajo
            
            # Obtiene 
            x1, y1, x2, y2 = face_location_1[3], face_location_1[0], face_location_1[1], face_location_1[2]
            
            

            color = (125, 220, 0) # color verdecilloframe_original
            cv2.rectangle(frame_original_editado, (x1, y1), (x2, y2), color, 8)
            #hace crop
            x1_crop = max(0, x1 - 200 ) 
            y1_crop = max(0, y1 - 200 ) 
            x2_crop = min(ancho, x2 + 200 )
            y2_crop = min(alto, y2 + 200 )
            frame_original_editado = frame_original_editado[y1_crop:y2_crop, x1_crop:x2_crop]
            
            
            #self.imagen_global = self.imagen_global[y1:y2, x1:x2] #hace el crop sin los pixeles alrededor extras ni el rectangulo verdoso
            self.imagen_global = self.imagen_global[y1_crop:y2_crop, x1_crop:x2_crop]


            self.Bool_add_Imagen.set(True)
        ### num caras > 0
        
        # Calcula la nueva altura manteniendo el mismo aspect ratio
        alto, ancho, canales = frame_original_editado.shape #los toma de nuevo 
        nueva_alto = min(alto, 300)
        nueva_ancho = int((nueva_alto / alto) * ancho)
        
        frame_original_editado = cv2.cvtColor(frame_original_editado, cv2.COLOR_BGR2RGB)
        frame_original_editado = cv2.resize(frame_original_editado, (   round(nueva_ancho)  , round(nueva_alto)))# lo regresa a su resolución original por si se redujo para acelerar el procesamiento
        
        imagen_tk = ImageTk.PhotoImage(Image.fromarray(frame_original_editado))
        
        self.labelimg.config(image=imagen_tk)
        self.labelimg.image = imagen_tk  # Esto es importante para evitar que Python "limpie" la imagen
        
        # esto ocurre al final casi para reajustar el tamaño de la imagen
        self.Auto_adjust_Geometry_de_esta_ventana() # REAJUSTA TAMAÑO
    #####



    def __init__(self, Ventana):

        # 1 establece los strings
        # ahora crea las variables que estára utilizando
        self.codigo_alumno_int = tk.StringVar()
        self.codigo_alumno_int.trace("w", self.copiar_codigo)
        self.nombre_alumno_str = tk.StringVar()
        self.nombre_alumno_str.trace("w", self.copiar_nombre)

        self.imagen_global = None
        self.Visible = False

        # 2 Banderas para validar que todo esté bien y ya pueda darle a guardar:
        self.Bool_add_Nombre = tk.BooleanVar()
        self.Bool_add_Codigo = tk.BooleanVar()
        self.Bool_add_Imagen = tk.BooleanVar()


        # 3 crea la estructura
        self.__crea_estructura__(Ventana)# manda a crear la estructura de la ventana.

        # 3 eventos listerners para cada bool:
        self.Bool_add_Nombre.trace("w", self.fx_bool_nombre)
        self.Bool_add_Codigo.trace("w", self.fx_bool_codigo)
        self.Bool_add_Imagen.trace("w", self.fx_bool_imagen)
        

        self.Auto_adjust_Geometry_de_esta_ventana()
    #### end del init




    # esta función la usa la función de init para crear la estructura
    def __crea_estructura__(self, Ventana):
        ## Configura el inicio de la ventana. Ventana principal
        ventana_confirmacion = tk.Toplevel(Ventana)
        ventana_confirmacion.title("Añadir Alumno")
        ventana_confirmacion.geometry("350x200")
        ventana_confirmacion.withdraw()  # Oculta la ventana de mientras hasta que el user quiera añadir a un buey
        
        self.ventana_confirmacion = ventana_confirmacion

        ventana_confirmacion.protocol("WM_DELETE_WINDOW", self.on_closing)  # Cambia el comportamiento del botón de cerrar

        ##########################
        ### Primero genera toda  la estructura y ya después son las acciones y todas esas cosas.
        ##########################

        # Frame lado izquierdo (Donde van los datos)
        izquierda = tk.Frame(ventana_confirmacion)
        izquierda.pack(pady=5, side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Frame lado Derecho (donde va la imagen y la confirmación de la imagen)
        derecha = tk.Frame(ventana_confirmacion)
        derecha.pack(pady=5, side=tk.RIGHT, fill=tk.BOTH, expand=True)

        # Frame Abajo (Donde va la confrimación para enviar los datos del usuario).
        abajo = tk.Frame(ventana_confirmacion)
        #abajo.pack(pady=5, side=tk.RIGHT, fill=tk.BOTH, expand=True)
        

        ### Acá empieza a colocar las cosas del lado IZQUIERDO que necesita compeltar quien ande viendo esto:

        # Label: Código.
        tk.Label(izquierda, text="Código:").grid(row=0, column=0)
        # Entry: Código.
        validacion_code = ventana_confirmacion.register(es_numero)# regsitra que validará
        entrada_codigo = ttk.Entry(izquierda, width=30, validate="key", validatecommand=(validacion_code, "%P"), textvariable=self.codigo_alumno_int)
        entrada_codigo.grid(row=0, column=1)

        # Label Nombre del alumno.
        tk.Label(izquierda, text="Nombre:").grid(row=1, column=0)
        # Entry Nombre del alumno.
        validacion_nombre = ventana_confirmacion.register(validar_nombre)
        entrada_nombre = ttk.Entry(izquierda, width=30, textvariable=self.nombre_alumno_str, validate="key", validatecommand=(validacion_nombre, "%P"))
        entrada_nombre.grid(row=1, column=1)

        # Label Ruta de imagen.
        tk.Label(izquierda, text="Ruta Imagen:").grid(row=2, column=0)
        # Entry Ruta de imagen.
        entrada_ruta = ttk.Entry(izquierda, width=30)
        entrada_ruta.grid(row=2, column=1)
        entrada_ruta.configure(state="disabled")

        # Boton para seleccionar imagen.
        seleccion_img = ttk.Button(izquierda, text="Seleccionar Imagen", command=self.agregar_imagen)
        seleccion_img.grid(row=3, column=0, columnspan=2, pady=20)

        ### Acá empieza a colocar las cosas del lado DERECHO donde se muestra la imagen del wey y también confirmar que ya puede enviar las madres que rellenó.

        # Label Anuncio de arriba del estado de la imagen
        Anuncio_derecha = tk.Label(derecha, text="[Selecciona una imagen]")
        Anuncio_derecha.grid(row=1, column=0, pady=(5, 0), columnspan=2, sticky='n')  
        
        #Boton para guardar imagen.
        btnguardar_registro = ttk.Button(derecha, text="Guardar Registro", command=self.guardar_registro)
        btnguardar_registro.grid(row=7, column=0, columnspan=2, pady=10)
        btnguardar_registro.configure(state="disabled")
        

        # Aca procesa la imagen para crear el IMage Label
        
        # Image Label de arriba.
        frame_original = cv2.imread("ImagesSrc/nophotoholder.png")
        alto, ancho, canales = frame_original.shape
        # Calcula la nueva altura manteniendo el mismo aspect ratio:
        nueva_alto = min(alto, 200)
        nueva_ancho = int((nueva_alto / alto) * ancho)

        frame_original = cv2.cvtColor(frame_original, cv2.COLOR_BGR2RGB)
        frame_original = cv2.resize(frame_original, (   round(nueva_ancho)  , round(nueva_alto)))# lo regresa a su resolución original por si se redujo para acelerar el procesamiento
        imagen_tk = ImageTk.PhotoImage(Image.fromarray(frame_original))
        labelimg = tk.Label(derecha, image = imagen_tk)
        labelimg.grid(row=2, column=0, columnspan=2, pady=(0, 5))

        # Label código de Alumnos:
        Codigo_perfil = tk.Label(derecha, text=Codigoperfil_default_txt)
        Codigo_perfil.grid(row=3, column=0, pady=(5, 0), sticky='w')  
        # Label nombre del alumno
        Nombre_perfil = tk.Label(derecha, text=nombreperfil_default_txt )
        Nombre_perfil.grid(row=4, column=0, pady=(5, 0), sticky='w') 
        # Label de apellido paterno
        ApellidoPaterno_perfil = tk.Label(derecha, text=Apellido_Paterno_perfil_default_txt)
        ApellidoPaterno_perfil.grid(row=5, column=0, pady=(5, 0), sticky='w')  
        # Label de apellido materno
        ApellidoMaterno_perfil = tk.Label(derecha, text=Apellido_Materno_perfil_default_txt)
        ApellidoMaterno_perfil.grid(row=6, column=0, pady=(5, 0), sticky='w')


        # aca lo guarda en el objeto self
        self.btnguardar_registro = btnguardar_registro # lo guarda como self
        
        self.seleccion_img = seleccion_img
        self.entrada_codigo = entrada_codigo
        self.entrada_nombre = entrada_nombre
        self.entrada_ruta = entrada_ruta
        self.labelimg = labelimg

        self.Anuncio_derecha = Anuncio_derecha

        self.Codigo_perfil = Codigo_perfil
        self.Nombre_perfil = Nombre_perfil
        self.ApellidoPaterno_perfil = ApellidoPaterno_perfil
        self.ApellidoMaterno_perfil = ApellidoMaterno_perfil

    ###



    def Mostrar(self):
        # Hace visible la ventana
        
        self.ventana_confirmacion.deiconify()
        self.ventana_confirmacion.grab_set()  # Hace que la ventana sea modal
        self.Visible = True
    ### end de cuando se hace visible esta ventana


    def Ocultar(self):
        
        self.ventana_confirmacion.grab_release()  # Libera la ventana para que ya no sea modal
        self.ventana_confirmacion.withdraw()
        self.Visible = False
    ### end de cuando se hace visible esta ventana
    
    def on_closing(self):
        
        self.ventana_confirmacion.grab_release()  # Libera la ventana para que ya no sea modal
        self.ventana_confirmacion.withdraw()  # Oculta la ventana en lugar de destruirla
        self.Visible = False
    ### de cuando se da click a cerrar esta madre



    # Funcion para autoajustar el tamaño de la ventana y hacer que esta ventana.
    def Auto_adjust_Geometry_de_esta_ventana(self):
        # esto ocurre al final casi para reajustar el tamaño de la imagen
        ventana_confirmacion = self.ventana_confirmacion

        ventana_confirmacion.update_idletasks()  # Asegura que los widgets se han creado y configurado
        ancho_requerido = ventana_confirmacion.winfo_reqwidth()  # Obtiene el ancho requerido
        alto_requerido = ventana_confirmacion.winfo_reqheight()  # Obtiene el ancho requerido
        ventana_confirmacion.geometry(f"{ancho_requerido}x"f"{alto_requerido}"  )  # Establece el ancho de la ventana### 

    ### Auto_adjust_Geometry_de_esta_ventana

# END DE CLASS DE ADD_Alumno
