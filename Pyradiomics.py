import csv
import tempfile
import SimpleITK as sitk
from radiomics import featureextractor
import os
from datetime import datetime
import numpy as np
from database import get_connection
import mysql.connector
import pandas as pd
from Ajout_fichier import upload_csv

def upload_csv_to_drive(csv_filepath, prenom_patient, nom_patient, niss_patient, id_irm):
    try:
        csv_url = upload_csv(nom_patient, prenom_patient, csv_filepath)
        sauver_fichier_csv_db(csv_url, niss_patient,id_irm) #On enregistre le fichier dans la base de données
        print("Le fichier a bien été sauvegardé dans la base de donnée si aucune erreur survenue")
    except Exception as e:
        print(f"Erreur lors de l'upload : {str(e)}")

def sauver_fichier_csv_db(chemin_csv, niss_patient, id_irm):
    conn = None
    cursor = None
    try:
        conn = get_connection()
        cursor = conn.cursor()
        # Utilisation du même nom de colonnes que dans le CREATE TABLE
        cursor.execute(
            "INSERT INTO Caracteristiques_IRM (Id_irm, NISS, Date_extraction, Chemin_csv) VALUES (%s, %s, NOW(), %s)",
            (
                id_irm,
                niss_patient,
                chemin_csv
            )
        )
        conn.commit()
    except mysql.connector.Error as e:
        print("Erreur technique",f"Erreur de base de données : {e}")
        if conn: conn.rollback()
    except Exception as e:
        print("Erreur inattendue",f"Erreur : {str(e)}")
        if conn: conn.rollback()
    finally:
        if cursor: cursor.close()
        if conn: conn.close()

def check_patient_has_4_irms(niss_patient):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT COUNT(*) 
            FROM Caracteristiques_IRM 
            WHERE NISS = %s 
            AND Statut_traitement = 'En attente'
        """, (niss_patient,))
        return cursor.fetchone()[0] >= 4
    except Exception as e:
        print(f"Erreur vérification 4 IRMs : {str(e)}")
        return False

# Fonction pour charger une image PNG et la convertir en SimpleITK
def load_png_as_sitk(image_path):
    image = sitk.ReadImage(image_path)
    return image

def get_caracteristics(image_path_jpeg,mask_path_jpeg,patient_info,id_irm,choix=1):
    niss_patient = patient_info["niss"]
    nom_patient = patient_info["nom"]
    prenom_patient = patient_info["prenom"]
    current_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    # Liste contenant les informations du patients, les chemins des images et masques :
    patient_data = [
        {"patient_id": niss_patient, "date": current_datetime,"image_path": image_path_jpeg,"mask_path": mask_path_jpeg},

    ]
    # Initialisation de l'extracteur avec les options pour les caractéristiques basées sur les ondelettes
    extractor = featureextractor.RadiomicsFeatureExtractor()
    # Ajouter les transformations par ondelettes à l'extracteur
    extractor.enableImageTypeByName('Wavelet')
    extractor.enableFeatureClassByName('shape2D')
    # Liste des caractéristiques à conserver issues de feature selection
    allowed_features = [
        "wavelet-HL_glcm_MaximumProbability",
        "original_shape2D_Elongation",
        "wavelet-LL_glszm_SizeZoneNonUniformity",
        "wavelet-HL_ngtdm_Coarseness",
        "wavelet-HL_glcm_JointEntropy",
        "original_shape2D_PixelSurface",
        "original_shape2D_Sphericity"
    ]
    # Créer une liste pour stocker les DataFrames de chaque patient
    all_features_df = []
    # Traitement de chaque patient
    for patient in patient_data:
        # Chargement de l'image et du masque
        image = load_png_as_sitk(patient["image_path"])
        if choix == 1:
            mask = load_png_as_sitk(patient["mask_path"])
        elif choix == 2:
            raw_mask = sitk.ReadImage(patient["mask_path"])
            arr = sitk.GetArrayFromImage(raw_mask).astype(np.uint8)
            bin_arr = (arr > 0).astype(np.uint8)  # any non-zero → 1
            mask = sitk.GetImageFromArray(bin_arr)
            mask.CopyInformation(raw_mask)
        else:
            # 3) isoler le(s) label(s) non‑zéro original(s) et ne prendre que le premier
            raw_mask = sitk.ReadImage(patient["mask_path"])
            arr = sitk.GetArrayFromImage(raw_mask).astype(np.uint8)
            # trouver tous les labels présents (sauf 0)
            labels = np.unique(arr)
            labels = labels[labels != 0]
            if labels.size == 0:
                raise ValueError("Aucun label non‑zéro trouvé dans le masque.")
            target_label = int(labels[0])
            # ne conserver que ce label → 1
            bin_arr = (arr == target_label).astype(np.uint8)
            mask = sitk.GetImageFromArray(bin_arr)
            mask.CopyInformation(raw_mask)
        # Vérification des dimensions
        assert image.GetSize() == mask.GetSize(), f"L'image et le masque pour le patient {patient['patient_id']} doivent avoir les mêmes dimensions."
        # Extraction des caractéristiques
        features = extractor.execute(image, mask)
        # Filtrer les caractéristiques avec les préfixes autorisés
        #allowed_prefixes = ("original_shape2D", "original_firstorder", "original_glcm", "original_glrlm", "original_glszm", "original_gldm", "original_ngtdm", "wavelet")
        filtered_features = {k: v for k, v in features.items() if k in allowed_features}
        # Ajouter les informations sur le patient et la date à chaque caractéristique
        #patient_features = pd.DataFrame(list(filtered_features.items()), columns=["Feature", "Value"])
        if not filtered_features:
            print("AUCUNE CARACTÉRISTIQUE EXTRACTIBLE - Vérifiez les images/masques.")
            return None

        try:
            patient_features = pd.DataFrame(
                list(filtered_features.items()),
                columns=["Feature", "Value"]
            )
        except Exception as e:
            print(f"Erreur création DataFrame : {str(e)}")
            return None
        patient_features["Patient_ID"] = patient["patient_id"]
        patient_features["Date_IRM"] = patient["date"]
        # Ajouter le DataFrame du patient à la liste
        all_features_df.append(patient_features)
    # Concaténer tous les DataFrames des patients en un seul DataFrame
    final_df = pd.concat(all_features_df, ignore_index=True)
    # Créer un dossier de sortie
    output_folder = tempfile.mktemp(prefix=f"Radiomics_caracteristiques_pyradiomics_{niss_patient}_")
    #output_folder = "/content/drive/MyDrive/Radiomics_caracteristiques_pyradiomics/241998"
    os.makedirs(output_folder, exist_ok=True)
    # Exporter les résultats sous forme de fichier CSV
    chemin_csv = os.path.join(output_folder, "caracteristiques_tous_les_patients.csv")
    final_df['Feature'] = final_df['Feature'].str.replace('[",\n]', '', regex=True)
    final_df['Value'] = final_df['Value'].astype(str).str.replace('[",\n]', '', regex=True)
    final_df.to_csv(chemin_csv, index=False, quoting=csv.QUOTE_NONNUMERIC)
    upload_csv_to_drive(chemin_csv, prenom_patient,nom_patient, niss_patient,id_irm)
    print(f"CSV des caractéristiques PyRadiomics enregistrées à cet endroit : {chemin_csv}")
    return chemin_csv
