import os
import joblib
import pandas as pd
from django.conf import settings
from django.shortcuts import render

# ================= Load Model =================

MODEL_PATH = os.path.join(settings.BASE_DIR, "crop_model.pkl")
SCALER_PATH = os.path.join(settings.BASE_DIR, "scaler.pkl")

model = joblib.load(MODEL_PATH)
scaler = joblib.load(SCALER_PATH)

# ================= Soil Dictionary =================

SOIL = {
    "rice": "Clay Soil",
    "maize": "Loamy Soil",
    "cotton": "Black Soil",
    "banana": "Loamy Soil",
    "papaya": "Sandy Loam",
    "apple": "Well Drained Soil",
    "orange": "Loamy Soil",
    "mango": "Red Loam Soil",
    "grapes": "Sandy Loam",
    "watermelon": "Sandy Soil"
}

# ================= Fertilizer Dictionary =================

FERTILIZER = {
    "rice": "Urea + DAP",
    "maize": "NPK 20:20:20",
    "cotton": "Potash + Urea",
    "banana": "Organic Compost",
    "papaya": "Vermicompost",
    "apple": "Farm Yard Manure",
    "orange": "NPK 10:10:10",
    "mango": "Organic Compost",
    "grapes": "DAP",
    "watermelon": "Potash"
}

# ================= GDD Dictionary =================

GDD = {
    "rice": 2200,
    "maize": 1600,
    "cotton": 2400,
    "banana": 1800,
    "papaya": 2000,
    "apple": 2500,
    "orange": 2100,
    "mango": 2700,
    "grapes": 1900,
    "watermelon": 1700
}

def home(request):

    prediction = None
    confidence = None
    top5 = []
    soil = None
    fertilizer = None
    gdd = None
    crop_image = None

    if request.method == "POST":

        N = float(request.POST["N"])
        P = float(request.POST["P"])
        K = float(request.POST["K"])
        temperature = float(request.POST["temperature"])
        humidity = float(request.POST["humidity"])
        ph = float(request.POST["ph"])
        rainfall = float(request.POST["rainfall"])

        data = pd.DataFrame({
            "N":[N],
            "P":[P],
            "K":[K],
            "temperature":[temperature],
            "humidity":[humidity],
            "ph":[ph],
            "rainfall":[rainfall]
        })

        scaled_data = scaler.transform(data)

        probabilities = model.predict_proba(scaled_data)[0]
        classes = model.classes_

        top_indices = probabilities.argsort()[-5:][::-1]

        for i in top_indices:
            top5.append({
                "crop": classes[i],
                "confidence": round(probabilities[i]*100,2)
            })

        prediction = top5[0]["crop"]
        confidence = top5[0]["confidence"]

        crop = prediction.lower()

        soil = SOIL.get(crop, "Suitable Soil Not Available")
        fertilizer = FERTILIZER.get(crop, "General NPK Fertilizer")
        gdd = GDD.get(crop, "Not Available")

        crop_image = f"crop/images/{crop}.jpg"

    return render(request, "index.html", {
        "prediction": prediction,
        "confidence": confidence,
        "top5": top5,
        "soil": soil,
        "fertilizer": fertilizer,
        "gdd": gdd,
        "crop_image": crop_image,
    })