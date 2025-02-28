from flask import Flask, request, jsonify, render_template
import torch
from transformers import DeiTForImageClassification, DeiTFeatureExtractor
from PIL import Image
import os

app = Flask(__name__)

# Load model từ Hugging Face
model = DeiTForImageClassification.from_pretrained("facebook/deit-base-distilled-patch16-224")
feature_extractor = DeiTFeatureExtractor.from_pretrained("facebook/deit-base-distilled-patch16-224")

# Tải danh sách nhãn ImageNet
LABELS_URL = "https://storage.googleapis.com/download.tensorflow.org/data/ImageNetLabels.txt"
LABELS_PATH = "imagenet_labels.txt"

if not os.path.exists(LABELS_PATH):
    import requests
    response = requests.get(LABELS_URL)
    with open(LABELS_PATH, "w") as f:
        f.write(response.text)

# Đọc danh sách nhãn
with open(LABELS_PATH, "r") as f:
    labels = f.read().splitlines()

UPLOAD_FOLDER = 'static/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/classify', methods=['POST'])
def classify_image():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400

    file = request.files['file']
    
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    
    try:
        img_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(img_path)
        
        img = Image.open(img_path)
    except Exception as e:
        return jsonify({'error': 'Invalid image format'}), 400

    # Tiền xử lý ảnh
    inputs = feature_extractor(images=img, return_tensors="pt")

    # Dự đoán với mô hình
    with torch.no_grad():
        logits = model(**inputs).logits
    predicted_class_idx = logits.argmax(-1).item()

    # Lấy tên nhãn từ danh sách ImageNet
    predicted_label = labels[predicted_class_idx] if predicted_class_idx < len(labels) else "Unknown"

    return jsonify({"predicted_class": predicted_class_idx, "label": predicted_label})

if __name__ == '__main__':
    app.run(debug=True)
