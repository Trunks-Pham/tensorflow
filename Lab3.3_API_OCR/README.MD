# Lab 3-3: Triển khai API RESTful nhận dạng văn bản trong ảnh bằng TensorFlow với Tesseract OCR

## Mục tiêu
- **Sử dụng TensorFlow và Tesseract OCR** để nhận dạng văn bản từ hình ảnh.
- **Xây dựng API RESTful bằng Flask**.
- **Đóng gói API với Docker** để dễ dàng triển khai.

## Yêu cầu trước khi bắt đầu
1. **Cài đặt phần mềm cần thiết**:
   - Python 3.x
   - TensorFlow
   - Flask
   - Tesseract OCR (dùng để nhận dạng văn bản)
   - OpenCV/PIL để xử lý hình ảnh
   - Postman để kiểm thử API

2. **Cài đặt thư viện Python**:
   ```
   pip install flask tensorflow numpy pillow pytesseract opencv-python
   ```

3. **Cài đặt Tesseract OCR**:
   - **Windows**: Tải từ [tesseract-ocr](https://github.com/tesseract-ocr/tesseract) và thêm vào PATH.
   - **Ubuntu**:
     ```
     sudo apt install tesseract-ocr
     ```
   - **MacOS**:
     ```
     brew install tesseract
     ```

## Bước 1: Xây dựng API RESTful bằng Flask

1.1 **Khởi tạo Flask App**

Tạo tệp `app.py` và thêm đoạn mã sau:

```python
from flask import Flask, request, jsonify
import pytesseract
from PIL import Image
import numpy as np
import cv2

app = Flask(__name__)

@app.route('/ocr', methods=['POST'])
def ocr():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    try:
        img = Image.open(file)
        img = np.array(img)
        text = pytesseract.image_to_string(img)
        return jsonify({'text': text}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
```

## Bước 2: Kiểm thử API

2.1 **Chạy API**

Chạy lệnh sau để khởi động API:

```
python app.py
```

Sau khi chạy, API sẽ hoạt động tại `http://127.0.0.1:5000/ocr`.

2.2 **Gửi yêu cầu kiểm thử bằng Postman**

- **Method**: POST
- **URL**: `http://127.0.0.1:5000/ocr`
- **Body**: Chọn form-data, key là `file`, chọn một ảnh có chứa văn bản.

## Bước 3: Đóng gói API bằng Docker

3.1 **Viết Dockerfile**

Tạo tệp `Dockerfile` với nội dung sau:

```Dockerfile
# Sử dụng Python image
FROM python:3.9

# Cài đặt thư viện cần thiết
RUN apt-get update && apt-get install -y tesseract-ocr \
    && pip install flask tensorflow numpy pillow pytesseract opencv-python

# Sao chép mã nguồn vào container
COPY . /app
WORKDIR /app

# Mở cổng 5000 và chạy API
CMD ["python", "app.py"]
```

3.2 **Xây dựng và chạy Docker container**

- Xây dựng Docker image:
  ```
  docker build -t text-recognition-api .
  ```

- Chạy Docker container:
  ```
  docker run -p 5000:5000 text-recognition-api
  ```

## Bước 4: Mở rộng API và triển khai lên Cloud

- **Mở rộng**: API có thể được tích hợp với Google Vision API hoặc AWS Rekognition để cải thiện độ chính xác.
- **Triển khai lên Cloud**: Dùng AWS Lambda, Google Cloud Run, hoặc Azure App Service để triển khai API.

## Kết luận

Sau bài Lab này, bạn sẽ có thể:
- Xây dựng API RESTful để nhận dạng văn bản trong ảnh bằng TensorFlow và Tesseract OCR.
- Kiểm thử API bằng Postman.
- Đóng gói API bằng Docker để triển khai lên môi trường thực tế.

## Bài tập mở rộng
1. Thêm tính năng lưu lịch sử dự đoán vào cơ sở dữ liệu.
2. Tích hợp giao diện web cho phép upload ảnh và hiển thị kết quả.
3. Tích hợp API vào ứng dụng di động.