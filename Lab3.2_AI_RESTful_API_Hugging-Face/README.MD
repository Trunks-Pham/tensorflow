# Lab 3-2 - Triển khai RESTful API cho phân loại hình ảnh với Hugging Face và Flask

## 1. Mục tiêu
- Hiểu cách triển khai RESTful API để phân loại hình ảnh.
- Sử dụng mô hình học sâu từ Hugging Face để phân loại hình ảnh.
- Xây dựng API sử dụng Flask để nhận ảnh, xử lý và trả kết quả phân loại.

## 2. Yêu cầu chuẩn bị

### 2.1 Phần cứng
- Máy tính chạy **Windows 10/11**.
- RAM tối thiểu **4GB** (khuyến nghị **8GB**).

### 2.2 Phần mềm và môi trường
1. **Cài đặt Python** (Phiên bản 3.8 trở lên):
   - Kiểm tra phiên bản Python bằng lệnh:
     ```bash
     python --version
     ```

2. **Cài đặt Jupyter Notebook**:
   - Cài đặt qua pip:
     ```bash
     pip install notebook
     ```

3. **Cài đặt thư viện cần thiết**:
   - Chạy các lệnh sau trong terminal hoặc Jupyter Notebook:
     ```bash
     pip install flask transformers torch pillow requests
     ```

4. **Đăng ký API Key trên Hugging Face (nếu cần)**:
   - Truy cập **Hugging Face** và tạo tài khoản.
   - Truy cập **Hugging Face API** để tạo API Key.
   - Lưu API Key để sử dụng trong ứng dụng.

## 3. Cấu trúc thư mục dự án
```
Lab3_Image_Classification_API/
│-- app.py                # Code Flask
│-- models/               # Lưu các mô hình
│-- static/uploads/       # Lưu ảnh tải lên
│-- .env                  # (Nếu sử dụng API Key Hugging Face)
```

## 4. Hướng dẫn triển khai

### 4.1. Cài đặt mô hình phân loại hình ảnh trên Hugging Face
Chúng ta sẽ sử dụng mô hình **facebook/deit-base-distilled-patch16-224** để phân loại hình ảnh. Mô hình này đã được huấn luyện và có thể dễ dàng tải về để sử dụng.

### 4.2. Xây dựng RESTful API với Flask
Tạo file **`app.py`** để triển khai API Flask. Dưới đây là mã nguồn cơ bản của file **app.py**:

```python
from flask import Flask, request, jsonify
import torch
from transformers import DeiTForImageClassification, DeiTFeatureExtractor
from PIL import Image
import requests
import io

app = Flask(__name__)

# Load mô hình và bộ trích xuất đặc trưng từ Hugging Face
model = DeiTForImageClassification.from_pretrained("facebook/deit-base-distilled-patch16-224")
feature_extractor = DeiTFeatureExtractor.from_pretrained("facebook/deit-base-distilled-patch16-224")

@app.route('/classify', methods=['POST'])
def classify_image():
    # Lấy file ảnh từ request
    file = request.files['file']
    img = Image.open(file.stream)

    # Tiền xử lý ảnh
    inputs = feature_extractor(images=img, return_tensors="pt")

    # Dự đoán với mô hình
    with torch.no_grad():
        logits = model(**inputs).logits
    predicted_class_idx = logits.argmax(-1).item()

    # Trả về nhãn phân loại
    return jsonify({"predicted_class": predicted_class_idx})

if __name__ == '__main__':
    app.run(debug=True)
```

### 4.3. Gửi yêu cầu API để phân loại hình ảnh
Sau khi chạy Flask, bạn có thể gửi yêu cầu API bằng Python hoặc Postman.

#### **Gửi yêu cầu bằng Python**:
```python
import requests

url = 'http://127.0.0.1:5000/classify'
file_path = 'path_to_image.jpg'
files = {'file': open(file_path, 'rb')}
response = requests.post(url, files=files)

print(response.json())
```

#### **Gửi yêu cầu bằng Postman**:
1. Chọn **POST** request.
2. Nhập URL: `http://127.0.0.1:5000/classify`.
3. Trong phần **Body**, chọn **form-data**, thêm key `file`, chọn file ảnh.
4. Nhấn **Send** để nhận kết quả phân loại.

## 5. Kiểm thử và mở rộng

### 5.1. Kiểm thử ứng dụng
- Gửi ảnh bất kỳ để kiểm tra phân loại.
- Xác minh kết quả phân loại có hợp lý không.

### 5.2. Nâng cấp ứng dụng
- **Hỗ trợ nhiều mô hình phân loại ảnh khác nhau**: Bạn có thể mở rộng API để hỗ trợ các mô hình khác như **ResNet** hay **MobileNet**.
- **Thêm xử lý ảnh trước khi phân loại**: Tăng cường tiền xử lý ảnh (như thay đổi kích thước, cân bằng ánh sáng) để cải thiện kết quả phân loại.
- **Tích hợp React hoặc Vue** để tạo giao diện web thân thiện hơn, thay vì sử dụng Postman hay Python để gửi yêu cầu API.

## 6. Kết luận
- Hoàn thành triển khai RESTful API để phân loại hình ảnh.
- Sử dụng **Hugging Face** và **Flask** để xây dựng ứng dụng phân loại hình ảnh đơn giản.
- Có thể mở rộng ứng dụng để hỗ trợ nhiều mô hình phân loại ảnh hoặc tích hợp vào hệ thống lớn hơn.
