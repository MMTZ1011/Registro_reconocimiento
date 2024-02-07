import requests

# URL de inicio de sesión y credenciales
url = 'https://auth.wyze.com/login'  # Reemplaza con la URL de inicio de sesión de tu sitio
usuario = 'iLabTDI_Test01@proton.me'
contrasena = 'Zapopan201'

datos = {
    'username': usuario,
    'password': contrasena
}
response = requests.post(url, data=datos)

if response.status_code == 200:
    print('Inicio de sesión exitoso')
    print('text')
    print(response.text)
    print('json')
    print(response.json)
    print('content')
    print(response.content)
    print('cookies')
    print(response.cookies)

else:
    print('Error al iniciar sesión. Verifica las credenciales y la URL.')
###