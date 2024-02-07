# Proyecto de Reconocimiento Facial

![Logo del Proyecto](ruta/a/logo.png)

Version Beta 1.1

Present vision
Esta parte del proyecto es parte de la app y el proyecto general de IlabTDI para el nombramiento de lista desarrollado por Martín Eduardo Martínez Barrera en iLabTDI 2023.

En iLabTDI estamos a la vanguardia en visión por computadora y aprendizaje automático para llevar a cabo el reconocimiento facial en tiempo real. La aplicación tiene la capacidad de detectar y reconocer personas a través de cámaras, permitiendo un control de acceso eficiente y seguro en entornos de clase y salones internos. 

Además, cuenta con una interfaz intuitiva diseñada en tkinter para una experiencia de usuario óptima.


## Funcionalidades

- Detección y reconocimiento de caras en imágenes estáticas.
- Reconocimiento facial en tiempo real desde una cámara.
- Interfaz gráfica de usuario (GUI) para facilitar la interacción.
- Entrenamiento del modelo con nuevas imágenes de personas.
- Tomado de lista.

## ORDEN DE ARCHIVOS:
- Main.py : Es el código principal el que ejecuta todos los demás.
- App_class.py: Lo relacionado con la app que más que nada corresponde a las ventanas de escritorio que genera.
- Camara_class.py: lo relacionado a la camara y el procesamiento. Si 


## Requisitos del Sistema

- OpenCV
- face-recognition 1.3.0
- face-recognition-models 0.3.0
- Documentación del face-recognition: https://pypi.org/project/face-recognition/
- Python 3.x
- Bibliotecas: OpenCV, tkinter, numpy, etc. (Consulte el archivo requirements.txt)
- el visual studio moradito con dlib


## Updates 1.1:
- Event listener
- Sonido para primera vez y siguientes veces
- reduccion de calidad de imagen de unknown
- Imagenes encriptadas.
- Apertura de los .csv


## Update 1.1.1:
- Arreglado bug de lista
- Arreglado bug de string en vez de int
- mejora en la velocidad de carga.
- se medio mete los listeners para acceder a los logs y mandarlos a whatsapp, telegram, drive o un lugar donde tener respaldo e incluso gurdado.


# Carpetas:
- BaseDatosCara: los archivos que inician con _ y 000temp son los que puse que no se deben mover y sirven como donde se almacena el backend, los .dat son las imagenes .jpg 
- build: no se mueve, es algo del face-recognition
- Credenciales: esta incompleto, es donde estaba poniendo los datos de googledrive api se puede borrar
- Dist: es el intento de generar el exe que permita abrir el main.py sin acceder aqui al visual studio, sino tener el puro ejecutable.
- FaceRecon_workspace: no se mueve, lo genera la libreria
- Fotos desconocidos: Donde se almacenan las fotos de los que la camara no identifico 
- Imagenes: aqui fui poniendo imagenes de los del servicio para tenerlas a la mano al registrarlos
- ImagenesSrc: las que iba usar para la propia app y ventanas
- Sonidos: Los sonidos de cuando detecta la cara poder avisar.
- Ya no necesarios: Estan las cosas viejas que ya no se necesitaron

# Codigos:
- Add_Alumnos_class.py: La ventana para añadir alumnos de la app
- App_Class.py: la clase correspondiente a la ventana
- Camara_Class.py: La clase correspondiente a la camara
- config.py: aqui iba poner los parametros para configurar globalmente cada aspecto de la app
- cosas.py: un ejemplo nada mas para abrir los .csv sin excel
- DataBase_Class.py: Aqui va el backend
- googledrive.py: Aqui iba poner lo de la api para mandar a googledrive cada .csv  y tenerlos como copia de seguridad pero me fallaron los auth tokens
- iaGoogle.py: aqui andaba probando la api de google de text to speech para que dijera el nombre de cada alumno que detectara segun la base de datos
- Main.py: el codigo principal ejecutable
- requeriments.txt: donde esta lo que se necesita descargar para el proyecto.


## Instalación

1. Clone este repositorio en su compu local.
2. Instale las dependencias utilizando el siguiente comando:
3. Listo

## Ejecutar
4. Para ejecutar se necesita entrar al archivo Main.py y ese ejecutarlo. Tardara un poco por que de las caras que estan guardadas, 


# a considerar:
- si se guarda una cara se debe reiniciar el progrma, cerrarlo y correrlo de nuevo
- como es un modelo de aprendizaje, requiere mucho procesador o tarjeta grafica, aun no corre en gpu el procesamiento de imagen.
- Se necesita tener el visual studio morado ya que ese descarga en automatico unos builds bien importantes para cuando se hace el pip install al face-recognition models, sin el visual studio morado que ya incluye una libreria del dlib entonces a cada rato va mandar un error de que no se pudo.
- Toma fotos cuando encuentra una cara desconocida y la guarda en una carpeta de Fotos_desconocidos
- si la compu tiene la paqueteria de windows por defecto para los .csv, abrirá los .csv en excel todo bien hasta ahi, sino manualmente se debe ingresar a ellos desde BaseDatos_Caras
- De preferencia la persona debe ver la camara para la hora de salida y de entrada.
- Si corre en tiempo real y es veloz, en algunos momentos a caras conocidas las interpretara como desconocidas cuando su cara tal vez sale recortada por el margen.
- Se puede modificar el valor de sensibilidad para detectar esta en camara_class.py y es el de tolerancia_ia, el que puse segun yo esta mas que perfecto.



# Lo que falta:
- falta conectar de los logs al archivo ya sea googledrive.py o algo que lo matenga guardado y seguro.
- Falta que el codigo se ejecute en segundo plano todo el tiempo incluso cuando la sesión de windows este cerrada.


```bash
pip install -r requirements.txt