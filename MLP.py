import os
import re
import tempfile
import gdown
import torch
import numpy as np
import pandas as pd
from torch import nn
import joblib
from database import get_connection
# Définition des classes du modèle
# MLP Model
class MLP(nn.Module):
    def __init__(self, input_dim):
        super(MLP, self).__init__()
        self.fct1 = nn.Linear(input_dim, 64)
        self.fct2 = nn.Linear(64, 32)
        self.fct3 = nn.Linear(32, 1)
    def forward(self, x):
        x = torch.relu(self.fct1(x))
        x = torch.relu(self.fct2(x))
        x = torch.sigmoid(self.fct3(x))
        return x

class BaseModel(nn.Module):
    def __init__(self, model, loss_fn):
        super(BaseModel, self).__init__()
        self.model = model
        self.loss_fn = loss_fn

    def forward(self, x):
        return self.model(x)

# Chargement du modèle pré-entraîné
def load_pretrained_model(weights_path='Checkpoints/mlp_model_weights.pth',
                         input_dim_path='Checkpoints/input_dim.npy'):
    # Charger la dimension d'entrée
    input_dim = np.load(input_dim_path)
    # Créer le modèle
    model = BaseModel(MLP(input_dim=int(input_dim)), nn.BCELoss())
    # Charger les poids
    model.load_state_dict(torch.load(weights_path))
    model.eval()  # Mode évaluation
    return model

#agencement des données
def extraire_et_transposer_fichier(fichier_entree, fichier_sortie):
    """
    Extrait les deux premières colonnes d'un fichier CSV, les transpose,
    puis enregistre le résultat dans un nouveau fichier CSV.
    """
    try:
        df = pd.read_csv(fichier_entree, usecols=[0, 1], header=None, sep=",")
        df_transpose = df.transpose()
        df_transpose.to_csv(fichier_sortie, index=False, header=False)
        return fichier_sortie
    except Exception as e:
        raise RuntimeError(f"Erreur lors de l'extraction/transposition : {e}")

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
    #gdrive_links = self.check_patient_has_multiple_irms(niss_patient)
    """
    if not gdrive_links:
        print("Aucun fichier CSV trouvé pour ce patient.")
        return"""
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

def in_mlp(niss_patient):
    fichier_csv_path = check_patient_has_multiple_irms(niss_patient)
    if fichier_csv_path:
        print("Il y a assez de dates pour le MLP")
        fichier_entree = merge_all_csv(niss_patient, fichier_csv_path)
        print(fichier_entree)
        # Charger le modèle
        print("Le modèle est chargé")
        model = load_pretrained_model()
        print(model)
        # Exemple d'utilisation
        #fichier_entree = fichier_csv_path  #METTRE ICI L'URL DU FICHIER QUI SORT DE L'EXTRACTION PyRadiomics
        #fichier_sortie = "/content/mon_fichier_transpose.csv" #FICHIER AGENCE POUR RENTRER DANS LE MLP
        with tempfile.NamedTemporaryFile(suffix=".csv", delete=False) as tmp:
            fichier_sortie = tmp.name
        fichier_sortie = extraire_et_transposer_fichier(fichier_entree, fichier_sortie)
        print(fichier_sortie)
        #extraire_et_transposer_fichier(fichier_entree, fichier_sortie)
        # Charger les nouvelles données
        print("on charge les nouvelles données")
        input_path = fichier_sortie
        new_data = pd.read_csv(input_path)
        # Prétraitement identique à l'entraînement
        # 1. Supprimer les colonnes non features (comme ID si présent)
        print("on supprime les colonnes non features")
        if 'Feature' in new_data.columns:
            new_data = new_data.drop(columns=['Feature'])
        # 2. Normalisation (utiliser le même scaler que pendant l'entraînement)
        print("on normalise")
        # Charger le scaler sauvegardé
        scaler_path = 'Checkpoints/scaler.save'
        print("scaler_path")
        scaler = joblib.load(scaler_path)
        print("scaler chargé")
        #print("Colonnes de new_data :", new_data.columns)
        vals = new_data.values.reshape(1, -1) #NEW CHATGPT
        print(f"Shape avant normalization : {vals.shape}")
        print("après l'ajout de chat")
        #X_new_scaled = scaler.transform(new_data.values)  # Note: utilisez transform() pas fit_transform()
        X_new_scaled = scaler.transform(vals) #NEW CHATGPT
        print(f"Shape après normalization : {X_new_scaled.shape}")
        print("X_new_scaled")
        # Conversion en tensor
        print("conversion en tenseur")
        X_new_tensor = torch.tensor(X_new_scaled, dtype=torch.float32)
        # Faire la prédiction
        print("faire la prédiction")
        with torch.no_grad():
            print("dans le with")
            predictions = model(X_new_tensor)
            predicted_classes = (predictions > 0.5).int()
            print("à la fin du with")
        # Afficher les résultats
        print("avant l'affichage des résultats")
        for i, (proba, cls) in enumerate(zip(predictions, predicted_classes)):
            print(f"  Classe prédite: {cls.item()}")
            if cls.item() == 1 or cls.item() == "1":
                return "La patiente réagit positivement au traitement"
            else:
                return "La patiente ne réagit pas positivement au traitement"
    else:
        print("Il y a pas assez de dates pour le MLP")
        return "Pas assez de date pour avoir un résultat sur le traitement"