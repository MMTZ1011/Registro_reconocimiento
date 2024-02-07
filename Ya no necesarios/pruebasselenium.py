from selenium import webdriver
from selenium.webdriver.common.by import By

from time import sleep
import threading

Logindatos = {
    'username': 'iLabTDI_Test01@proton.me',
    'password': 'Zapopan201'
}

driver = webdriver.Chrome() #Inicia el driver
url = 'https://view.wyze.com/' # entra a la página de Login
driver.get(url) #Se mete al y empieza a usar el navegador



pagina_login_usado = False
def pagina_login():
    global pagina_login_usado# la va usar
    if pagina_login_usado == True:
        return
    ####
    print("Entró a pagina de login")
    E_username_id = driver.find_element(By.ID, "username")
    E_password_id = driver.find_element(By.ID, "password")
    E_submitButton_id = driver.find_element(By.ID, "submitbtn")

    E_username_id.send_keys(Logindatos["username"])
    E_password_id.send_keys(Logindatos["password"])
    driver.execute_script("arguments[0].innerText = 'Dale click aqui wey';", E_submitButton_id)

    pagina_login_usado = True
### end pagina de login

pagina_code_usado = False
def pagina_code():
    global pagina_code_usado# la va usar
    if pagina_code_usado == True:
        return
    ####
    print("Entró a página del code de verification")
####


pagina_live_usado = False
def pagina_live():
    global pagina_live_usado# la va usar
    if pagina_live_usado == True:
        return
    ####
    print("Entró a página del livel")

    # Encontrar el elemento que deseas hacer clic (por ejemplo, un botón)
    Button_class = driver.find_element(By.CLASS_NAME, 'c-fYPKku')  # Reemplaza 'elemento_id' con el ID real del elemento
    Button_class.click()
####




def verificar_pag():
    while True:
        # Coloca aquí la lógica que deseas verificar cada 2 segundos
        url_actual = driver.current_url
        if url_actual == "https://auth.wyze.com/login":
           pagina_login()#lo manda a ejecutar
        elif url_actual == "https://auth.wyze.com/login/mfa/code?sendEmailCodeResult=true":
            pagina_code() #lo manda a ejecutar
        elif url_actual == "https://view.wyze.com/live":
            pagina_live() #lo manda a ejecutar
        # Espera 2 segundos antes de verificar nuevamente
        sleep(2)
    ####
####
        

# Inicia el hilo para verificar la página
hilo = threading.Thread(target=verificar_pag)
hilo.start()



# Encontrar el campo de búsqueda y escribir "Python"


#E_password_id.submit()# Enviar la búsqueda (presionar Enter)


# Esperar unos segundos para ver los resultados (puedes ajustar el tiempo)
#driver.implicitly_wait(30)


#sleep(15)
# Cerrar el navegador
#driver.quit()






while True:
    sleep(1)