from transformers import pipeline, AutoModelForSequenceClassification, AutoTokenizer

# Tải mô hình và tokenizer cục bộ
model_name = "distilbert-base-uncased-finetuned-sst-2-english"
try:
    model = AutoModelForSequenceClassification.from_pretrained("./sentiment_model")
    tokenizer = AutoTokenizer.from_pretrained("./sentiment_model")
except:
    # Nếu không tìm thấy mô hình cục bộ, tải từ Hugging Face và lưu lại
    model = AutoModelForSequenceClassification.from_pretrained(model_name)
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model.save_pretrained("./sentiment_model")
    tokenizer.save_pretrained("./sentiment_model")

# Khởi tạo pipeline với mô hình và tokenizer
sentiment_pipeline = pipeline('sentiment-analysis', model=model, tokenizer=tokenizer)

def analyze_sentiment(comment):
    """
    Phân tích cảm xúc của bình luận.
    Args:
        comment (str): Bình luận cần phân tích.
    Returns:
        str: Nhãn cảm xúc ('POSITIVE', 'NEGATIVE') hoặc thông báo lỗi.
    """
    if not isinstance(comment, str) or not comment.strip():
        return "Error: Comment must be a non-empty string"
    try:
        result = sentiment_pipeline(comment)
        return result[0]['label'].capitalize()  # Chuẩn hóa định dạng: Positive, Negative
    except Exception as e:
        return f"Error analyzing sentiment: {str(e)}"
