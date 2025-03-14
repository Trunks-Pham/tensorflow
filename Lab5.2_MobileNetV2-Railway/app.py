from flask import Flask, request, jsonify
import tensorflow as tf
import numpy as np
from PIL import Image
import io 
import os
import tensorflow_hub as hub

app = Flask(__name__)
model = tf.keras.applications.MobileNetV2(weights='imagenet') 

with open('imagenet_labels.txt', 'r') as f:
    labels = f.read().splitlines()

@app.route('/predict', methods=['POST'])
def predict():
    try:
        file = request.files['file']
        img = Image.open(io.BytesIO(file.read()))
        img = img.resize((224, 224))
        img_array = np.array(img) / 255.0
        img_array = np.expand_dims(img_array, axis=0)

        predictions = model.predict(img_array)
        decoded_predictions = tf.keras.applications.mobilenet_v2.decode_predictions(predictions, top=3)[0]

        result = [{"label": pred[1], "confidence": float(pred[2])} for pred in decoded_predictions] 
        return jsonify(result)

    except Exception as e:
        return jsonify({'error': str(e)})

if __name__ == '__main__':  
    app.run(host='0.0.0.0', port=5000)