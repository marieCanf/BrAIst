import mysql
from openai import OpenAI
from database import get_connection
import re, os, gdown
import pandas as pd


client = OpenAI(
 api_key="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")
APP_PROFILE = """
Tu es l'assistant virtuel d'un médecin spécialisé dans le traitement des cancers du sein.
Ta mission est d’aider ce médecin à interpréter les résultats extraits d’IRM, en répondant à ses questions concernant le suivi de ses patientes et les données disponibles.
 
Informations générales : 
- **Localisation** : Belgique
- **Langue de communication** : Français

Processus : 
Le médecin utilise une application dans laquelle il charge les IRM des patientes.
Chaque IRM est segmentée afin d’obtenir un masque de la tumeur, puis un traitement est appliqué pour extraire des caractéristiques radiomiques à l’aide de la librairie radiomics. Les caractéristiques suivantes sont extraites pour chaque IRM : 
- wavelet-HL_glcm_MaximumProbability ;
- original_shape2D_Elongation ;
- wavelet-LL_glszm_SizeZoneNonUniformity ;
- wavelet-HL_ngtdm_Coarseness ;
- wavelet-HL_glcm_JointEntropy ;
- original_shape2D_PixelSurface ;
- original_shape2D_Sphericity.
 
Dès que quatre IRM ont été enregistrées à des dates différentes pour une patiente, les caractéristiques extraites sont utilisées comme entrée d’un réseau de neurones MultiLayer Perceptron (MLP). Ce modèle prédit la réponse au traitement selon deux classes : 
- 0 si la patiente réagit négativement au traitement ;
- 1 si la patiente réagit positivement au traitement.

Informations fournies à l'IA: 
Tu recevras : 
- Un fichier .csv contenant les caractéristiques radiomiques extraites pour les 4 IRM successives, ou le message "Aucun fichier .csv" si quatre IRM n'ont pas encore été enregistré.
- La prédiction du modèle MLP (0 ou 1), ou -1 si quatre IRM n'ont pas encore été enregistré.
 
Instruction : 
- Baser strictement tes réponses sur les données contenues dans le fichier CSV et la prédiction du MLP.
- Fournir des réponses claires, précises et factuelles.
- Si les données ne permettent pas de tirer une conclusion, indiquer clairement qu’une interprétation clinique reste nécessaire, et inviter le médecin à consulter directement les IRM.

"""


def check_patient_has_multiple_irms(niss_patient):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT Chemin_csv 
            FROM Caracteristiques_IRM 
            WHERE NISS = %s 
        """, (niss_patient,))
        rows = cursor.fetchall()
        liste = [row[0] for row in rows]
        if len(liste) >= 4:
            print("Il y a 4 IRM c'est bon")
            return liste[-4:] #On prend les 4 derniers url
        else:
            return False
    except Exception as e:
        print(f"Erreur vérification IRMs : {str(e)}")
        return False
def get_direct_download_url(gdrive_url):  # Extraction des ID de fichier Google Drive et construction d'une URL de téléchargement directe
    match = re.search(r"/d/([\w-]+)", gdrive_url)
    if not match:
        raise ValueError(f"Impossible d'extraire l'ID depuis: {gdrive_url}")
    file_id = match.group(1)
    return f"https://drive.google.com/uc?export=download&id={file_id}"

def cleanup_temp(dir_path):
    for f in os.listdir(dir_path):
        os.remove(os.path.join(dir_path, f))
    os.rmdir(dir_path)

def merge_all_csv(niss_patient, gdrive_links):
    download_dir = 'temp_csvs'
    os.makedirs(download_dir, exist_ok=True)
    dataframes = []
    downloaded_paths = []
    for idx, url in enumerate(gdrive_links, start=1):
        try:
            direct_url = get_direct_download_url(url)
            output_path = os.path.join(download_dir, f"file_{idx}.csv")
            print(f"Téléchargement de {url} -> {output_path}")
            gdown.download(direct_url, output_path, quiet=False)
            df = pd.read_csv(output_path)
            dataframes.append(df)
            downloaded_paths.append(output_path)
        except Exception as e:
            print(f"Erreur lors du traitement de {url}: {e}")
    # Choisir le fichier à traiter (fusionné ou unique)
    if len(dataframes) > 1:
        merged_df = pd.concat(dataframes, axis=0, ignore_index=True, sort=False)
        output_file = 'merged_output.csv'
        merged_df.to_csv(output_file, index=False)
        file_to_process = output_file
        print(f"Fichier FUSIONE enregistré sous: {output_file}")
    else:
        file_to_process = downloaded_paths[0]
        print(f"Un seul fichier trouvé, utilisation de : {file_to_process}")
    # Génération des graphiques
    file_to_process = file_to_process
    # Nettoyage
    cleanup_temp(download_dir)
    return file_to_process

def getDataPatient(NISS):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT Résultat_Suivi FROM Patient WHERE NISS = %s",(NISS,))
        row = cursor.fetchone()
        resultat_suivi = row[0]
        cursor.close()
        conn.close()
        return f"Prédiction du modèle : {resultat_suivi}"
    except mysql.connector.Error as e:
        print("Erreur DB",f"Erreur lors du chargement du résultat suivi pour le patient : {e}")

def generate_faculty_response(question: str,NISS):
    fichier_csv_path = check_patient_has_multiple_irms(NISS)
    patient_info_MLP = getDataPatient(NISS)
    if fichier_csv_path:
        fichier_entree = merge_all_csv(NISS, fichier_csv_path)
        with open(fichier_entree, 'r', encoding='utf-8') as f:
            csv_text = f.read()
        context = (
            f"{APP_PROFILE}\n\n"
            "Voici les données extraites (CSV) :\n"
            f"{csv_text}\n\n"
            f"{patient_info_MLP}"
        )
    else:
        context = f"{APP_PROFILE}\n\nAucun fichier .csv\n\n{patient_info_MLP}"
    # Construction du contexte
    completion = client.chat.completions.create(
    model="gpt-4o",
    messages=[
        {"role": "system", "content": APP_PROFILE},
        {"role": "system", "content": "Données IRM (CSV) :\n" + csv_text},
        {"role": "system", "content": patient_info_MLP},
        {"role": "user", "content": question},
    ],)
    return completion.choices[0].message.content
