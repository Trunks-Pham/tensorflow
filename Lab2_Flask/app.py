from flask import Flask, request, jsonify, render_template
from utils.sentiment import analyze_sentiment
from transformers import pipeline
from PIL import Image
import os
from concurrent.futures import ThreadPoolExecutor
import time

app = Flask(__name__)

# Initialize the Hugging Face pipeline for OCR
ocr_pipeline = pipeline("image-to-text", model="microsoft/trocr-base-handwritten")

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    text = request.form['text']
    result = analyze_sentiment(text)
    return jsonify(result)

def process_image_part(image_part_path):
    text = ocr_pipeline(image_part_path)[0]['generated_text']
    os.remove(image_part_path)  # Clean up the temporary image part file
    return text

@app.route('/analyze_image', methods=['POST'])
def analyze_image():
    if 'image' not in request.files:
        return jsonify({"error": "No image file provided"}), 400

    image = request.files['image']
    image_path = f"/tmp/{image.filename}"
    image.save(image_path)

    # Split the image into smaller parts
    img = Image.open(image_path)
    width, height = img.size
    num_parts = 4  # Number of parts to split the image into
    part_height = height // num_parts

    image_parts = []
    for i in range(num_parts):
        part = img.crop((0, i * part_height, width, (i + 1) * part_height))
        part_path = f"/tmp/{image.filename}_part_{i}.png"
        part.save(part_path)
        image_parts.append(part_path)

    # Measure the time taken for processing
    start_time = time.time()

    # Process image parts in parallel
    with ThreadPoolExecutor() as executor:
        texts = list(executor.map(process_image_part, image_parts))

    # Combine the extracted texts and analyze sentiment
    combined_text = " ".join(texts)
    result = analyze_sentiment(combined_text)

    end_time = time.time()
    processing_time = end_time - start_time

    os.remove(image_path)  # Clean up the original image file

    return jsonify({"result": result, "processing_time": processing_time})

if __name__ == '__main__':
    app.run(debug=True)