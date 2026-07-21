from django.shortcuts import render
from django.conf import settings
import os
import numpy as np
from PIL import Image

# Global variable for model caching
_WEED_MODEL = None

# ==========================================
# Lazy Model Loader
# ==========================================
def get_weed_model():
    global _WEED_MODEL
    if _WEED_MODEL is None:
        from tensorflow.keras.models import load_model
        
        model_path = os.path.join(
            settings.BASE_DIR,
            "weed_detection",
            "model",
            "weed_identification_efficientnetb0.keras"
        )
        _WEED_MODEL = load_model(model_path)
    return _WEED_MODEL

# ==========================================
# Weed Classes
# ==========================================
class_names = [
    "Black-grass",
    "Charlock",
    "Cleavers",
    "Common Chickweed",
    "Common wheat",
    "Fat Hen",
    "Loose Silky-bent",
    "Maize",
    "Scentless Mayweed",
    "Shepherds Purse",
    "Small-flowered Cranesbill",
    "Sugar beet"
]

# ==========================================
# Confidence Threshold
# ==========================================
CONFIDENCE_THRESHOLD = 80.0

# ==========================================
# Weed Information
# ==========================================
weed_info = {
    "Black-grass": {
        "scientific_name": "Alopecurus myosuroides",
        "description": "A grassy weed commonly found in cereal fields.",
        "control": "Use selective herbicides and crop rotation."
    },
    "Charlock": {
        "scientific_name": "Sinapis arvensis",
        "description": "Yellow flowering broadleaf weed.",
        "control": "Mechanical removal and herbicide application."
    },
    "Cleavers": {
        "scientific_name": "Galium aparine",
        "description": "Sticky climbing weed.",
        "control": "Early cultivation and selective herbicides."
    },
    "Common Chickweed": {
        "scientific_name": "Stellaria media",
        "description": "Fast growing winter annual weed.",
        "control": "Mulching and broadleaf herbicides."
    },
    "Common wheat": {
        "scientific_name": "Triticum aestivum",
        "description": "This is a crop plant, not a weed.",
        "control": "No weed control required."
    },
    "Fat Hen": {
        "scientific_name": "Chenopodium album",
        "description": "Broadleaf annual weed commonly found in fields.",
        "control": "Manual removal before flowering."
    },
    "Loose Silky-bent": {
        "scientific_name": "Apera spica-venti",
        "description": "Grass weed commonly found in wheat fields.",
        "control": "Apply recommended selective herbicides."
    },
    "Maize": {
        "scientific_name": "Zea mays",
        "description": "This is a crop plant, not a weed.",
        "control": "No weed control required."
    },
    "Scentless Mayweed": {
        "scientific_name": "Tripleurospermum inodorum",
        "description": "Annual flowering weed.",
        "control": "Hand weeding and herbicide application."
    },
    "Shepherds Purse": {
        "scientific_name": "Capsella bursa-pastoris",
        "description": "Common annual broadleaf weed.",
        "control": "Mechanical removal before seed formation."
    },
    "Small-flowered Cranesbill": {
        "scientific_name": "Geranium pusillum",
        "description": "Broadleaf weed found in cultivated land.",
        "control": "Use selective herbicides."
    },
    "Sugar beet": {
        "scientific_name": "Beta vulgaris",
        "description": "This is a crop plant, not a weed.",
        "control": "No weed control required."
    }
}

# ==========================================
# Home Page
# ==========================================
def weed_home(request):
    return render(
        request,
        "weed_detection/index.html"
    )

# ==========================================
# Weed Prediction
# ==========================================
def predict_weed(request):
    if request.method != "POST":
        return render(
            request,
            "weed_detection/index.html"
        )

    # -----------------------------
    # Check Uploaded Image
    # -----------------------------
    if "image" not in request.FILES:
        return render(
            request,
            "weed_detection/index.html",
            {
                "error": "Please upload an image."
            }
        )

    uploaded_file = request.FILES["image"]

    # -----------------------------
    # Save & Compress Uploaded Image
    # -----------------------------
    upload_dir = os.path.join(
        settings.MEDIA_ROOT,
        "weed_uploads"
    )
    os.makedirs(upload_dir, exist_ok=True)

    file_path = os.path.join(
        upload_dir,
        uploaded_file.name
    )

    # Fast processing ke liye image size resize & compress karke save kar rahe hain
    img_pil = Image.open(uploaded_file)
    if img_pil.mode in ("RGBA", "P"):
        img_pil = img_pil.convert("RGB")
    
    img_pil_resized = img_pil.resize((224, 224))
    img_pil_resized.save(file_path, "JPEG", optimize=True, quality=80)

    # -----------------------------
    # Lazy Imports for TensorFlow
    # -----------------------------
    from tensorflow.keras.preprocessing import image
    from tensorflow.keras.applications.efficientnet import preprocess_input

    # -----------------------------
    # Image Preprocessing
    # -----------------------------
    img = image.load_img(
        file_path,
        target_size=(224, 224)
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
    model = get_weed_model()
    prediction = model.predict(
        img_array,
        verbose=0
    )

    predicted_index = np.argmax(prediction)
    confidence = float(
        np.max(prediction) * 100
    )

    # Relative path for front-end rendering
    image_relative_url = settings.MEDIA_URL + "weed_uploads/" + uploaded_file.name

    # ==========================================
    # Confidence Threshold
    # ==========================================
    if confidence < CONFIDENCE_THRESHOLD:
        return render(
            request,
            "weed_detection/index.html",
            {
                "error": "❌ This is not a weed.",
                "confidence": round(confidence, 2),
                "uploaded_image": image_relative_url
            }
        )

    # ==========================================
    # Get Weed Details
    # ==========================================
    weed_name = class_names[predicted_index]
    info = weed_info.get(
        weed_name,
        {}
    )

    # ==========================================
    # Result Context
    # ==========================================
    context = {
        "prediction": weed_name,
        "confidence": round(confidence, 2),
        "scientific_name": info.get(
            "scientific_name",
            "Not Available"
        ),
        "description": info.get(
            "description",
            "Not Available"
        ),
        "control_method": [
            info.get(
                "control",
                "Not Available"
            )
        ],
        "uploaded_image": image_relative_url
    }

    return render(
        request,
        "weed_detection/index.html",
        context
    )