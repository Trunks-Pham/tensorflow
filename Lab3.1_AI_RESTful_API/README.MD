# Lab 3-1: Triển khai RESTful API cho Phân Loại Hình Ảnh

## 1. Mục tiêu
- Xây dựng API Flask để phân loại hình ảnh bằng mô hình AI đã huấn luyện.
- Gửi yêu cầu đến API và nhận kết quả dự đoán.
- Kiểm thử API bằng Postman hoặc frontend đơn giản.
- Triển khai API trên Cloud hoặc Docker.

## 2. Yêu cầu chuẩn bị

### 2.1. Phần cứng
- Máy tính cài đặt Python 3.8+
- Kết nối Internet để tải thư viện cần thiết

### 2.2. Phần mềm
1. Cài đặt thư viện cần thiết:
    ```bash
    pip install flask tensorflow pillow
    ```
2. Lưu mô hình AI đã huấn luyện trước đó:
   - Hoặc mô hình MobileNet (hoặc mô hình khác phù hợp)
3. Cấu trúc thư mục dự án:
    ```
    Lab3_AI_RESTful_API/
    ├── app.py              # Code Flask API
    ├── model.h5            # Mô hình AI đã lưu
    ├── static/uploads/     # Lưu ảnh tải lên
    ├── templates/
    │   └── index.html      # Giao diện web đơn giản
    ```

## 3. Hướng dẫn triển khai API với Flask

### 3.1. Viết mã Flask API (app.py)
- Trong `app.py`, bạn sẽ tạo một API đơn giản với Flask, có khả năng nhận ảnh từ người dùng và trả về kết quả dự đoán.

```python
from flask import Flask, request, jsonify
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
import numpy as np
import os

app = Flask(__name__)

# Load model đã huấn luyện
model = load_model('model.h5')

# Route để dự đoán hình ảnh
@app.route('/predict', methods=['POST'])
def predict():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    
    # Save file tải lên
    filepath = os.path.join('static/uploads', file.filename)
    file.save(filepath)
    
    # Đọc và xử lý ảnh
    img = image.load_img(filepath, target_size=(224, 224))  # Thay đổi kích thước cho phù hợp
    img_array = image.img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0)  # Thêm chiều batch
    
    # Dự đoán với mô hình
    predictions = model.predict(img_array)
    result = np.argmax(predictions, axis=1)
    
    return jsonify({'prediction': str(result[0])})

if __name__ == '__main__':
    app.run(debug=True)
```

### 3.2. Tạo giao diện web đơn giản (index.html)
- Tạo một giao diện web để người dùng có thể tải ảnh lên và nhận kết quả dự đoán từ API.

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Image Classification</title>
</head>
<body>
    <h1>Image Classification API</h1>
    <form action="/predict" method="POST" enctype="multipart/form-data">
        <input type="file" name="file" required><br><br>
        <input type="submit" value="Upload Image">
    </form>
</body>
</html>
```

## 4. Kiểm tra API bằng Postman

1. Mở **Postman** và chọn **POST**.
2. Nhập URL: `http://127.0.0.1:5000/predict`.
3. Chọn **Body** → **form-data**, thêm key: `file` và tải ảnh lên.
4. Nhấn **Send** để gửi yêu cầu.
5. API sẽ trả về JSON chứa kết quả dự đoán.

## 5. Triển khai API lên Cloud hoặc Docker

### 5.1. Đóng gói ứng dụng với Docker

1. Tạo **Dockerfile**:
    ```Dockerfile
    FROM python:3.8
    WORKDIR /app
    COPY . /app
    RUN pip install -r requirements.txt
    CMD ["python", "app.py"]
    ```

2. Xây dựng và chạy Docker container:
    ```bash
    docker build -t ai-api .
    docker run -p 5000:5000 ai-api
    ```

### 5.2. Triển khai lên Google Cloud Run

1. Đăng nhập Google Cloud CLI:
    ```bash
    gcloud auth login
    ```

2. Triển khai API:
    ```bash
    gcloud run deploy ai-api --source . --platform managed --allow-unauthenticated
    ```

3. Nhận link API Public và kiểm tra trên Postman.

## 6. Tổng kết và bài tập mở rộng

### Tóm tắt nội dung
- Tạo RESTful API với Flask để phân loại hình ảnh.
- Gửi ảnh qua API và nhận kết quả dự đoán.
- Kiểm tra API bằng Postman.
- Triển khai API lên Docker và Cloud.

### Mở rộng
1. Thêm tính năng lưu lịch sử dự đoán vào cơ sở dữ liệu.
2. Cải thiện giao diện web hiển thị kết quả dự đoán.
3. Tích hợp API vào ứng dụng di động.
 