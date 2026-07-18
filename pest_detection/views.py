from django.shortcuts import render
from django.conf import settings

import os
import numpy as np

from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
from tensorflow.keras.applications.efficientnet import preprocess_input

# ==========================================
# Load Pest Detection Model
# ==========================================

MODEL_PATH = os.path.join(
    settings.BASE_DIR,
    "pest_detection",
    "model",
    "pest_detection_efficientnetb0.keras"
)

model = load_model(MODEL_PATH)

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

    # ----------------------------------
    # Save Uploaded Image
    # ----------------------------------

    upload_dir = os.path.join(
        settings.MEDIA_ROOT,
        "pest_uploads"
    )

    os.makedirs(upload_dir, exist_ok=True)

    file_path = os.path.join(
        upload_dir,
        uploaded_file.name
    )

    with open(file_path, "wb+") as destination:

        for chunk in uploaded_file.chunks():

            destination.write(chunk)

    # ----------------------------------
    # Image Preprocessing
    # ----------------------------------

    img = image.load_img(
        file_path,
        target_size=(160, 160)
    )

    img_array = image.img_to_array(img)

    img_array = np.expand_dims(
        img_array,
        axis=0
    )

    img_array = preprocess_input(img_array)
        # ==========================================
    # Model Prediction
    # ==========================================

    prediction = model.predict(
        img_array,
        verbose=0
    )

    predicted_index = np.argmax(prediction)

    confidence = float(
        np.max(prediction) * 100
    )

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
                "uploaded_image":
                    settings.MEDIA_URL +
                    "pest_uploads/" +
                    uploaded_file.name
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

        "prediction": pest_name,

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

        "uploaded_image":
            settings.MEDIA_URL +
            "pest_uploads/" +
            uploaded_file.name

    }

    return render(
        request,
        "pest_detection/index.html",
        context
    )