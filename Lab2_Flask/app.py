from flask import Flask, request, jsonify, render_template
from transformers import pipeline
from PIL import Image
import os
import time
from concurrent.futures import ThreadPoolExecutor

def analyze_sentiment(text):
    sentiment_pipeline = pipeline("sentiment-analysis")
    result = sentiment_pipeline(text)[0]
    return {"label": result['label'], "score": round(result['score'] * 100, 2)}

app = Flask(__name__)
ocr_pipeline = pipeline("image-to-text", model="microsoft/trocr-base-handwritten")

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    text = request.form.get('text', '')
    if not text:
        return jsonify({"error": "No text provided"}), 400
    result = analyze_sentiment(text)
    return jsonify(result)

def process_image(image_path):
    text = ocr_pipeline(image_path)[0]['generated_text']
    os.remove(image_path)
    return text

@app.route('/analyze_image', methods=['POST'])
def analyze_image():
    if 'image' not in request.files:
        return jsonify({"error": "No image file provided"}), 400
    
    image = request.files['image']
    image_path = f"/tmp/{image.filename}"
    image.save(image_path)
    img = Image.open(image_path)
    width, height = img.size
    num_parts = 4
    part_height = height // num_parts

    image_parts = []
    for i in range(num_parts):
        part = img.crop((0, i * part_height, width, (i + 1) * part_height))
        part_path = f"/tmp/{image.filename}_part_{i}.png"
        part.save(part_path)
        image_parts.append(part_path)

    start_time = time.time()
    with ThreadPoolExecutor() as executor:
        texts = list(executor.map(process_image, image_parts))
    combined_text = " ".join(texts)
    result = analyze_sentiment(combined_text)
    end_time = time.time()
    
    os.remove(image_path)
    return jsonify({"extracted_text": combined_text, "sentiment_analysis": result, "processing_time": round(end_time - start_time, 2)})

if __name__ == '__main__':
    app.run(debug=True)
