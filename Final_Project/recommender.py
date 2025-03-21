import requests

user_clicks = {}

def track_click(user_id, product_id):
    if user_id not in user_clicks:
        user_clicks[user_id] = {}
    if product_id not in user_clicks[user_id]:
        user_clicks[user_id][product_id] = 0
    user_clicks[user_id][product_id] += 1

def get_recommendations(user_id):
    if user_id not in user_clicks or not user_clicks[user_id]:
        url = "https://api.escuelajs.co/api/v1/products?offset=0&limit=3"
        response = requests.get(url)
        if response.status_code == 200:
            products = response.json()
            return [
                {
                    "id": p["id"],
                    "title": p["title"],
                    "price": p["price"],
                    "images": p["images"] if p["images"] else ['https://via.placeholder.com/150'],
                    "category": p["category"]["name"]
                }
                for p in products[:3]
            ]
        return []

    clicked_products = user_clicks[user_id]
    clicked_ids = list(clicked_products.keys())

    all_products = []
    for product_id in clicked_ids:
        url = f"https://api.escuelajs.co/api/v1/products/{product_id}"
        response = requests.get(url)
        if response.status_code == 200:
            p = response.json()
            all_products.append({
                "id": p["id"],
                "title": p["title"],
                "price": p["price"],
                "images": p["images"] if p["images"] else ['https://via.placeholder.com/150'],
                "category": p["category"]["name"]
            })

    category_counts = {}
    for product in all_products:
        category = product["category"]
        category_counts[category] = category_counts.get(category, 0) + clicked_products[product["id"]]

    if not category_counts:
        return []

    top_category = max(category_counts, key=category_counts.get)

    url = "https://api.escuelajs.co/api/v1/products?offset=0&limit=10"
    response = requests.get(url)
    if response.status_code == 200:
        products = response.json()
        recommendations = [
            {
                "id": p["id"],
                "title": p["title"],
                "price": p["price"],
                "images": p["images"] if p["images"] else ['https://via.placeholder.com/150'],
                "category": p["category"]["name"]
            }
            for p in products if p["category"]["name"] == top_category and p["id"] not in clicked_ids
        ]
        return recommendations[:3]
    return []