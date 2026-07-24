import os
import uuid
import numpy as np
import tensorflow as tf
from PIL import Image
from django.shortcuts import render
from django.conf import settings

# Load Class Names and Weed Info
try:
    from .class_names import class_names
    from .weed_info import weed_info
except ImportError:
    class_names = []
    weed_info = {}

CONFIDENCE_THRESHOLD = 50.0

# Singleton TFLite Interpreter Lazy Loading
_WEED_INTERPRETER = None

def get_weed_interpreter():
    global _WEED_INTERPRETER
    if _WEED_INTERPRETER is None:
        model_path = os.path.join(settings.BASE_DIR, "weed_detection", "model", "weed_model.tflite")
        _WEED_INTERPRETER = tf.lite.Interpreter(model_path=model_path)
        _WEED_INTERPRETER.allocate_tensors()
    return _WEED_INTERPRETER

def predict_weed(request):
    if request.method != "POST" or "image" not in request.FILES:
        return render(request, "weed_detection/index.html", {"error": "Please upload an image."} if request.method == "POST" else {})

    uploaded_file = request.FILES["image"]

    try:
        # Create uploads folder if not exists
        upload_dir = os.path.join(settings.MEDIA_ROOT, "weed_uploads")
        os.makedirs(upload_dir, exist_ok=True)

        ext = os.path.splitext(uploaded_file.name)[1].lower() or ".jpg"
        unique_filename = f"{uuid.uuid4().hex}{ext}"
        file_path = os.path.join(upload_dir, unique_filename)

        # Process Image using PIL safely
        img_pil = Image.open(uploaded_file)
        if img_pil.mode != "RGB":
            img_pil = img_pil.convert("RGB")

        # Resize for model input (224x224) and save
        img_pil_resized = img_pil.resize((224, 224))
        img_pil_resized.save(file_path, "JPEG", optimize=True, quality=80)

        # Preprocess array for TFLite
        img_array = np.array(img_pil_resized, dtype=np.float32)
        img_array = np.expand_dims(img_array, axis=0)

        # Run TFLite Model
        interpreter = get_weed_interpreter()
        input_details = interpreter.get_input_details()
        output_details = interpreter.get_output_details()

        interpreter.set_tensor(input_details[0]['index'], img_array)
        interpreter.invoke()
        prediction = interpreter.get_tensor(output_details[0]['index'])

        predicted_index = int(np.argmax(prediction[0]))
        confidence = float(np.max(prediction[0]) * 100)

        image_relative_url = f"{settings.MEDIA_URL}weed_uploads/{unique_filename}"

        if confidence < CONFIDENCE_THRESHOLD:
            return render(request, "weed_detection/index.html", {
                "error": "❌ This is not a recognized weed.",
                "confidence": round(confidence, 2),
                "uploaded_image": image_relative_url
            })

        weed_name = class_names[predicted_index] if class_names and predicted_index < len(class_names) else f"Class_{predicted_index}"
        info = weed_info.get(weed_name, {})
        control_method = info.get("control", "Not Available")

        context = {
            "prediction": weed_name,
            "confidence": round(confidence, 2),
            "scientific_name": info.get("scientific_name", "Not Available"),
            "description": info.get("description", "Not Available"),
            "control_method": [control_method] if isinstance(control_method, str) else control_method,
            "uploaded_image": image_relative_url
        }

        return render(request, "weed_detection/index.html", context)

    except Exception as e:
        print("DEBUG WEED ERROR:", str(e))
        return render(request, "weed_detection/index.html", {"error": f"Error processing image: {str(e)}"})