import os
import uuid
import numpy as np
from PIL import Image

from django.shortcuts import render
from django.conf import settings

# Global variable for model caching
_PEST_MODEL = None

# ==========================================
# Lazy Model Loader (RAM Memory Optimization)
# ==========================================
def get_pest_model():
    global _PEST_MODEL
    if _PEST_MODEL is None:
        from tensorflow.keras.models import load_model
        
        model_path = os.path.join(
            settings.BASE_DIR,
            "pest_detection",
            "model",
            "pest_detection_efficientnetb0.keras"
        )
        _PEST_MODEL = load_model(model_path)
    return _PEST_MODEL

# ==========================================
# Confidence Threshold
# ==========================================
CONFIDENCE_THRESHOLD = 80.0

# ==========================================
# Pest Classes
# ==========================================
class_names = [
    "aphids",
    "armyworm",
    "beetle",
    "bollworm",
    "grasshopper",
    "mites",
    "mosquito",
    "sawfly",
    "stem_borer"
]

# ==========================================
# Pest Information
# ==========================================
pest_info = {
    "aphids": {
        "scientific_name": "Aphidoidea",
        "description": "Small sap-sucking insects that weaken plants by feeding on plant sap.",
        "pesticide": "Imidacloprid 17.8 SL",
        "control": "Spray Imidacloprid or Neem Oil. Avoid excessive nitrogen fertilizer."
    },
    "armyworm": {
        "scientific_name": "Spodoptera frugiperda",
        "description": "Armyworms feed on leaves and stems causing severe crop damage.",
        "pesticide": "Chlorantraniliprole 18.5 SC",
        "control": "Use pheromone traps and spray Chlorantraniliprole."
    },
    "beetle": {
        "scientific_name": "Coleoptera",
        "description": "Leaf-feeding beetles reduce plant growth by damaging foliage.",
        "pesticide": "Carbaryl 50 WP",
        "control": "Manual collection and Carbaryl spray."
    },
    "bollworm": {
        "scientific_name": "Helicoverpa armigera",
        "description": "Attacks cotton, tomato and vegetable crops.",
        "pesticide": "Emamectin Benzoate 5 SG",
        "control": "Install pheromone traps and spray Emamectin Benzoate."
    },
    "grasshopper": {
        "scientific_name": "Caelifera",
        "description": "Grasshoppers feed on crop leaves and young shoots.",
        "pesticide": "Malathion 50 EC",
        "control": "Use Malathion spray during early infestation."
    },
    "mites": {
        "scientific_name": "Tetranychidae",
        "description": "Tiny pests causing yellow spots and leaf drying.",
        "pesticide": "Abamectin 1.9 EC",
        "control": "Maintain field humidity and spray Abamectin."
    },
    "mosquito": {
        "scientific_name": "Culicidae",
        "description": "Mosquitoes breed near stagnant water around farms.",
        "pesticide": "Pyrethrin",
        "control": "Remove stagnant water and maintain sanitation."
    },
    "sawfly": {
        "scientific_name": "Symphyta",
        "description": "Larvae consume leaves rapidly causing defoliation.",
        "pesticide": "Spinosad 45 SC",
        "control": "Spray Spinosad and monitor infestation regularly."
    },
    "stem_borer": {
        "scientific_name": "Scirpophaga incertulas",
        "description": "Stem borers bore into stems causing dead heart and white ear symptoms.",
        "pesticide": "Cartap Hydrochloride 4G",
        "control": "Apply Cartap Hydrochloride granules at the recommended dose."
    }
}

# ==========================================
# Home Page
# ==========================================
def pest_home(request):
    return render(
        request,
        "pest_detection/index.html"
    )

# ==========================================
# Pest Prediction
# ==========================================
def predict_pest(request):
    if request.method != "POST":
        return render(
            request,
            "pest_detection/index.html"
        )

    # ----------------------------------
    # Check Uploaded Image
    # ----------------------------------
    if "image" not in request.FILES:
        return render(
            request,
            "pest_detection/index.html",
            {
                "error": "Please upload an image."
            }
        )

    uploaded_file = request.FILES["image"]

    try:
        # ----------------------------------
        # Save & Compress Uploaded Image
        # ----------------------------------
        upload_dir = os.path.join(
            settings.MEDIA_ROOT,
            "pest_uploads"
        )
        os.makedirs(upload_dir, exist_ok=True)

        # Generating unique file name to avoid overwrite conflict
        ext = os.path.splitext(uploaded_file.name)[1].lower() or ".jpg"
        unique_filename = f"{uuid.uuid4().hex}{ext}"
        file_path = os.path.join(upload_dir, unique_filename)

        # Image Compression / Resizing using PIL
        img_pil = Image.open(uploaded_file)
        if img_pil.mode in ("RGBA", "P"):
            img_pil = img_pil.convert("RGB")
            
        img_pil_resized = img_pil.resize((160, 160))
        img_pil_resized.save(file_path, "JPEG", optimize=True, quality=80)

        # ----------------------------------
        # Preprocessing Direct from Memory
        # ----------------------------------
        from tensorflow.keras.applications.efficientnet import preprocess_input

        # Direct converting resized PIL image to numpy array
        img_array = np.array(img_pil_resized, dtype=np.float32)
        img_array = np.expand_dims(img_array, axis=0)
        img_array = preprocess_input(img_array)

        # ==========================================
        # Model Prediction
        # ==========================================
        model = get_pest_model()
        prediction = model.predict(
            img_array,
            verbose=0
        )

        predicted_index = np.argmax(prediction)
        confidence = float(
            np.max(prediction) * 100
        )

        image_relative_url = f"{settings.MEDIA_URL}pest_uploads/{unique_filename}"

        # ==========================================
        # Confidence Threshold
        # ==========================================
        if confidence < CONFIDENCE_THRESHOLD:
            return render(
                request,
                "pest_detection/index.html",
                {
                    "error": "❌ This is not a pest.",
                    "confidence": round(confidence, 2),
                    "uploaded_image": image_relative_url
                }
            )

        # ==========================================
        # Pest Details
        # ==========================================
        pest_name = class_names[predicted_index]
        info = pest_info.get(
            pest_name,
            {}
        )

        # ==========================================
        # Result Context
        # ==========================================
        context = {
            "prediction": pest_name.replace("_", " ").title(),
            "confidence": round(confidence, 2),
            "scientific_name": info.get(
                "scientific_name",
                "Not Available"
            ),
            "description": info.get(
                "description",
                "Not Available"
            ),
            "pesticide": info.get(
                "pesticide",
                "Not Available"
            ),
            "control": info.get(
                "control",
                "Not Available"
            ),
            "uploaded_image": image_relative_url
        }

        return render(
            request,
            "pest_detection/index.html",
            context
        )

    except Exception as e:
        return render(
            request,
            "pest_detection/index.html",
            {
                "error": "Invalid or corrupted image file uploaded."
            }
        )