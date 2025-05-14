from segment_anything import SamPredictor, sam_model_registry
import torch
import pydicom
import os
import cv2
import numpy as np
import supervision as sv
import tempfile
from Modèles_IA import Pyradiomics

def select_roi(image_path):
    # Vérifier que le fichier existe et charger l'image
    if not os.path.exists(image_path):
        raise FileNotFoundError(f"Fichier introuvable : {image_path}")
    image = cv2.imread(image_path)
    if image is None:
        raise ValueError(f"Échec du chargement de l'image : {image_path}")
    # Redimensionner si trop large
    max_width = 800
    h, w = image.shape[:2]
    scale = max_width / w if w > max_width else 1.0
    resized = cv2.resize(image, (int(w * scale), int(h * scale)))
    # Utiliser selectROI directement (création interne de la fenêtre)
    # Cela évite les erreurs liées à setMouseCallback sur une fenêtre non initialisée
    roi = cv2.selectROI(resized, showCrosshair=True, fromCenter=False)
    cv2.destroyAllWindows()
    # Si pas de sélection
    if roi == (0, 0, 0, 0):
        return None
    x, y, w_roi, h_roi = roi
    # Recalibrer aux dimensions originales
    return [
        int(x / scale),
        int(y / scale),
        int((x + w_roi) / scale),
        int((y + h_roi) / scale)
    ]

def dicom_to_jpeg(dicom_path, windowed=True):
    # Création d'un fichier temporaire avec extension .jpeg
    temp_file = tempfile.NamedTemporaryFile(suffix='.jpeg', delete=False)
    output_path = temp_file.name
    temp_file.close()  # Fermeture immédiate pour libérer le handle
    ds = pydicom.dcmread(dicom_path)
    pixel_array = ds.pixel_array.astype(np.float32)
    if windowed and ('WindowWidth' in ds and 'WindowCenter' in ds):
        center = ds.WindowCenter
        width = ds.WindowWidth
        # Gestion des valeurs multiples (ex: fenêtrage double)
        if isinstance(center, pydicom.multival.MultiValue):
            center = center[0]
        if isinstance(width, pydicom.multival.MultiValue):
            width = width[0]
        min_val = center - width / 2
        max_val = center + width / 2
        pixel_array = np.clip(pixel_array, min_val, max_val)
    else:
        min_val = np.min(pixel_array)
        max_val = np.max(pixel_array)
    # Normalisation et conversion en JPEG
    pixel_array = (pixel_array - min_val) / (max_val - min_val) * 255.0
    pixel_array = pixel_array.astype(np.uint8)
    cv2.imwrite(output_path, pixel_array)
    if not os.path.exists(output_path):
        raise RuntimeError("La conversion DICOM -> JPEG a échoué")
    return output_path

def save_dicom_to_jpeg(dicom_folder,patient_niss, id_irm):
    dcm_files = sorted([
        f for f in os.listdir(dicom_folder)
        if f.lower().endswith(".dcm")
    ])
    dicom_path = os.path.join(dicom_folder, dcm_files[0])
    output_path = dicom_to_jpeg(dicom_path)
    print("OUTPUT PATH DONE ✅", output_path)
    selected_box = select_roi(output_path)
    default_box = [68, 247, 68+555, 247+678]
    box = np.array(selected_box if selected_box else default_box)
    print("Coordonnées de la boîte:", box)
    image_bgr = cv2.imread(output_path)
    image_rgb = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2RGB)
    CHECKPOINT_PATH = "checkpoints/sam_vit_b_01ec64.pth"
    MODEL_TYPE = "vit_b"
    # Charger le modèle
    sam = sam_model_registry[MODEL_TYPE](checkpoint=CHECKPOINT_PATH)
    sam.to(device="cuda" if torch.cuda.is_available() else "cpu")
    print("✅ SAM chargé avec succès !")
    mask_predictor = SamPredictor(sam)
    mask_predictor.set_image(image_rgb)
    masks, scores, logits = mask_predictor.predict(
        box=box,
        multimask_output=True
    )
    box_annotator = sv.BoxAnnotator(color=sv.Color.RED, color_lookup=sv.ColorLookup.INDEX)
    mask_annotator = sv.MaskAnnotator(color=sv.Color.RED, color_lookup=sv.ColorLookup.INDEX)
    detections = sv.Detections(
        xyxy=sv.mask_to_xyxy(masks=masks),
        mask=masks
    )
    detections = detections[detections.area == np.max(detections.area)]
    source_image = box_annotator.annotate(scene=image_bgr.copy(), detections=detections)
    segmented_image = mask_annotator.annotate(scene=image_bgr.copy(), detections=detections)
    sv.plot_images_grid(
        images=[source_image, segmented_image],
        grid_size=(1, 2),
        titles=['source image', 'segmented image']
    )
    sv.plot_images_grid(
        images=masks,
        grid_size=(1, 4),
        size=(16, 4)
    )
    cv2.imwrite("segmented_image.jpg", segmented_image)
    largest_mask = detections.mask[0].astype(np.uint8) * 255
    tmp_dir = tempfile.mkdtemp(prefix="masks_")
    mask_path = os.path.join(tmp_dir, "largest_mask.png")
    cv2.imwrite(mask_path, largest_mask)
    print("Masque écrit dans:", mask_path)
    cv2.imwrite("largest_mask.png", largest_mask)
    chemin_csv = Pyradiomics.get_caracteristics(output_path,mask_path,patient_niss,id_irm, choix=2)
    if os.path.exists(output_path):
        os.remove(output_path)
        print("OUTPUT PATH REMOVED 💥")
    return largest_mask