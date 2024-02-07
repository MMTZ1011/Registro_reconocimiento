import os
import cv2
import csv
import tkinter as tk
import face_recognition
import datetime
import pandas as pd
import json
import time
import threading

import pygame.mixer

import Event_listeners


colddown_conocido = 120 # segundos
colddown_unknown = 15 # segundos


DEVELOPER_MODE = True

carpeta_DB =  "BaseDatos_caras"




def play_sound(file_path):
    # Inicializa el mixer
    pygame.mixer.init()
    
    # Carga y reproduce el sonido
    pygame.mixer.music.load(file_path)
    pygame.mixer.music.play()

    # Espera a que termine la música para no cerrar el programa
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)  # Puedes ajustar este número para que sea más eficiente
    ####while
## def play_sound


def play_sound_non_blocking(file_path):
    hilo_sonido = threading.Thread(target=play_sound, args=(file_path,))
    hilo_sonido.start()
####




def dividir_por_espacios(texto):
    palabras = texto.split()
    return palabras
#### end de dividir por espacios

def obtener_piezas_nombre(contenido):
    
    nombre_separado = dividir_por_espacios(contenido)
    num_names = len(nombre_separado)

    if num_names == 3: # caso valido Si es nombre, apellido paterno y apellido materno
        name_0 = nombre_separado[0]
        name_1 = ""
        lastname_dad = nombre_separado[1]
        lastname_mom = nombre_separado[2]
    elif num_names == 4: #caso valido si es nombre 1, nombre 2, apellido paterno y apellido materno
        name_0 = nombre_separado[0]
        name_1 = nombre_separado[1]
        lastname_dad = nombre_separado[2]
        lastname_mom = nombre_separado[3]
    #####
    return name_0, name_1, lastname_dad, lastname_mom
### end de obtener las piezas que componen un nombre

def float_a_hora(flotante):
    horas = int(flotante)
    minutos = int((flotante - horas) * 60)
    return "{:02d}:{:02d}".format(horas, minutos)
# el numero flotante


def  verifica_ruta_carpeta(carpeta):

    ruta_carpeta = os.path.join(os.getcwd(), carpeta) # Obtiene la ruta completa de la carpeta
    if not os.path.exists(ruta_carpeta): # Verifica si la carpeta existe
        os.makedirs(ruta_carpeta) # Si no existe, la crea
    ####
### end de verifica la ruta de la carpeta


def verifica_ruta_registrocsv(ruta_registros):
    if not os.path.exists(ruta_registros):
        with open(ruta_registros, 'w', newline='') as archivo_csv:# Si no existe, pues a crearlo
            escritor = csv.writer(archivo_csv)            
            escritor.writerow(['Codigo de Estudiante', 'Nombre_1', 'Nombre_2', 'Apellido_Paterno', 'Apellido_Materno', 'primera_vez_hoy','ultima_vez_hoy', "ultimo_dia", 'horas_hoy', 'veces_hoy', 'Dias_Asistiendo'])# Estos son los encabezados por defecto
        ### del with de csv que se crea
    ### end de si no existe la ruta donde esta el .csv
### end de verifica ruta registros csv


def verifica_ruta_ListaAlumnos(ruta_lista):
    if not os.path.exists(ruta_lista):
        with open(ruta_lista, 'w', newline='') as archivo_csv:# Si no existe, pues a crearlo
            escritor = csv.writer(archivo_csv)            
            escritor.writerow(['Codigo de Estudiante', 'Nombre Completo', "Asistencias" ])# Estos son los encabezados por defecto
        ### del with de csv que se crea
    ### end de si no existe la ruta donde esta el .csv
### end de verifica ruta  Lista de asistencias


def verifica_ruta_Asistencias(ruta_asistencia):
    if not os.path.exists(ruta_asistencia):
        with open(ruta_asistencia, 'w', newline='') as archivo_csv:# Si no existe, pues a crearlo
            escritor = csv.writer(archivo_csv)            
            escritor.writerow(['Codigo de Estudiante', 'Nombre Completo' ])# Estos son los encabezados por defecto
        ### del with de csv que se crea
    ### end de si no existe la ruta donde esta el .csv
### end de verifica ruta de asistencias csv


def verifica_logs(ruta_logs):
    if not os.path.exists(ruta_logs):
        with open(ruta_logs, 'w', newline='') as archivo_csv:# Si no existe, pues a crearlo
            escritor = csv.writer(archivo_csv)            
            
            escritor.writerow(['Dia', 'Hora', 'Alumno', 'Codigo', 'Veces Paso', 'Duracion','Imagen' ])# Estos son los encabezados por defecto

        ### del with de csv que se crea
    ### end de si no existe la ruta donde esta el .csv
### end de verifica ruta de logs



def guardado_registros(codigo_alumno_int, name_0, name_1, lastname_dad, lastname_mom):
    # GUARDA el csv de la relación de cara con el alum no
    with open(carpeta_DB + '/_Registros.csv', mode= 'a', newline='') as archivo_csv:
        escritor_csv = csv.writer(archivo_csv)
        escritor_csv.writerow([codigo_alumno_int, name_0, name_1, lastname_dad, lastname_mom])
    #### de cuando puede guardar el registro
## end del guardado de cada alumno y su relación con el rostro en el sistema.



def guardado_Lista(codigo_alumno_int, e_student_name, asistencias_int):
    # GUARDA el csv de la relación de cara con el alum no
    with open(carpeta_DB + '/_ListaAlumnos.csv', mode= 'a', newline='') as archivo_csv:
        escritor_csv = csv.writer(archivo_csv)
        escritor_csv.writerow([codigo_alumno_int, e_student_name, asistencias_int])
    #### de cuando puede guardar el registro
## end del guardado de cada alumno y su relación con el rostro en el sistema.


def guardado_Asistencias_primera_vez(codigo_alumno_int, e_student_name):
    # GUARDA el csv de la relación de cara con el alum no
    with open(carpeta_DB + '/_Asistencias.csv', mode= 'a', newline='') as archivo_csv:
        escritor_csv = csv.writer(archivo_csv)
        escritor_csv.writerow([codigo_alumno_int, e_student_name])
    #### de cuando puede guardar el registro
## end del guardado de cada alumno y su relación con el rostro en el sistema.



def safe_str(value):
    if pd.isna(value):
        return ""
    return str(value)
### end de safe_str
















def Cara_Carga_Registro(obj):
    archivo_csv = carpeta_DB + '/' + "_Registros.csv" # Ruta de los registros de las caras que ya están asociadas a nombres:


    
    # Variables que se necesitan:
    total_alumnos = 0
    alumnos_sin_foto = [] #aqui guarda los codigos y los que no tienen foto
    fotos_no_existen = 0
    alumnos_contados = 0

    #los knowns
    known_face_encodings  = [] # Aqui va guardando lo del enconding
    known_vatos_info = []  # la info de codigo y nombre del alumno.
    known_codigos_info = []  # la info de codigo y nombre del alumno.

    obj.set_texto_progress(  "1/2"  +" Cargando Estudiantes...")



    verifica_ruta_registrocsv(archivo_csv)# ahora verifica donde está el _Registros.csv de cada relación imagen- alumno que hay
    
    # Ahora carga 
    with open(archivo_csv, 'r') as archivo:
        for linea in archivo:
            total_alumnos += 1
    total_alumnos -= 1 # Restar 1 para excluir la primera línea (encabezados)
    
    obj.set_num_texto_progress( str(alumnos_contados) + "/" + str(total_alumnos) + " Estudiantes cargados."  )
    

    # ya que detectó el numero de estudiantes que debe cargar, ahora carga bien toda la lista una por una.
    with open(archivo_csv, newline='') as archivo_cargado:
        lector_csv = csv.reader(archivo_cargado)
        next(lector_csv) # Ignorar la primera fila (encabezados de codigo y nombre)
        
        print("v1.2 de metiendo caras a la ia...")

        alumno_i = 1
        for fila in lector_csv: # Iterar a través de las filas del CSV
            i_codigo = fila[0]
            
            i_nombre_1 = fila[1]
            i_nombre_2 = fila[2]

            i_apellido_paterno = fila[3]
            i_apellido_materno = fila[4]
            nombre_completo = i_nombre_1 + i_nombre_2  + i_apellido_paterno + i_apellido_materno


            nombre_archivo = carpeta_DB +"/" + str(i_codigo) +".dat"
            ruta_temporal = carpeta_DB +"/" + "TemporalImg" +".jpg"
            existe_foto = os.path.exists(nombre_archivo) #checa si existe la foto
            if not existe_foto:
                nombre_archivo = carpeta_DB + "/" + str(i_codigo) +".jpg"
                existe_foto = os.path.exists(nombre_archivo) #checa si existe la foto
            #### de si no existe como jpg pruebe como png

            if existe_foto: #existe la foto en la carpetota
                
                # se supone que la foto de la base de datos ya está recortada, entonces nada más busca los face encodings
                # y ya lo manda a usar en el encodings
                with open(nombre_archivo, 'rb') as file_dat:
                    data_dat = file_dat.read()
                ### lo que clona

                with open(ruta_temporal, 'wb') as file_jpg:
                    file_jpg.write(data_dat)
                ### clona el dat
                
                foto_cargada = cv2.imread(ruta_temporal) #carga el archivon

                os.remove(ruta_temporal) #borra el archivo temporal que creó para poder cargar el imread


                face_loc = face_recognition.face_locations(foto_cargada)[0] #localiza donde ve una cara
                #print("face_loc:", face_loc)
                face_image_encodings = face_recognition.face_encodings(foto_cargada, known_face_locations=[face_loc]) # lo mete a la ia

                i_encoding = face_image_encodings[0] # encoding de cara actual osea la index 0

               
                # guarda en un array el encoding, el nombre y el código para usarlo después.
                known_face_encodings.append(i_encoding) # hace append del encoding actual
                known_vatos_info.append(i_nombre_1) # le envia el primer nombre por que ahi nomas sirve para mostrar el primer nombre.
                known_codigos_info.append(i_codigo) # le envia el primer nombre por que ahi nomas sirve para mostrar el primer nombre.
                
            else: ##no existe la foto
                alumnos_sin_foto.append(str(i_codigo)+ " - "+ nombre_completo)
                fotos_no_existen = fotos_no_existen + 1
            #### de si existe foto
            alumnos_contados = alumnos_contados + 1
            
            obj.set_num_texto_progress( str(alumnos_contados) + "/" + str(total_alumnos) + " Estudiantes cargados."  )
            obj.set_progress_barra(int((alumnos_contados/total_alumnos)*90))

            alumno_i += 1
        ## end del for de cada fila del csv
    ### end del with open ese

    # actualiza los encodings que encontró:
    #obj.known_face_encodings = known_face_encodings
    #obj.known_vatos_info = known_vatos_info
    #obj.known_codigos_info = known_codigos_info
    
    
    # Ahora imprime los resultados para que el developer sepa que pudo estar bien o mal:
    print("")
    print("")
    print("Cargado con éxito")
    print("--------------------------------------")
    print("Se encontraron "+  str(alumnos_contados) +" alumnos")
    print("de los cuales "+  str(fotos_no_existen) +" no se encontro su foto")
    for alumno in alumnos_sin_foto:
        print("No se encontró su foto: "+ alumno)
    #### del for que recorre cada alumno sin fotillo
    print("--------------------------------------")

   
    
    return known_face_encodings, known_vatos_info, known_codigos_info
### end de carga Registro de Alumnos.




def Guardar_nuevo_alumno(codigo_alumno_int, e_student_name, imagen_global, ):
    Exito_guardando = False

    #divide el nombre por nombres y apellidos materno y paterno:
    name_0, name_1, lastname_dad, lastname_mom = obtener_piezas_nombre(e_student_name)


    ruta_registros = carpeta_DB + '/' + "_Registros.csv"
    ruta_alumnos_Lista = carpeta_DB + '/' + "_ListaAlumnos.csv"
    ruta_alumnos_Asistencias = carpeta_DB + '/' + "_Asistencias.csv"
    ruta_Logs = carpeta_DB + '/' + "_Logs.csv"
    ruta_guardado_img = carpeta_DB + '/' + str(codigo_alumno_int) + ".jpg"  # Reemplaza 'ruta_de_tu_carpeta' con la ruta de tu carpeta
    ruta_guardado_dat = carpeta_DB + '/' + str(codigo_alumno_int) + ".dat"

    # aca empiezan las verificaciones:
    verifica_ruta_carpeta(carpeta_DB)# verifica la ruta donde está la carpeta mismas de la base de datos:

    verifica_ruta_registrocsv(ruta_registros)# ahora verifica donde está el _Registros.csv de cada relación imagen- alumno que hay
    verifica_ruta_ListaAlumnos(ruta_alumnos_Lista) # verifica donde está la lista de alumnos acá alv
    verifica_ruta_Asistencias(ruta_alumnos_Asistencias) # verifica donde está la lista de alumnos acá alv

    verifica_logs(ruta_Logs) # solo lo verifica por si es la primera vez que está aquí, lo genere 

    # GUARDA la imagen del alumno original
    cv2.imwrite(ruta_guardado_img, imagen_global) # guarda la imagen
    os.rename(ruta_guardado_img, ruta_guardado_dat) # sustituye el nombre

    guardado_registros(codigo_alumno_int, name_0, name_1, lastname_dad, lastname_mom)

    asistencias_int = 0 # como es la primera vez que asiste por que recien lo guarda, le pone que cero asistencias al wey
    guardado_Lista(codigo_alumno_int, e_student_name, asistencias_int)
    
    guardado_Asistencias_primera_vez(codigo_alumno_int, e_student_name)


    Exito_guardando = True # lo guarda una vez comprueba que guardo exitosamente.    

    return Exito_guardando
#### end de Guardar_nuevo_alumno 








def read_dato_registro_usuario(codigo_estudiante, nombredato):
    df = pd.read_csv(carpeta_DB + '/_Registros.csv')# Cargamos el CSV en un DataFrame
    estudiante = df[df['Codigo de Estudiante'] == (int(codigo_estudiante))]# Buscamos la fila que corresponde al estudiante
    if not estudiante.empty:# si si existe este vato entonces se continua:
        return estudiante.iloc[0][nombredato]
    else:
        return None
    ### end de si es o no un estudiante registrado
## end de leer una cosa del registro

def obtener_registro_usuario(codigo_estudiante):
    df = pd.read_csv(carpeta_DB + '/_Registros.csv') # Cargamos el CSV en un DataFrame
    estudiante = df[df['Codigo de Estudiante'] == (int(codigo_estudiante))]# Buscamos la fila que corresponde al estudiante
    if not estudiante.empty:# si si existe este vato entonces se continua:
        return estudiante.iloc[0]
    else:
        return None
    ### end de si es o no un estudiante registrado
### end de obtener el registro del usuario


def set_dato_registro_usuario(codigo_estudiante, nombredato, nuevo_valor):
    df = pd.read_csv(carpeta_DB + '/_Registros.csv')# Cargamos ese CSV en un DataFrame, como ya sabes hacer
    estudiante_idx = df[df['Codigo de Estudiante'] == int(codigo_estudiante)].index # Buscamos el índice del estudiante, igual que en tu función de lectura

    if not estudiante_idx.empty:  # Si encontramos al vato
        df.at[estudiante_idx[0], nombredato] = nuevo_valor # Actualizamos el dato. Aquí usamos 'at' porque ya tenemos el índice y el nombre de la columna
        df.to_csv(carpeta_DB + '/_Registros.csv', index=False)# Guardamos el DataFrame actualizado en el archivo CSV
    else:  # Si no encontramos al estudiante
        # Pues aquí puedes hacer lo que quieras, como añadir una nueva fila o lanzar una excepción
        print("Ese vato no existe, compa.")
    ### de los ifs de si no es empty
### set dato de registro de usuario

def actualizar_registro_estudiante(codigo_estudiante, **datos):
    ruta_archivo = carpeta_DB + '/_Registros.csv'
    df = pd.read_csv(ruta_archivo) # Cargamos ese CSV en un DataFrame, como ya sabes hacer
    estudiante_idx = df[df['Codigo de Estudiante'] == int(codigo_estudiante)].index

    if not estudiante_idx.empty:  # Si encontramos al vato
        for nombredato, nuevo_valor in datos.items():
            df.at[estudiante_idx[0], nombredato] = nuevo_valor # Actualizamos los datos. Aquí usamos 'at' porque ya tenemos el índice y el nombre de la columna
        df.to_csv(ruta_archivo, index=False) # Guardamos el DataFrame actualizado en el archivo CSV una sola vez.
    else:
        # Pues aquí puedes hacer lo que quieras, como añadir una nueva fila o lanzar una excepción
        print("Ese vato no existe, compa.")
    ###
#### de función de actualizar_registro_estudiante



def set_num_asistencias_totales(codigo_estudiante, Numero):
    df = pd.read_csv(carpeta_DB + '/_ListaAlumnos.csv')# Cargamos ese CSV en un DataFrame, como ya sabes hacer
    estudiante_idx = df[df['Codigo de Estudiante'] == int(codigo_estudiante)].index # Buscamos el índice del estudiante, igual que en tu función de lectura

    if not estudiante_idx.empty:  # Si encontramos al vato
        df.at[estudiante_idx[0], "Asistencias"] = Numero # Actualizamos el dato. Aquí usamos 'at' porque ya tenemos el índice y el nombre de la columna
        df.to_csv(carpeta_DB + '/_ListaAlumnos.csv', index=False)# Guardamos el DataFrame actualizado en el archivo CSV
    else:  # Si no encontramos al estudiante
        # Pues aquí puedes hacer lo que quieras, como añadir una nueva fila o lanzar una excepción
        print("Ese vato no existe, compa.")
    ### de los ifs de si no es empty
### set dato de registro de usuario


def agregar_registro_logs(dia, hora, alumno, codigo, primera_vez_hoy, duracion, imagenruta):
    # Preparamos el registro nuevo
    nuevo_registro = [dia, hora, alumno, str(codigo), primera_vez_hoy, duracion, imagenruta]
    
    # Abrimos el archivo en modo append ('a') para agregar el registro al final
    with open(carpeta_DB + '/_Logs.csv', 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(nuevo_registro)
    ###
### agregara al registro de logs


def agregar_horas_asistidas_hoy(codigo_estudiante, strptime_dia_actual, value_horas  ):
    df = pd.read_csv(carpeta_DB + '/_Asistencias.csv')
    # Verificamos si la columna existe en el DataFrame
    if strptime_dia_actual in df.columns:
        pass
    else:
        df[strptime_dia_actual] = None

        df.to_csv(carpeta_DB + '/_Asistencias.csv', index=False) # guarda el archivo
    ### si encontró el dia o no

    # Buscamos la fila que corresponde al estudiante
    estudiante_index = df[df['Codigo de Estudiante'] == codigo_estudiante].index

    # Si encontramos el vato en el DataFrame
    if not estudiante_index.empty:  # Si encontramos al vato
        df.at[estudiante_index[0], strptime_dia_actual] = value_horas
        df.to_csv(carpeta_DB + '/_Asistencias.csv', index=False) #LO GUARDA
    ####

### agregar horas de asistencia



def obtener_fecha_hora():
    ahora = datetime.datetime.now()# Obtiene el momento actual
    
    # Extrae el día, mes, año, hora, minuto y segundo
    dia = ahora.day
    mes = ahora.month
    año = ahora.year
    hora = ahora.hour
    minuto = ahora.minute
    segundo = ahora.second

    return dia, mes, año, hora, minuto, segundo
### obtener fecha y hora.







def Deteccion_persona_Conocida(  i_codigo =None):
    Nuevo_Dia = False
    datos_usuario = obtener_registro_usuario(i_codigo)

    if str(datos_usuario["ultima_vez_hoy"]) == "nan" : #Primera vez que guarda un dato.
        Nuevo_Dia = True
    else: # si no es un valor nulo el de ultima vez entonces puede acceder a él
        ultimo_dia_obtenido = str(datos_usuario["ultimo_dia"])
        ultimo_dia = datetime.datetime.strptime(ultimo_dia_obtenido, "%d/%m/%Y").date()
        # Obtenemos la fecha actual
        dia_actual = datetime.datetime.now().date()
        # Comparamos

        if dia_actual > ultimo_dia:
            Nuevo_Dia = True
        else:
            Nuevo_Dia = False
        #### si es el dia nuevo o no
    #### if de la ultima vez o del dia nuevo
            
    ### de si es nan la ultima vez osea que es la primera vez que está aqui
    if Nuevo_Dia == True:
        nombre_del_alumno = safe_str(datos_usuario["Nombre_1"]) + " " + safe_str(datos_usuario["Nombre_2"]) + " " + safe_str(datos_usuario["Apellido_Paterno"]) + " " +  safe_str(datos_usuario["Apellido_Materno"]) 

        
        # si es un nuevo dia entonces nada mas guarda los datos del dia este
        dia, mes, año, hora, minuto, segundo = obtener_fecha_hora() # Obtiene el dia, mes año, hroa minuto y segundo
        strptime_hora_actual = str(hora) + ":" + str(minuto) + ":" + str(segundo)
        strptime_dia_actual = str(dia) + "/" + str(mes) + "/" + str(año)

        #GUARDA:
        dias_asistiendo = datos_usuario["Dias_Asistiendo"]

        if str(dias_asistiendo)  == "nan": #si es su primer día asistiendo:
            dias_asistiendo = 1 #pone su primerito día
        else:
            dias_asistiendo = dias_asistiendo + 1 #le añade otro dia
        ### Dias asistiendo


        actualizar_registro_estudiante(i_codigo,
                        primera_vez_hoy=strptime_hora_actual,
                        ultima_vez_hoy=strptime_hora_actual,
                        ultimo_dia=strptime_dia_actual,
                        horas_hoy=0,
                        veces_hoy=0, 
                        Dias_Asistiendo=dias_asistiendo)


        # EL numero de asistencias totales
        set_num_asistencias_totales(i_codigo, dias_asistiendo) # pone el numero total de las asistencais

        # Registro logs para que vean como se meteiendo
        agregar_registro_logs(strptime_dia_actual, strptime_hora_actual, nombre_del_alumno, i_codigo, 0, 0, "")

        # añade horas asistidas
        agregar_horas_asistidas_hoy(i_codigo, strptime_dia_actual, 0)


        play_sound_non_blocking("Sonidos/Detectado_PrimeraVez.mp3")

    elif Nuevo_Dia == False: # es el mismo dia.

        # Revisa el debunce  para este alumno o persona
        tiempo_actual = time.time()
        # Fecha actual
        fecha_actual = datetime.datetime.now().date()
        
        hoy_debunce = datetime.datetime.combine(fecha_actual, datetime.datetime.strptime(datos_usuario["ultima_vez_hoy"], "%H:%M:%S").time()) .timestamp()
        
        if tiempo_actual > (hoy_debunce + colddown_conocido): 
            nombre_del_alumno = safe_str(datos_usuario["Nombre_1"]) + " " + safe_str(datos_usuario["Nombre_2"]) + " " + safe_str(datos_usuario["Apellido_Paterno"]) + " " +  safe_str(datos_usuario["Apellido_Materno"]) 

            dia, mes, año, hora, minuto, segundo = obtener_fecha_hora() # Obtiene el dia, mes año, hroa minuto y segundo
            strptime_hora_actual = str(hora) + ":" + str(minuto) + ":" + str(segundo)
            strptime_dia_actual = str(dia) + "/" + str(mes) + "/" + str(año)

            #### actualiza la ultima vez de hora
            #set_dato_registro_usuario(i_codigo, "ultima_vez_hoy", strptime_hora_actual)

            #### el numero de veces pasado por la camara hoy
            veces_hoy = datos_usuario["veces_hoy"] + 1
            #set_dato_registro_usuario(i_codigo, "veces_hoy", veces_hoy)

            ##### busca la primera vez hoy la vez actual.
            hora_inicial_str = datos_usuario["primera_vez_hoy"]
            hora_final_str = strptime_hora_actual # la hora actual

            hora_inicial = datetime.datetime.strptime(hora_inicial_str, "%H:%M:%S")
            hora_final = datetime.datetime.strptime(hora_final_str, "%H:%M:%S")

            diferencia = hora_final - hora_inicial # Calculamos la diferencia
            diferencia_en_horas = round(diferencia.seconds / 3600 , 2) # Convertimos la diferencia a horas decimales
            #set_dato_registro_usuario(i_codigo, "horas_hoy", diferencia_en_horas)

            actualizar_registro_estudiante(i_codigo,
                            ultima_vez_hoy= strptime_hora_actual,
                            horas_hoy= diferencia_en_horas,
                            veces_hoy= veces_hoy )
            # Registro LOGS para que vean como se meteiendo
            
            agregar_registro_logs(strptime_dia_actual, strptime_hora_actual, nombre_del_alumno, i_codigo, veces_hoy, float_a_hora(diferencia_en_horas), "")
            # Añade horas asistidas
            agregar_horas_asistidas_hoy(i_codigo, strptime_dia_actual, diferencia_en_horas)

            
            play_sound_non_blocking("Sonidos/Detectado_Conocido.mp3")
        else:
            pass
        ###



        

    ### De si es un nuevo dia True or False:


## de si es un conocido entonces procede.


unknown_debounce = 0
def Deteccion_Desconocido(Frame_snapshot=None):
    global unknown_debounce
    tiempo_actual = time.time()

    if tiempo_actual > unknown_debounce + colddown_unknown:
        
        ### INICIA CONTENIDO DE LA FUNCIÓN
        dia, mes, año, hora, minuto, segundo = obtener_fecha_hora() # Obtiene el dia, mes año, hroa minuto y segundo
        strptime_hora_actual = str(hora) + ":" + str(minuto) + ":" + str(segundo)
        strptime_dia_actual = str(dia) + "/" + str(mes) + "/" + str(año)
        
        # guardado de imagen
        if Frame_snapshot is not None:
            # Vamos a darle un nombre único a la foto, para no andar sobrescribiendo cochinadas

            # Obtenemos la fecha y hora actual
            fecha_hora_actual = datetime.datetime.now()
            nombre_formato = fecha_hora_actual.strftime('%Y_%m_%d_%H_%M_%S') # Formateamos la fecha y hora al estilo que quieres
            nombre_foto = os.path.join("Fotos_Desconocidos", f"UnKnown_{nombre_formato}.jpg")# Generamos el nombre del archivo
            if not DEVELOPER_MODE:
                cv2.imwrite(nombre_foto, Frame_snapshot) # guarda la imagen
                agregar_registro_logs(strptime_dia_actual, strptime_hora_actual, "Unknown", "", "---", "---", nombre_foto )
            else:
                #agregar_registro_logs(strptime_dia_actual, strptime_hora_actual, "Unknown", "", "---", "---", "[Unknown developer Mode]" )
                pass
            #### si no está en el modo developer entonces guarda la foto

        else:
            agregar_registro_logs(strptime_dia_actual, strptime_hora_actual, "Unknown", "", "---", "---", "No hay foto")
        ## Frame_snapshot




        ### FIN CONTENIDO DE LA FUNCIÓN
        unknown_debounce = tiempo_actual
    else:
        #print("no entro")
        pass
    ###

    
####






#Deteccion_persona_Conocida( "214451676")
"""
Deteccion_Desconocido()
Deteccion_Desconocido()
time.sleep(3)
Deteccion_Desconocido()
time.sleep(10)
Deteccion_Desconocido()
"""

