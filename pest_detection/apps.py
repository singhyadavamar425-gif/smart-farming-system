from django.apps import AppConfig
import tensorflow as tf
import os
from django.conf import settings

class PestDetectionConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'pest_detection'
    model = None

    def ready(self):
        # Pre-load model on server start up
        if not PestDetectionConfig.model:
            model_path = os.path.join(settings.BASE_DIR, 'pest_detection', 'models', 'pest_model.h5') # Apne model filename se verify karein
            if os.path.exists(model_path):
                PestDetectionConfig.model = tf.keras.models.load_model(model_path)