from flask import Flask, request, jsonify, render_template
import tensorflow as tf
import numpy as np
from PIL import Image
import os
import tensorflow_hub as hub

app = Flask(__name__)

# Load the pre-trained MobileNetV2 model from TensorFlow Hub
model_url = "https://tfhub.dev/google/tf2-preview/mobilenet_v2/classification/4"
model = hub.load(model_url)
print("Model loaded successfully!")

# Define upload folder for saving images
UPLOAD_FOLDER = 'static/uploads/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Preprocess the uploaded image
def preprocess_image(image_path):
    image = Image.open(image_path).resize((224, 224))  # Resize image to 224x224
    image = np.array(image) / 255.0  # Normalize the pixel values to [0, 1]
    image = image[np.newaxis, ...]  # Add batch dimension
    return image

# Route for the home page
@app.route('/')
def index():
    return render_template('index.html')

# API for prediction
@app.route('/predict', methods=['POST'])
def predict():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"})

    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"})

    # Save the file to the upload folder
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    file.save(filepath)

    # Preprocess the image and make prediction
    processed_image = preprocess_image(filepath)
    processed_image = tf.cast(processed_image, dtype=tf.float32)

    # Run prediction with the MobileNetV2 model
    predictions = model(processed_image)
    predicted_class = np.argmax(predictions, axis=-1)

    # Load ImageNet labels
    labels_path = "https://storage.googleapis.com/download.tensorflow.org/data/ImageNetLabels.txt"
    labels = tf.keras.utils.get_file("ImageNetLabels.txt", labels_path)

    with open(labels, "r") as f:
        labels = f.read().splitlines()

    # Get the predicted label and confidence score
    predicted_label = labels[predicted_class[0]]
    confidence = np.max(predictions)

    return jsonify({
        "predictions": [
            {"class": predicted_label, "confidence": float(confidence)}
        ]
    })

if __name__ == '__main__':
    app.run(debug=True)
