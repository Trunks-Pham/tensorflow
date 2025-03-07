import requests
from langdetect import detect
from config import HUGGING_FACE_API_KEY, HUGGING_FACE_MODELS
from PIL import Image
import pytesseract
from transformers import TrOCRProcessor, VisionEncoderDecoderModel

def analyze_sentiment(text):
    try:
        lang = detect(text)
        model = HUGGING_FACE_MODELS.get(lang, HUGGING_FACE_MODELS["en"])

        headers = {"Authorization": f"Bearer {HUGGING_FACE_API_KEY}"}
        api_url = f"https://api-inference.huggingface.co/models/{model}"

        payload = {"inputs": text}
        response = requests.post(api_url, headers=headers, json=payload)

        if response.status_code == 200:
            result = response.json()
            label = result[0][0]['label']
            score = result[0][0]['score']
            return {"label": label, "score": round(score * 100, 2), "language": lang}
        else:
            return {"error": f"API error: {response.status_code} - {response.text}"}
    except Exception as e:
        return {"error": f"Lỗi: {str(e)}"}

def extract_text_from_image(image_path):
    try:
        # Load the image
        image = Image.open(image_path)

        # Initialize the processor and model
        processor = TrOCRProcessor.from_pretrained('microsoft/trocr-base-handwritten')
        model = VisionEncoderDecoderModel.from_pretrained('microsoft/trocr-base-handwritten')

        # Preprocess the image
        pixel_values = processor(images=image, return_tensors="pt").pixel_values

        # Generate text
        generated_ids = model.generate(pixel_values)
        generated_text = processor.batch_decode(generated_ids, skip_special_tokens=True)[0]

        return generated_text
    except Exception as e:
        return {"error": f"Lỗi: {str(e)}"}