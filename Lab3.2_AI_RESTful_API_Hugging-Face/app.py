from flask import Flask, request, jsonify, render_template
import torch
from transformers import DeiTForImageClassification, DeiTFeatureExtractor
from PIL import Image
import os

app = Flask(__name__)

# Load model từ Hugging Face
model_name = "facebook/deit-base-distilled-patch16-224"
model = DeiTForImageClassification.from_pretrained(model_name)
feature_extractor = DeiTFeatureExtractor.from_pretrained(model_name)

UPLOAD_FOLDER = 'static/uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def classify_image(filepath):
    """Phân loại ảnh từ đường dẫn file."""
    img = Image.open(filepath).convert("RGB")
    inputs = feature_extractor(images=img, return_tensors="pt")
    with torch.no_grad():
        outputs = model(**inputs)
    logits = outputs.logits
    predicted_class_idx = logits.argmax(-1).item()
    label = model.config.id2label.get(predicted_class_idx, "Unknown")
    return predicted_class_idx, label

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/classify', methods=['POST'])
def classify():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    file.save(filepath)
    
    try:
        predicted_class_idx, predicted_label = classify_image(filepath)
        return jsonify({"predicted_class": predicted_class_idx, "label": predicted_label})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)