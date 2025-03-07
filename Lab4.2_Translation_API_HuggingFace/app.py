from flask import Flask, request, jsonify, render_template
from transformers import pipeline
from PIL import Image
import os
import time
from concurrent.futures import ThreadPoolExecutor

# Khởi tạo pipeline dịch thuật
translation_pipeline = pipeline("translation_en_to_fr")  # Thay thế với mô hình phù hợp 

def translate_text(text):
    result = translation_pipeline(text)[0]
    return {"translated_text": result['translation_text']}

def process_image(image_path):
    text = ocr_pipeline(image_path)[0]['generated_text']
    os.remove(image_path)  # Xóa file tạm
    return text

app = Flask(__name__)
ocr_pipeline = pipeline("image-to-text", model="microsoft/trocr-base-handwritten")

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/translate', methods=['POST'])
def translate():
    text = request.form.get('text', '').strip()
    if not text:
        return jsonify({"error": "No text provided"}), 400
    result = translate_text(text)
    return jsonify(result)

@app.route('/translate_image', methods=['POST'])
def translate_image():
    if 'image' not in request.files:
        return jsonify({"error": "No image file provided"}), 400
    
    image = request.files['image']
    image_path = f"/tmp/{image.filename}"
    image.save(image_path)
    
    try:
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

        # Xử lý ảnh song song
        start_time = time.time()
        with ThreadPoolExecutor() as executor:
            texts = list(executor.map(process_image, image_parts))
        combined_text = " ".join(texts)
        result = translate_text(combined_text)
        end_time = time.time()

        # Dọn dẹp tệp tạm
        for part_path in image_parts:
            os.remove(part_path)

        return jsonify({
            "extracted_text": combined_text,
            "translation": result,
            "processing_time": round(end_time - start_time, 2)
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        os.remove(image_path)

if __name__ == '__main__':
    app.run(debug=True)
