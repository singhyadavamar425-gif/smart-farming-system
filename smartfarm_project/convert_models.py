import os
import tensorflow as tf

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# 1. Weed Model Convert Karein
weed_keras_path = os.path.join(BASE_DIR, 'weed_detection', 'model', 'weed_identification_efficientnetb0.keras')
weed_tflite_path = os.path.join(BASE_DIR, 'weed_detection', 'model', 'weed_model.tflite')

if os.path.exists(weed_keras_path):
    print("Converting Weed Model to TFLite...")
    weed_model = tf.keras.models.load_model(weed_keras_path, compile=False)
    converter = tf.lite.TFLiteConverter.from_keras_model(weed_model)
    converter.optimizations = [tf.lite.Optimize.DEFAULT]
    weed_tflite = converter.convert()
    with open(weed_tflite_path, 'wb') as f:
        f.write(weed_tflite)
    print("✅ Weed Model Converted Successfully!")
else:
    print("❌ Weed Keras model not found at path:", weed_keras_path)

# 2. Pest Model Convert Karein
pest_keras_path = os.path.join(BASE_DIR, 'pest_detection', 'model', 'pest_detection_efficientnetb0.keras')
pest_tflite_path = os.path.join(BASE_DIR, 'pest_detection', 'model', 'pest_model.tflite')

if os.path.exists(pest_keras_path):
    print("Converting Pest Model to TFLite...")
    pest_model = tf.keras.models.load_model(pest_keras_path, compile=False)
    converter = tf.lite.TFLiteConverter.from_keras_model(pest_model)
    converter.optimizations = [tf.lite.Optimize.DEFAULT]
    pest_tflite = converter.convert()
    with open(pest_tflite_path, 'wb') as f:
        f.write(pest_tflite)
    print("✅ Pest Model Converted Successfully!")
else:
    print("❌ Pest Keras model not found at path:", pest_keras_path)