from flask import Flask, request, jsonify, render_template
from utils.sentiment import analyze_sentiment, extract_text_from_image

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    text = request.form['text']
    result = analyze_sentiment(text)
    return jsonify(result)

@app.route('/analyze_image', methods=['POST'])
def analyze_image():
    if 'image' not in request.files:
        return jsonify({"error": "No image file provided"}), 400

    image = request.files['image']
    image_path = f"/tmp/{image.filename}"
    image.save(image_path)

    text = extract_text_from_image(image_path)
    if 'error' in text:
        return jsonify(text), 500

    result = analyze_sentiment(text)
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True)