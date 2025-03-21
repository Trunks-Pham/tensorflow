from transformers import TFAutoModelForSequenceClassification, AutoTokenizer, pipeline

# Tải mô hình sentiment analysis với TensorFlow
try:
    # Nếu bạn có mô hình cục bộ
    model = TFAutoModelForSequenceClassification.from_pretrained("./sentiment_model", from_tf=True)
    tokenizer = AutoTokenizer.from_pretrained("./sentiment_model")
    sentiment_analyzer = pipeline('sentiment-analysis', model=model, tokenizer=tokenizer, framework='tf')
except Exception as e:
    print(f"Error loading sentiment model: {str(e)}")
    # Nếu không có mô hình cục bộ, dùng mô hình mặc định từ Hugging Face
    try:
        sentiment_analyzer = pipeline('sentiment-analysis', framework='tf')
    except Exception as e:
        print(f"Error loading default sentiment model: {str(e)}")
        sentiment_analyzer = None

def analyze_sentiment(text):
    """
    Phân tích cảm xúc của đoạn văn bản.
    Args:
        text (str): Văn bản cần phân tích.
    Returns:
        str: Positive, Negative hoặc thông báo lỗi.
    """
    if not sentiment_analyzer:
        return "Error: Sentiment model not loaded"
    try:
        result = sentiment_analyzer(text)
        return result[0]['label']  
    except Exception as e:
        return f"Error analyzing sentiment: {str(e)}"