# Lab 5.2: AI API - Triển khai mô hình đã huấn luyện trước thành API có thể mở rộng với Railway

Dự án này hướng dẫn cách xây dựng, đóng gói Docker và triển khai một API AI có khả năng mở rộng bằng cách sử dụng mô hình đã huấn luyện trước (MobileNetV2) với Flask, Docker và Railway. API nhận hình ảnh đầu vào và trả về dự đoán kèm theo điểm tin cậy.

## Mục tiêu
- Xây dựng API AI sử dụng mô hình đã huấn luyện trước với Flask.
- Đóng gói API bằng Docker để dễ dàng triển khai.
- Triển khai API miễn phí trên Railway.app.

## Yêu cầu trước
- Python 3.x đã được cài đặt ([Tải tại đây](https://www.python.org/downloads/)).
- Docker đã được cài đặt (tùy chọn, để thử nghiệm cục bộ).
- Tài khoản miễn phí trên Railway.app để triển khai.
- Kiến thức cơ bản về Flask, Docker và Git.

## Cấu trúc dự án
```
ai-api/
├── app.py              # Ứng dụng Flask chính
├── Dockerfile          # Cấu hình Docker
├── requirements.txt    # Các thư viện Python cần thiết
└── README.md           # Tài liệu dự án
```

## Hướng dẫn cài đặt

### Bước 1: Thiết lập môi trường làm việc
1. **Cài đặt Python 3.x**
   - Kiểm tra phiên bản Python:
     ```bash
     python --version
     ```
   - Nếu chưa cài, tải từ [python.org](https://www.python.org/downloads/).

2. **Tạo thư mục dự án**
   ```bash
   mkdir ai-api && cd ai-api
   ```

3. **Thiết lập môi trường ảo**
   - Tạo môi trường ảo:
     ```bash
     python -m venv env
     ```
   - Kích hoạt môi trường:
     - Windows: `env\Scripts\activate`
     - Mac/Linux: `source env/bin/activate`

4. **Cài đặt các thư viện cần thiết**
   ```bash
   pip install flask tensorflow pillow
   ```
   - Kiểm tra các gói đã cài:
     ```bash
     pip list
     ```

### Bước 2: Tạo API AI
API sử dụng MobileNetV2, một mô hình học sâu đã được huấn luyện trước từ TensorFlow, để phân loại hình ảnh.

1. **Tạo file `app.py`**
   Sao chép đoạn mã sau vào `app.py`:
   ```python
   from flask import Flask, request, jsonify
   import tensorflow as tf
   import numpy as np
   from PIL import Image
   import io

   # Khởi tạo ứng dụng Flask
   app = Flask(__name__)

   # Tải mô hình MobileNetV2 đã huấn luyện trước
   model = tf.keras.applications.MobileNetV2(weights="imagenet")

   # Tải danh sách nhãn của MobileNetV2
   with open("imagenet_labels.txt") as f:
       labels = f.read().splitlines()

   @app.route('/predict', methods=['POST'])
   def predict():
       try:
           # Đọc hình ảnh từ yêu cầu
           file = request.files['file']
           img = Image.open(io.BytesIO(file.read()))
           # Tiền xử lý hình ảnh
           img = img.resize((224, 224))  # Thay đổi kích thước thành 224x224
           img_array = np.array(img) / 255.0  # Chuẩn hóa
           img_array = np.expand_dims(img_array, axis=0)  # Thêm chiều batch
           # Dự đoán
           predictions = model.predict(img_array)
           decoded_predictions = tf.keras.applications.mobilenet_v2.decode_predictions(predictions, top=3)[0]
           # Định dạng kết quả
           result = [{"label": pred[1], "confidence": float(pred[2])} for pred in decoded_predictions]
           return jsonify(result)
       except Exception as e:
           return jsonify({"error": str(e)})

   if __name__ == "__main__":
       app.run(host="0.0.0.0", port=5000)
   ```
   *Lưu ý*: Bạn cần tải file `imagenet_labels.txt` (danh sách nhãn ImageNet) và đặt vào thư mục dự án. Hoặc sử dụng nhãn có sẵn trong TensorFlow.

2. **Chạy API cục bộ**
   ```bash
   python app.py
   ```
   - Kiểm tra bằng Postman hoặc curl:
     ```bash
     curl -X POST http://127.0.0.1:5000/predict -F "file=@image.jpg"
     ```

### Bước 3: Đóng gói API bằng Docker
1. **Tạo file `Dockerfile`**
   ```dockerfile
   # Sử dụng Python 3.9 làm hình ảnh cơ sở
   FROM python:3.9

   # Đặt thư mục làm việc
   WORKDIR /app

   # Sao chép và cài đặt các yêu cầu
   COPY requirements.txt .
   RUN pip install -r requirements.txt

   # Sao chép mã nguồn
   COPY . .

   # Mở cổng và chạy ứng dụng
   EXPOSE 5000
   CMD ["python", "app.py"]
   ```

2. **Tạo file `requirements.txt`**
   ```
   flask
   tensorflow
   pillow
   ```

3. **Xây dựng và chạy hình ảnh Docker**
   ```bash
   docker build -t ai-api .
   docker run -p 5000:5000 ai-api
   ```
   - Kiểm tra lại bằng:
     ```bash
     curl -X POST http://127.0.0.1:5000/predict -F "file=@image.jpg"
     ```

### Bước 4: Triển khai lên Railway
- URL: https://thaopm-mobilenetv2.up.railway.app/predict
1. **Đẩy mã nguồn lên GitHub**
   - Khởi tạo kho Git:
     ```bash
     git init
     git add .
     git commit -m "Initial commit"
     git branch -M main
     git remote add origin https://github.com/TEN_NGUOI_DUNG/TEN_KHO.git
     git push -u origin main
     ```

2. **Triển khai trên Railway**
   - Đăng ký tại [railway.app](https://railway.app/) bằng tài khoản GitHub.
   - Tạo dự án mới:
     - Nhấn "New Project" > "Deploy from GitHub repo".
     - Kết nối với kho GitHub của bạn và chọn repository vừa đẩy lên.
   - Cấu hình:
     - Railway sẽ tự động phát hiện `Dockerfile` hoặc `requirements.txt` để build.
     - Đảm bảo biến môi trường `PORT` được đặt là `5000` (Railway yêu cầu ứng dụng lắng nghe trên biến `$PORT`).
     - Nếu cần, thêm biến môi trường trong dashboard Railway:
       ```
       PORT=5000
       ```
     - Nhấn "Deploy" để triển khai.
   - Sau khi triển khai, Railway cung cấp một URL công khai (ví dụ: `https://your-app-name.up.railway.app`).

3. **Kiểm tra API trên Railway**
   - Sử dụng URL công khai mà Railway cung cấp:
     ```bash
     curl -X POST https://your-app-name.up.railway.app/predict -F "file=@image.jpg"
     ```

## Kết quả mong đợi
Một yêu cầu thành công sẽ trả về phản hồi JSON như sau:
```json
[
  {"label": "mèo", "confidence": 0.95},
  {"label": "chó", "confidence": 0.03},
  {"label": "chim", "confidence": 0.01}
]
```

## Xử lý sự cố
- Đảm bảo tất cả thư viện cần thiết được liệt kê trong `requirements.txt`.
- Kiểm tra file hình ảnh hợp lệ và tương thích (ví dụ: `.jpg`, `.png`).
- Xem log trên Railway (trong dashboard) để tìm lỗi triển khai.
- Nếu gặp lỗi liên quan đến cổng, đảm bảo ứng dụng Flask chạy trên `$PORT` của Railway bằng cách sửa `app.run` trong `app.py`:
  ```python
  import os
  port = int(os.getenv("PORT", 5000))
  app.run(host="0.0.0.0", port=port)
  ```

---

### Ghi chú bổ sung
- Railway tự động phát hiện `Dockerfile` nếu có, vì vậy bạn không cần cấu hình thêm nếu đã đóng gói bằng Docker.
- Nếu không dùng Docker, Railway sẽ sử dụng `requirements.txt` để cài đặt môi trường Python.
- Railway cung cấp tier miễn phí với giới hạn tài nguyên, hãy kiểm tra [trang giá](https://railway.app/pricing) để biết thêm chi tiết.
 