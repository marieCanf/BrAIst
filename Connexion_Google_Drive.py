from pydrive2.auth import GoogleAuth
from pydrive2.drive import GoogleDrive
import os

def connecter_drive():
    if not os.path.exists('client_secrets.json'):
        raise FileNotFoundError("Placez le fichier client_secrets.json dans le dossier du projet!")

    gauth = GoogleAuth()

    # Charger la configuration client depuis le fichier client_secrets.json
    gauth.LoadClientConfigFile("client_secrets.json")

    # Si le flow n'est pas encore créé, l'initialiser
    if gauth.flow is None:
        gauth.GetFlow()

    # Forcer la demande d'un refresh token
    gauth.flow.params.update({'access_type': 'offline', 'approval_prompt': 'force'})
    gauth.settings['get_refresh_token'] = True

    if os.path.exists('credentials.json'):
        gauth.LoadCredentialsFile('credentials.json')
    else:
        gauth.CommandLineAuth()
        gauth.SaveCredentialsFile('credentials.json')

    if gauth.access_token_expired:
        gauth.Refresh()
        gauth.SaveCredentialsFile('credentials.json')

    drive = GoogleDrive(gauth)
    print("Authentification réussie !")
    return drive


connecter_drive()

