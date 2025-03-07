# Bài Lab 4-1: Tích hợp NLP API vào ứng dụng web

## 1. Mục tiêu Lab

- Gọi Hugging Face Sentiment Analysis API từ backend.
- Xây dựng API bằng Flask hoặc Node.js để xử lý dữ liệu từ frontend.
- Hiển thị kết quả phân tích cảm xúc lên trang web.

## 2. Yêu cầu thực hiện

### Bước 1: Chuẩn bị môi trường

- Cài đặt các thư viện cần thiết:

  Với Python:

  ```bash
  pip install requests flask
  ```


  Với Node.js:

  ```bash
  npm install express axios cors
  ```


### Bước 2: Xây dựng Backend (Flask hoặc Node.js)

- Python Flask Backend:

  Tạo một ứng dụng Flask để nhận dữ liệu từ frontend, gọi Hugging Face Sentiment Analysis API và trả kết quả về cho frontend.

- Node.js Backend (Express + Axios):

  Tạo một ứng dụng Express để xử lý yêu cầu từ frontend, sử dụng Axios để gọi Hugging Face Sentiment Analysis API và gửi kết quả lại cho frontend.

### Bước 3: Xây dựng Frontend đơn giản

- Sử dụng HTML và JavaScript để tạo giao diện người dùng cho phép nhập văn bản và gửi yêu cầu đến backend:

  ```html
  <!DOCTYPE html>
  <html lang="vi">
  <head>
    <meta charset="UTF-8">
    <title>Phân tích cảm xúc</title>
  </head>
  <body>
    <h1>Phân tích cảm xúc</h1>
    <textarea id="inputText" rows="4" cols="50"></textarea><br>
    <button onclick="analyzeSentiment()">Phân tích</button>
    <p id="result"></p>

    <script>
      async function analyzeSentiment() {
        const text = document.getElementById('inputText').value;
        const response = await fetch('/api/sentiment', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({ text }),
        });
        const result = await response.json();
        document.getElementById('result').innerText = `Kết quả: ${result.sentiment}`;
      }
    </script>
  </body>
  </html>
  ```


## 3. Kết quả mong đợi

- Khi người dùng nhập văn bản vào ô và nhấn "Phân tích", hệ thống sẽ:
  1. Gửi dữ liệu lên backend.
  2. Backend gửi yêu cầu đến Hugging Face API.
  3. Nhận kết quả và hiển thị trên frontend.

## 4. Tổng kết

- Học viên sẽ hiểu cách tích hợp các API NLP vào ứng dụng web.
- Biết cách gọi API NLP từ backend.
- Ứng dụng phân tích cảm xúc vào việc phân tích phản hồi của khách hàng.

## 5. Đánh giá bài lab

- Hoàn thành API backend và gọi được Hugging Face API (50%).
- Giao diện frontend hoạt động, hiển thị kết quả phân tích cảm xúc (30%).
- Tích hợp API mượt mà, có xử lý lỗi nếu API trả về lỗi (20%).

## Mở rộng

Học viên có thể tiếp tục phát triển hệ thống bằng cách:

- Hiển thị kết quả dưới dạng biểu đồ.
- Hỗ trợ nhiều ngôn ngữ bằng cách tích hợp Google Translate API.
- Lưu trữ dữ liệu vào cơ sở dữ liệu để phân tích thống kê. 