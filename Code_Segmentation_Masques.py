from segment_anything import sam_model_registry, SamAutomaticMaskGenerator
import torch
import pydicom
from PIL import Image
import os
import cv2
import numpy as np
import supervision as sv
import tempfile
from pathlib import Path
from Modèles_IA import Pyradiomics
from Ajout_fichier import upload_csv


def get_mask_contrast(mask, image):
    region_pixels = image[mask.astype(bool)]
    if region_pixels.size == 0:
        return 0
    return np.std(region_pixels)

def mask_above_y_threshold(mask, y_threshold):
    ys, xs = np.where(mask)
    if len(ys) == 0:
        return False
    return np.mean(ys < y_threshold) > 0.8

def mask_size(mask):
    mask = mask.astype(bool)
    return np.count_nonzero(mask)


def mask_generation(jpeg_folder):
    CHECKPOINT_PATH = "checkpoints/sam_vit_b_01ec64.pth"
    MODEL_TYPE = "vit_b"
    # Charger le modèle
    sam = sam_model_registry[MODEL_TYPE](checkpoint=CHECKPOINT_PATH)
    sam.to(device="cuda" if torch.cuda.is_available() else "cpu")
    print("✅ SAM chargé avec succès !")
    mask_generator = SamAutomaticMaskGenerator(sam)
    patient_folder = os.path.basename(jpeg_folder)
    IMAGE_DIR = jpeg_folder
    SAVE_DIR = tempfile.mkdtemp(prefix="masques_")
    os.makedirs(SAVE_DIR, exist_ok=True)
    y_threshold = 200
    image_files = sorted([f for f in os.listdir(IMAGE_DIR) if f.endswith(('.jpg', '.jpeg', '.png'))])
    saved_masks_info = []
    for image_name in image_files:
        image_path = os.path.join(IMAGE_DIR, image_name)
        image_bgr = cv2.imread(image_path)
        if image_bgr is None:
            print(f"Erreur de lecture de {image_path}")
            continue
        image_rgb = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2RGB)
        sam_result = mask_generator.generate(image_rgb)
        mask_annotator = sv.MaskAnnotator(color_lookup=sv.ColorLookup.INDEX)
        detections = sv.Detections.from_sam(sam_result=sam_result)
        annotated_image = mask_annotator.annotate(scene=image_bgr.copy(), detections=detections)
        filtered_masks = [m for m in sam_result if mask_above_y_threshold(m["segmentation"], y_threshold)]
        if not filtered_masks:
            filtered_masks = sam_result
        for m in filtered_masks:
            contrast = get_mask_contrast(m["segmentation"], image_rgb)
            masked_image = image_rgb.copy()
            masked_image[~m["segmentation"]] = 0
            size = mask_size(m["segmentation"])
            saved_masks_info.append({
                "image_name": image_name,
                "size": size,
                "contrast": contrast,
                "masked_image": masked_image
            })
    filtered_masks = [m for m in saved_masks_info if m["size"] < 9000]
    top_30_largest = sorted(filtered_masks, key=lambda x: x["size"], reverse=True)[:30]
    top_5 = sorted(top_30_largest, key=lambda x: x["contrast"], reverse=True)[:5]
    top = sorted(top_5, key=lambda x: x["contrast"], reverse=True)[:1]
    for i, info in enumerate(top):
        filename = f"{i + 1:02d}_{info['image_name']}"
        print("Fichier du masque s'appelle : ", filename)
        print("L'image associée s'appelle :", info["image_name"])
        save_path = os.path.join(SAVE_DIR, filename)
        img_bgr = cv2.cvtColor(info["masked_image"], cv2.COLOR_RGB2BGR)
        cv2.imwrite(save_path, img_bgr)
        return SAVE_DIR, info['image_name'], filename

def dicom_to_jpeg(dicom_path, jpeg_path):
    dicom = pydicom.dcmread(dicom_path)
    # Extraire les données de pixels
    pixel_array = dicom.pixel_array.astype(float)
    # Normalisation entre 0 et 255 pour l'affichage
    pixel_array = (np.maximum(pixel_array, 0) / pixel_array.max()) * 255.0
    pixel_array = np.uint8(pixel_array)
    # Étape 1 : Débruitage (filtre Gaussien)
    denoised = cv2.GaussianBlur(pixel_array, (5, 5), 0)
    # Étape 2 : Redimensionnement à 224x224
    resized = cv2.resize(denoised, (224, 224))
    # Étape 3 : Normalisation [0,1]
    scaled = resized / 255.0
    preprocessed_image = Image.fromarray((scaled * 255).astype(np.uint8))
    directory = os.path.dirname(jpeg_path)
    if not os.path.exists(directory):
        os.makedirs(directory)
    preprocessed_path = jpeg_path.replace('.jpg', '_pretraitee.jpg')
    preprocessed_image.save(preprocessed_path, 'JPEG')
    #image.save(jpeg_path, 'JPEG')
    print(f"Sauvegardé : {jpeg_path}")

def save_dicom_to_jpeg(dicom_folder_path, patient_info, url):
    jpeg_folder = tempfile.mktemp(prefix="jpeg_")
    # Filtrer et trier les fichiers DICOM
    dicom_files = sorted([
        f for f in os.listdir(dicom_folder_path)
        if f.lower().endswith(".dcm")
    ])
    taille = len(dicom_files)
    milieu = taille // 2  # Milieu 1-based
    start = max(1, milieu - 15)
    end = min(taille, milieu + 15)

    for i, filename in enumerate(dicom_files, 1):  # Index 1-based
        if start <= i <= end:
            dicom_path = os.path.join(dicom_folder_path, filename)
            jpeg_path = os.path.join(jpeg_folder, filename.replace(".dcm", ".jpeg"))
            dicom_to_jpeg(dicom_path, jpeg_path)
    print("✅ Les images sont sauvegardées !")
    mask_folder, name_image, nom_masque = mask_generation(jpeg_folder)
    print("✅ Les masques sont générés !")
    jpeg_dir = Path(jpeg_folder)  # convert string → Path
    for jpg in jpeg_dir.glob("*.jpeg"):
        if jpg.name != name_image:
            print(f"💥 Supprimé l'image temporaire JPEG: {jpg.name}")
            jpg.unlink()
    print(f"image lien : {jpeg_dir}\\{name_image}")
    print(f"Masque lien : {mask_folder}\\{nom_masque}")
    chemin_vers_image_jpeg = f"{jpeg_dir}\\{name_image}"
    chemin_vers_masque_jpeg = f"{mask_folder}\\{nom_masque}"
    chemin_csv = Pyradiomics.get_caracteristics(chemin_vers_image_jpeg,chemin_vers_masque_jpeg,patient_info, url)#Avoir les caractéristiques Pyradiomics de l'IRM
    upload_url = upload_csv("Patient_FirstName", "Patient_LastName", chemin_csv)
    print(f"CSV accessible at: {upload_url}")
    return mask_folder
