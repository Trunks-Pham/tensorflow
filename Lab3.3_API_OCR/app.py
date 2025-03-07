from flask import Flask, request, jsonify
import pytesseract
import numpy as np
import cv2
from PIL import Image
import io

# Initialize Flask app
app = Flask(__name__)

# Configure Tesseract OCR path (only needed if running on Windows)
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# Image preprocessing function
def preprocess_image(image):
    # Convert the image to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # Apply thresholding to binarize the image
    _, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    return thresh

@app.route("/ocr", methods=["POST"])
def recognize_text():
    if "file" not in request.files:
        return jsonify({"error": "no file upload"}), 400
    file = request.files["file"]
    image = Image.open(io.BytesIO(file.read()))
    image = np.array(image)
    processed_image = preprocess_image(image)
    text = pytesseract.image_to_string(processed_image)
    return jsonify({"text": text})

if __name__ == "__main__":
    app.run(debug=True)