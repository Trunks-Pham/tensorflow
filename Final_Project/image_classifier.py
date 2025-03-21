import tensorflow as tf
from tensorflow.keras.preprocessing import image
import numpy as np

try:
    model = tf.keras.applications.MobileNetV2(weights='imagenet')
except Exception as e:
    print(f"Error loading model: {str(e)}")
    model = None

def classify_image(image_path):
    if not model:
        return "Error: Model not loaded"
    try:
        img = image.load_img(image_path, target_size=(224, 224))
        img_array = image.img_to_array(img)
        img_array = np.expand_dims(img_array, axis=0)
        img_array = tf.keras.applications.mobilenet_v2.preprocess_input(img_array)
        
        predictions = model.predict(img_array)
        decoded = tf.keras.applications.mobilenet_v2.decode_predictions(predictions, top=1)[0]
        return decoded[0][1].replace("_", " ").capitalize()
    except Exception as e:
        return f"Error classifying image: {str(e)}"