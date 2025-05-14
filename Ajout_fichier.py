from Connexion_Google_Drive import connecter_drive
import os
import zipfile
import time

# Variable globale pour stocker le chemin du dossier à uploader
dossier_enregistre = None


def ajouter_dossier(dossier):
    global dossier_enregistre
    dossier_enregistre = dossier
    print(f"Dossier enregistré : {dossier}")

def zip_dossier(dossier_path, nom_archive, progress_callback=None):
    total_files = sum([len(files) for _, _, files in os.walk(dossier_path)])
    current_file = 0

    with zipfile.ZipFile(nom_archive, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, _, files in os.walk(dossier_path):
            for file in files:
                chemin_fichier = os.path.join(root, file)
                arcname = os.path.relpath(chemin_fichier, dossier_path)
                zipf.write(chemin_fichier, arcname)
                current_file += 1
                if progress_callback:
                    progress = int((current_file / total_files) * 100)
                    progress_callback(progress)
    return nom_archive

def upload_dossier_masques(nom_patient,prenom_patient,nom_archive):
    fichier_drive = None
    try:
        drive = connecter_drive()
        # 2. Créer et uploader le fichier
        fichier_drive = drive.CreateFile({
            'title': os.path.basename(nom_archive),
            'mimeType': 'application/zip'
        })
        fichier_drive.SetContentFile(nom_archive)  # Utiliser le contenu déjà lu
        fichier_drive.Upload()
        time.sleep(1)  # attente sécurisée

        # On  souhaite créer un URL partageable afin de l'enregistrer dans la abse de données :
        fichier_drive.InsertPermission({
            'type': 'anyone',
            'value': 'anyone',
            'role': 'reader'
        })
        url = fichier_drive["alternateLink"]

        print(url)
        return url

    except Exception as e:
        print(f"Erreur lors de l'upload : {str(e)}")
        raise
    finally:
        if fichier_drive:
            fichier_drive.content.close()
            del fichier_drive
        # 4. Supprimer le fichier seulement si tout est fermé
        if os.path.exists(nom_archive):
            time.sleep(1)
            try:
                os.remove(nom_archive)
                print(f"Fichier temporaire {nom_archive} supprimé")
            except PermissionError as pe:
                print(f"Impossible de supprimer le fichier : {str(pe)}")
                time.sleep(2)
                try:
                    os.remove(nom_archive)
                except Exception as e:
                    print(f"Echcec définitif : {str(e)}")

def upload_dossier(nom_patient, prenom_patient, nom_archive):
    fichier_drive = None
    try:
        drive = connecter_drive()
        # 2. Créer et uploader le fichier
        fichier_drive = drive.CreateFile({
            'title': os.path.basename(nom_archive),
            'mimeType': 'application/zip'
        })
        fichier_drive.SetContentFile(nom_archive)  # Utiliser le contenu déjà lu
        fichier_drive.Upload()
        time.sleep(1) #attente sécurisée
        #On  souhaite créer un URL partageable afin de l'enregistrer dans la abse de données :
        fichier_drive.InsertPermission({
            'type': 'anyone',
            'value': 'anyone',
            'role': 'reader'
        })
        url = fichier_drive["alternateLink"]
        print(url)
        return url

    except Exception as e:
        print(f"Erreur lors de l'upload : {str(e)}")
        raise
    finally:
        if fichier_drive:
            fichier_drive.content.close()
            del fichier_drive
        # 4. Supprimer le fichier seulement si tout est fermé
        if os.path.exists(nom_archive):
            time.sleep(1)
            try:
                os.remove(nom_archive)
                print(f"Fichier temporaire {nom_archive} supprimé")
            except PermissionError as pe:
                print(f"Impossible de supprimer le fichier : {str(pe)}")
                time.sleep(2)
                try :
                    os.remove(nom_archive)
                except Exception as e :
                    print(f"Echcec définitif : {str(e)}")


def upload_csv(nom_patient, prenom_patient, csv_path):
    fichier_drive = None
    try:
        drive = connecter_drive()
        # Create a parent folder in Drive (optional)
        dossier_parent = drive.CreateFile({
            'title': f"Radiomics_{nom_patient}_{prenom_patient}",
            'mimeType': 'application/vnd.google-apps.folder',
            'parents': [{'id': 'root'}]
        })
        dossier_parent.Upload()

        # Upload the CSV directly
        fichier_drive = drive.CreateFile({
            'title': os.path.basename(csv_path),
            'parents': [{'id': dossier_parent['id']}],  # Place inside the parent folder
            'mimeType': 'text/csv'
        })
        fichier_drive.SetContentFile(csv_path)
        fichier_drive.Upload()

        # Set shareable permissions
        fichier_drive.InsertPermission({
            'type': 'anyone',
            'value': 'anyone',
            'role': 'reader'
        })
        url = fichier_drive["alternateLink"]
        print(f"CSV uploaded to Google Drive: {url}")
        return url

    except Exception as e:
        print(f"Upload failed: {str(e)}")
        raise
    finally:
        if fichier_drive:
            fichier_drive.content.close()
            del fichier_drive