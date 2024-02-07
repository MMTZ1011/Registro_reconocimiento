from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import os

# La ruta al archivo que descargaste
CREDENTIALS_FILE = 'Credenciales\DriveGoogleApi.json'

# Scopes de la API que vas a usar
SCOPES = ['https://www.googleapis.com/auth/drive']

creds = None

# El archivo token.json guarda los tokens de acceso y de refresco, y se crea
# automáticamente cuando el flujo de autorización se completa por primera vez
if os.path.exists('token.json'):
    creds = Credentials.from_authorized_user_file('token.json', SCOPES)
###


# Si no hay credenciales válidas disponibles, deja que el usuario se loguee.
if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())
    else:
        flow = InstalledAppFlow.from_client_secrets_file(
            CREDENTIALS_FILE, SCOPES)
        creds = flow.run_local_server(port=0)

    # Guarda las credenciales para la próxima corrida
    with open('token.json', 'w') as token:
        token.write(creds.to_json())
