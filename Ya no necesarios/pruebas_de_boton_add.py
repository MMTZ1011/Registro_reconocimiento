import tkinter as tk
from tkinter import filedialog
import csv
import os
import cv2
import numpy as np
import face_recognition
from PIL import Image, ImageTk



Codigoperfil_default_txt = "Código: --------"
nombreperfil_default_txt = "Nombre: -----"
Apellido_Paterno_perfil_default_txt = "Apellido Paterno: -----"
Apellido_Materno_perfil_default_txt = "Apellido Materno: -----"


imagen_global = None



def es_numero(P):
    if P == "":
        return True
    try:
        float(P)
        return True
    except ValueError:
        return False
    ####
####


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
#####










def mostrar_ventana_confirmacion():


    ventana_confirmacion = tk.Toplevel(root)
    ventana_confirmacion.title("Añadir Alumno")
    ventana_confirmacion.geometry("350x200")

    def fx_evaluacion_guardar():
        if Bool_add_Nombre.get() and Bool_add_Codigo.get() and Bool_add_Imagen.get():
            btnguardar_registro.configure(state="normal")
        else:
            btnguardar_registro.configure(state="disabled")
        ###
    ####

    Bool_add_Nombre = tk.BooleanVar()
    def fx_bool_nombre(*args):
        fx_evaluacion_guardar()
    ###
    Bool_add_Nombre.trace("w", fx_bool_nombre)

    Bool_add_Codigo = tk.BooleanVar()
    def fx_bool_codigo(*args):
        fx_evaluacion_guardar()
    Bool_add_Codigo.trace("w", fx_bool_codigo)

    Bool_add_Imagen = tk.BooleanVar()
    def fx_bool_imagen(*args):
        fx_evaluacion_guardar()
    Bool_add_Imagen.trace("w", fx_bool_imagen)




    def agregar_imagen():
        global imagen_global

        seleccion_img.configure(state = "disabled")
        ruta_imagen = filedialog.askopenfilename(title="Seleccionar Imagen", filetypes=[("Imágenes", "*.jpg *.png")])
        seleccion_img.configure(state = "normal")

        Bool_add_Imagen.set(False)
                
        entrada_ruta.configure(state="normal")
        entrada_ruta.delete(0, tk.END)
        entrada_ruta.insert(0, ruta_imagen)
        entrada_ruta.icursor(tk.END)  
        entrada_ruta.configure(state="disabled")
        
        if ruta_imagen == "":
            # quita las imagenes
            Anuncio_derecha.config(text="[Selecciona una imagen]")
            labelimg.config(image=None)
            labelimg.image = None  

             # esto ocurre al final casi para reajustar el tamaño de la imagen
            ventana_confirmacion.update_idletasks()  # Asegura que los widgets se han creado y configurado
            ancho_requerido = ventana_confirmacion.winfo_reqwidth()  # Obtiene el ancho requerido
            alto_requerido = ventana_confirmacion.winfo_reqheight()  # Obtiene el ancho requerido
            ventana_confirmacion.geometry(f"{ancho_requerido}x"f"{alto_requerido}"  )  # Establece el ancho de la ventana


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
            Anuncio_derecha.config(text="Imagen Inválida ❌ No se detectó ningún rostro")
        elif num_caras > 1: #si es el caso de que hay mas de 2 caras en la camara
            Anuncio_derecha.config(text="Imagen Inválida ❌ Hay más de una cara")
        elif num_caras == 1: # caso correcto donde solo hay una
            Anuncio_derecha.config(text="Imagen válida ✔️")
            face_location_1 = face_locations[0]

            imagen_global = np.copy(frame_original_editado) # crea esta copia para el guardado de la imagen sin el rectangulo verde de abajo
            

            x1, y1, x2, y2 = face_location_1[3], face_location_1[0], face_location_1[1], face_location_1[2]
            color = (125, 220, 0) # color verdecilloframe_original
            cv2.rectangle(frame_original_editado, (x1, y1), (x2, y2), color, 8)

            x1_crop = max(0, x1 - 200 ) 
            y1_crop = max(0, y1 - 200 ) 
            x2_crop = min(ancho, x2 + 200 )
            y2_crop = min(alto, y2 + 200 )
            frame_original_editado = frame_original_editado[y1_crop:y2_crop, x1_crop:x2_crop]
            
            imagen_global = imagen_global[y1:y2, x1:x2] #hace el crop sin los pixeles alrededor extras
            
            Bool_add_Imagen.set(True)
        ### num caras > 0
        
        # Calcula la nueva altura manteniendo el mismo aspect ratio
        alto, ancho, canales = frame_original_editado.shape #los toma de nuevo 
        nueva_alto = min(alto, 300)
        nueva_ancho = int((nueva_alto / alto) * ancho)
        
        frame_original_editado = cv2.cvtColor(frame_original_editado, cv2.COLOR_BGR2RGB)
        frame_original_editado = cv2.resize(frame_original_editado, (   round(nueva_ancho)  , round(nueva_alto)))# lo regresa a su resolución original por si se redujo para acelerar el procesamiento
        
        imagen_tk = ImageTk.PhotoImage(Image.fromarray(frame_original_editado))
        
        labelimg.config(image=imagen_tk)
        labelimg.image = imagen_tk  # Esto es importante para evitar que Python "limpie" la imagen
        
        # esto ocurre al final casi para reajustar el tamaño de la imagen
        ventana_confirmacion.update_idletasks()  # Asegura que los widgets se han creado y configurado
        ancho_requerido = ventana_confirmacion.winfo_reqwidth()  # Obtiene el ancho requerido
        alto_requerido = ventana_confirmacion.winfo_reqheight()  # Obtiene el ancho requerido
        ventana_confirmacion.geometry(f"{ancho_requerido}x"f"{alto_requerido}"  )  # Establece el ancho de la ventana

        

    ### de función de agragar imagen

    def guardar_registro():
        # ahora guarda la imagen que seleccionó
        nombre_carpeta = "BaseDatos_caras"

        ruta_carpeta = os.path.join(os.getcwd(), nombre_carpeta) # Obtiene la ruta completa de la carpeta
        if not os.path.exists(ruta_carpeta): # Verifica si la carpeta existe
            os.makedirs(ruta_carpeta) # Si no existe, la crea
        ####
        ruta_guardado = nombre_carpeta + '/' + str(codigo_alumno_int.get()) + ".jpg"  # Reemplaza 'ruta_de_tu_carpeta' con la ruta de tu carpeta
        cv2.imwrite(ruta_guardado, imagen_global) # guarda la imagen


        

        # ahora guarda pero primero valida que todo esté bien
        if Bool_add_Nombre and Bool_add_Codigo and Bool_add_Imagen:

            #divide el nombre por nombres y apellidos materno y paterno:
            contenido = nombre_alumno_str.get()
            nombre_separado = dividir_por_espacios(contenido)
            num_names = len(nombre_separado)
            if num_names == 3: # caso valido
                name_0 = nombre_separado[0]
                name_1 = ""
                lastname_dad = nombre_separado[1]
                lastname_mom = nombre_separado[2]
            elif num_names == 4: #caso valido
                name_0 = nombre_separado[0]
                name_1 = nombre_separado[1]
                lastname_dad = nombre_separado[2]
                lastname_mom = nombre_separado[3]
            #####
            student_code = codigo_alumno_int.get()

            with open(nombre_carpeta + '/_Registros.csv', mode= 'a', newline='') as archivo_csv:
                escritor_csv = csv.writer(archivo_csv)
                escritor_csv.writerow([student_code, name_0, name_1, lastname_dad, lastname_mom])
                
                # borra los que estaban en los campos:
                entrada_nombre.delete(0, tk.END)
                entrada_codigo.delete(0, tk.END)
                entrada_ruta.configure(state="normal")
                entrada_ruta.delete(0, tk.END)
                entrada_ruta.configure(state="disabled")
                # quita las imagenes
                Anuncio_derecha.config(text="[Selecciona una imagen]")
                labelimg.config(image=None)
                labelimg.image = None  

                # esto ocurre al final casi para reajustar el tamaño de la imagen
                ventana_confirmacion.update_idletasks()  # Asegura que los widgets se han creado y configurado
                ancho_requerido = ventana_confirmacion.winfo_reqwidth()  # Obtiene el ancho requerido
                alto_requerido = ventana_confirmacion.winfo_reqheight()  # Obtiene el ancho requerido
                ventana_confirmacion.geometry(f"{ancho_requerido}x"f"{alto_requerido}"  )  # Establece el ancho de la ventana
                


                print("Registro guardado exitosamente")



        #### de si tiene las condicioones para todo eso:
        
    # end de guardar registro


    izquierda = tk.Frame(ventana_confirmacion)
    izquierda.pack(pady=5, side=tk.LEFT, fill=tk.BOTH, expand=True)

    derecha = tk.Frame(ventana_confirmacion)
    derecha.pack(pady=5, side=tk.RIGHT, fill=tk.BOTH, expand=True)


    abajo = tk.Frame(ventana_confirmacion)
    

    tk.Label(izquierda, text="Código:").grid(row=0, column=0)
    validacion = ventana_confirmacion.register(es_numero)
    codigo_alumno_int = tk.StringVar()
    def copiar_codigo(*args):
        contenido = codigo_alumno_int.get()
        if contenido:
            Codigo_perfil.config(text="Código: "+ contenido)
            Bool_add_Codigo.set(True)
        else:
            Codigo_perfil.config(text=Codigoperfil_default_txt)
            Bool_add_Codigo.set(False)
        ####
    ####
    codigo_alumno_int.trace("w", copiar_codigo)
    entrada_codigo = tk.Entry(izquierda, width=30, validate="key", validatecommand=(validacion, "%P"), textvariable=codigo_alumno_int)
    entrada_codigo.grid(row=0, column=1)




    nombre_alumno_str = tk.StringVar()
    def copiar_nombre(*args):
        contenido = nombre_alumno_str.get()
        if contenido:
           nombre_separado = dividir_por_espacios(contenido)
           num_names = len(nombre_separado)

           if num_names == 1 or num_names == 2:
               Nombre_perfil.config(text="Nombre: "+ contenido )
               ApellidoPaterno_perfil.config(text= Apellido_Paterno_perfil_default_txt)
               ApellidoMaterno_perfil.config(text=Apellido_Materno_perfil_default_txt)
               Bool_add_Nombre.set(False)
           elif num_names == 3:
               Nombre_perfil.config(text="Nombre: "+ nombre_separado[0] )
               ApellidoPaterno_perfil.config(text="Apellido Paterno: "+ nombre_separado[1])
               ApellidoMaterno_perfil.config(text="Apellido Materno: "+ nombre_separado[2])
               Bool_add_Nombre.set(True)
           elif num_names == 4:
               Nombre_perfil.config(text="Nombre: "+ nombre_separado[0]+ " "+ nombre_separado[1] )
               ApellidoPaterno_perfil.config(text="Apellido Paterno: "+ nombre_separado[2])
               ApellidoMaterno_perfil.config(text="Apellido Materno: "+ nombre_separado[3])
               Bool_add_Nombre.set(True)
            #### en del num_names                
        else:
            Nombre_perfil.config(text=nombreperfil_default_txt)
            ApellidoPaterno_perfil.config(text= Apellido_Paterno_perfil_default_txt)
            ApellidoMaterno_perfil.config(text= Apellido_Materno_perfil_default_txt)
            Bool_add_Nombre.set(False)
        ####
    ####
    nombre_alumno_str.trace("w", copiar_nombre)

    tk.Label(izquierda, text="Nombre:").grid(row=1, column=0)
    validacion_name = ventana_confirmacion.register(validar_nombre)
    entrada_nombre = tk.Entry(izquierda, width=30, textvariable=nombre_alumno_str, validate="key", validatecommand=(validacion_name, "%P"))
    entrada_nombre.grid(row=1, column=1)


    tk.Label(izquierda, text="Ruta Imagen:").grid(row=2, column=0)
    entrada_ruta = tk.Entry(izquierda, width=30)
    entrada_ruta.grid(row=2, column=1)
    entrada_ruta.configure(state="disabled")


    ###################################### BOTONES E INTERACCIÓN
    seleccion_img = tk.Button(izquierda, text="Seleccionar Imagen", command=agregar_imagen)
    seleccion_img.grid(row=3, column=0, columnspan=2, pady=20)
    btnguardar_registro = tk.Button(derecha, text="Guardar Registro", command=guardar_registro)
    btnguardar_registro.grid(row=7, column=0, columnspan=2, pady=10)
    btnguardar_registro.configure(state="disabled")
    

    Anuncio_derecha = tk.Label(derecha, text="[Selecciona una imagen]")
    Anuncio_derecha.grid(row=1, column=0, pady=(5, 0), columnspan=2, sticky='n')  

    frame_original = cv2.imread("Images/prueba_2.png")
    alto, ancho, canales = frame_original.shape
    # Calcula la nueva altura manteniendo el mismo aspect ratio
    nueva_alto = min(alto, 200)
    nueva_ancho = int((nueva_alto / alto) * ancho)
    

    frame_original = cv2.cvtColor(frame_original, cv2.COLOR_BGR2RGB)
    frame_original = cv2.resize(frame_original, (   round(nueva_ancho)  , round(nueva_alto)))# lo regresa a su resolución original por si se redujo para acelerar el procesamiento
    imagen_tk = ImageTk.PhotoImage(Image.fromarray(frame_original))
    labelimg = tk.Label(derecha, image = imagen_tk)
    labelimg.grid(row=2, column=0, columnspan=2, pady=(0, 5))
    #labelimg.image = imagen_tk  # Esto es importante para evitar que Python "limpie" la imagen
    #label.pack(side=tk.LEFT, padx=(5, 0), pady=(2,0),anchor='n')
    
    

    Codigo_perfil = tk.Label(derecha, text=Codigoperfil_default_txt)
    Codigo_perfil.grid(row=3, column=0, pady=(5, 0), sticky='w')  
    Nombre_perfil = tk.Label(derecha, text=nombreperfil_default_txt )
    Nombre_perfil.grid(row=4, column=0, pady=(5, 0), sticky='w')  
    ApellidoPaterno_perfil = tk.Label(derecha, text=Apellido_Paterno_perfil_default_txt)
    ApellidoPaterno_perfil.grid(row=5, column=0, pady=(5, 0), sticky='w')  
    ApellidoMaterno_perfil = tk.Label(derecha, text=Apellido_Materno_perfil_default_txt)
    ApellidoMaterno_perfil.grid(row=6, column=0, pady=(5, 0), sticky='w')


    # esto ocurre al final casi para reajustar el tamaño de la imagen
    ventana_confirmacion.update_idletasks()  # Asegura que los widgets se han creado y configurado
    ancho_requerido = ventana_confirmacion.winfo_reqwidth()  # Obtiene el ancho requerido
    alto_requerido = ventana_confirmacion.winfo_reqheight()  # Obtiene el ancho requerido
    ventana_confirmacion.geometry(f"{ancho_requerido}x"f"{alto_requerido}"  )  # Establece el ancho de la ventana

#### definir función de mostrar ventana confirmación

root = tk.Tk()

etiqueta_principal = tk.Label(root, text="Ventana Principal")
etiqueta_principal.pack()

boton_confirmacion = tk.Button(root, text="➕ Añadir Alumno", command=mostrar_ventana_confirmacion)
boton_confirmacion.pack()

root.mainloop()
