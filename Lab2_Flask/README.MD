## Lab 2: Tích hợp Hugging Face API vào ứng dụng web để nhận dạng văn bản từ ảnh

## 1. Mục tiêu
- Hiểu cách tích hợp API AI vào ứng dụng web.
- Sử dụng Hugging Face Transformers để nhận dạng văn bản trong ảnh.
- Xây dựng ứng dụng web đơn giản trên Jupyter Notebook với Flask.
- Hiển thị kết quả nhận dạng văn bản ngay trên trang web sau khi tải ảnh lên.
- Hiển thị cả hình ảnh đã tải lên và văn bản được nhận dạng.

## 2. Yêu cầu chuẩn bị

### 2.1 Phần cứng
- Máy tính chạy Windows 10/11.
- RAM tối thiểu 4GB (khuyến nghị 8GB).

### 2.2 Phần mềm và môi trường
1. **Cài đặt Python (Phiên bản 3.8 trở lên)**:
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
   pip install flask transformers torch requests pillow
   ```

4. **Đăng ký API Key trên Hugging Face**:
   - Truy cập Hugging Face và tạo tài khoản.
   - Truy cập Hugging Face API để tạo API Key.
   - Lưu API Key để sử dụng trong ứng dụng.

## 3. Cấu trúc thư mục dự án

```
Lab2_AI_API_Integration/
│-- app.py  # Code Flask
│-- templates/
│   │-- index.html  # Giao diện web
│-- static/
│   │-- uploads/  # Lưu ảnh tải lên
│-- .env  # Chứa API Key của Hugging Face
```

## 4. Hướng dẫn triển khai

### 4.1 Tạo ứng dụng Flask trong Jupyter Notebook
Trong một cell của Jupyter Notebook, tạo ứng dụng Flask cơ bản:
```python
from flask import Flask, render_template, request, redirect, url_for
import os

app = Flask(__name__)

# Đảm bảo thư mục uploads tồn tại
if not os.path.exists('static/uploads'):
    os.makedirs('static/uploads')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return redirect(request.url)
    file = request.files['file']
    if file.filename == '':
        return redirect(request.url)
    if file:
        filepath = os.path.join('static/uploads', file.filename)
        file.save(filepath)
        # Gọi API Hugging Face để nhận dạng văn bản
        # TODO: Thêm phần xử lý OCR
        return render_template('index.html', uploaded_image=file.filename, ocr_text="Text detected from image.")

if __name__ == '__main__':
    app.run(debug=True)
```

### 4.2 Cập nhật giao diện để hiển thị ảnh và kết quả OCR (`index.html`)
```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Text Recognition App</title>
</head>
<body>
    <h1>Upload an image for Text Recognition</h1>
    <form action="/upload" method="post" enctype="multipart/form-data">
        <input type="file" name="file" required>
        <button type="submit">Upload</button>
    </form>

    {% if uploaded_image %}
    <h2>Uploaded Image</h2>
    <img src="{{ url_for('static', filename='uploads/' + uploaded_image) }}" width="400">
    <h2>Recognized Text</h2>
    <p>{{ ocr_text }}</p>
    {% endif %}
</body>
</html>
```

## 5. Kết luận
- Ứng dụng đã được cập nhật để hiển thị cả ảnh đã tải lên và văn bản được nhận dạng.
- Người dùng có thể dễ dàng kiểm tra kết quả ngay trên trang web.
- Có thể mở rộng để lưu kết quả OCR vào cơ sở dữ liệu hoặc cải thiện giao diện.

## Phụ lục

### Hướng dẫn Đăng ký và Sử dụng Hugging Face API

#### 1. Đăng ký tài khoản trên Hugging Face
1. Truy cập trang chính thức: [Hugging Face Join](https://huggingface.co/join)
2. Điền thông tin đăng ký: username, email, password.
3. Nhấn Sign Up để tạo tài khoản.
4. Xác minh email: Kiểm tra email và xác nhận tài khoản.
5. Đăng nhập vào Hugging Face: [Hugging Face Login](https://huggingface.co/login)

#### 2. Lấy API Key trên Hugging Face
1. Truy cập Token Settings: [Hugging Face Tokens](https://huggingface.co/settings/tokens)
2. Nhấn “New Token” (Tạo Access Token mới).
3. Đặt tên Token (VD: MyHuggingFaceToken).
4. Chọn quyền truy cập:
   - Read (Chỉ đọc): Dùng để truy cập API.
   - Write (Ghi dữ liệu): Nếu bạn cần tải mô hình lên.
   - Admin (Quản trị viên): Toàn quyền quản lý.
5. Nhấn “Generate Token” và sao chép API Key.

#### 3. Sử dụng Hugging Face API trong Python
Sau khi có API Key, bạn có thể gọi API của Hugging Face để chạy mô hình AI. Ví dụ:
```python
import requests

API_KEY = 'YOUR_API_KEY'
headers = {
    "Authorization": f"Bearer {API_KEY}"
}

# Gọi API để nhận diện văn bản từ hình ảnh
response = requests.post('https://api-inference.huggingface.co/models/your-model', headers=headers, files={'file': open('your-image.jpg', 'rb')})
result = response.json()
print(result)
```

### 4. Các API phổ biến của Hugging Face

| API                   | Ứng dụng                                            | Ví dụ Model                        |
|-----------------------|-----------------------------------------------------|------------------------------------|
| **NLP**                | Dịch ngôn ngữ, phân tích cảm xúc, tóm tắt văn bản    | bert-base-uncased, facebook/bart-large-mnli |
| **Text-to-Speech (TTS)** | Chuyển đổi văn bản thành giọng nói                 | facebook/wav2vec2-large-xlsr53     |
| **Computer Vision**    | Nhận diện vật thể trong ảnh                         | facebook/detr-resnet-50           |
| **Text Generation**    | Sinh văn bản tự động (AI Chatbot)                   | gpt2, facebook/blenderbot400M-distill |

### 5. Kiểm tra và xử lý lỗi
| Lỗi                    | Nguyên nhân                     | Cách khắc phục                      |
|------------------------|---------------------------------|------------------------------------|
| **403 Forbidden**       | API Key sai hoặc thiếu         | Kiểm tra lại API Key trong HEADERS. |
| **Quota Exceeded**      | Gọi API quá nhiều lần          | Kiểm tra quota miễn phí hoặc nâng cấp tài khoản. |
| **Invalid JSON response** | API không nhận diện được đầu vào | Kiểm tra lại dữ liệu gửi lên có đúng định dạng không. |

### 6. Tóm tắt các bước sử dụng Hugging Face
1. Truy cập Hugging Face để tạo tài khoản.
2. Lấy API Key tại [Hugging Face Tokens](https://huggingface.co/settings/tokens).
3. Cài đặt thư viện: `pip install requests`.
4. Gửi yêu cầu HTTP đến API để sử dụng mô hình.
5. Xử lý kết quả JSON từ API.

---