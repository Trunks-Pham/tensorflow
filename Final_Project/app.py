from flask import Flask, request, render_template, jsonify
import requests
from image_classifier import classify_image
from sentiment_analyzer import analyze_sentiment
from recommender import track_click, get_recommendations

app = Flask(__name__)

# Biến lưu trữ review (giả lập database)
product_reviews = {}  # {product_id: [{"user_id": "user1", "review": "Great product!", "sentiment": "Positive"}]}

# Endpoint lấy danh sách sản phẩm
@app.route('/products', methods=['GET'])
def get_products():
    page = request.args.get('page', 1, type=int)
    page_size = request.args.get('page_size', 20, type=int)
    offset = (page - 1) * page_size
    url = f'https://api.escuelajs.co/api/v1/products?offset={offset}&limit={page_size}'
    try:
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            products = response.json()
            filtered_products = [
                {
                    'id': product['id'],
                    'title': product['title'],
                    'price': product['price'],
                    'images': product['images'] if product['images'] else ['https://via.placeholder.com/150'],
                    'category': product['category']['name']
                }
                for product in products
            ]
            return jsonify({'products': filtered_products})
        return jsonify({'error': f'API returned status {response.status_code}'}), response.status_code
    except requests.exceptions.RequestException as e:
        return jsonify({'error': f'Failed to fetch products: {str(e)}'}), 500

# Endpoint lấy chi tiết sản phẩm
@app.route('/product/<int:product_id>', methods=['GET'])
def get_product(product_id):
    try:
        url = f'https://api.escuelajs.co/api/v1/products/{product_id}'
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            product = response.json()
            return jsonify({
                'id': product['id'],
                'title': product['title'],
                'slug': product['slug'],
                'price': product['price'],
                'description': product['description'],
                'category': product['category']['name'],
                'category_image': product['category']['image'],
                'images': product['images'],
                'creationAt': product['creationAt'],
                'updatedAt': product['updatedAt']
            })
        else:
            return jsonify({
                'error': 'Product not found in EscuelaJS API',
                'status_code': response.status_code,
                'response': response.text
            }), 404
    except requests.exceptions.RequestException as e:
        return jsonify({'error': f'Failed to connect to EscuelaJS API: {str(e)}'}), 500

# Endpoint gửi review từ modal
@app.route('/submit_review', methods=['POST'])
def submit_review():
    data = request.get_json()
    if not data or 'user_id' not in data or 'product_id' not in data or 'review' not in data:
        return jsonify({'error': 'Missing user_id, product_id, or review'}), 400
    user_id = data['user_id']
    product_id = data['product_id']
    review = data['review']
    sentiment = analyze_sentiment(review)
    
    if product_id not in product_reviews:
        product_reviews[product_id] = []
    product_reviews[product_id].append({
        'user_id': user_id,
        'review': review,
        'sentiment': sentiment
    })
    return jsonify({'status': 'review submitted', 'sentiment': sentiment})

# Endpoint lấy danh sách sản phẩm đã review
@app.route('/reviews', methods=['GET'])
def get_reviews():
    reviewed_products = []
    for product_id, reviews in product_reviews.items():
        try:
            url = f'https://api.escuelajs.co/api/v1/products/{product_id}'
            response = requests.get(url, timeout=5)
            if response.status_code == 200:
                product = response.json()
                reviewed_products.append({
                    'id': product['id'],
                    'title': product['title'],
                    'price': product['price'],
                    'images': product['images'] if product['images'] else ['https://via.placeholder.com/150'],
                    'category': product['category']['name'],
                    'category_image': product['category']['image'],
                    'description': product['description'],
                    'reviews': reviews
                })
        except requests.exceptions.RequestException as e:
            continue  # Bỏ qua nếu không lấy được chi tiết sản phẩm
    return jsonify({'reviewed_products': reviewed_products})

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/classify', methods=['POST'])
def classify():
    if 'file' not in request.files:
        return jsonify({'error': 'No file provided'}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400
    file.save(f'static/uploads/{file.filename}')
    category = classify_image(f'static/uploads/{file.filename}')
    return jsonify({'category': category})

@app.route('/analyze', methods=['POST'])
def analyze():
    data = request.get_json()
    if not data or 'comment' not in data:
        return jsonify({'error': 'No comment provided'}), 400
    comment = data['comment']
    sentiment = analyze_sentiment(comment)
    return jsonify({'sentiment': sentiment})

@app.route('/track_click', methods=['POST'])
def track():
    data = request.get_json()
    if not data or 'user_id' not in data or 'product_id' not in data:
        return jsonify({'error': 'Missing user_id or product_id'}), 400
    user_id = data['user_id']
    product_id = data['product_id']
    track_click(user_id, product_id)
    return jsonify({'status': 'click tracked'})

@app.route('/recommend', methods=['GET'])
def recommend():
    user_id = request.args.get('user_id')
    if not user_id:
        return jsonify({'error': 'Missing user_id'}), 400
    recommendations = get_recommendations(user_id)
    return jsonify({'recommendations': recommendations})

if __name__ == '__main__':
    app.run(debug=True)