# Lab 4-2: Dịch Văn Bản với Hugging Face API

## 1. Mục tiêu
- Hiểu cách sử dụng Hugging Face Translation API để dịch văn bản.
- Xây dựng một API bằng Flask hoặc Node.js để gọi mô hình dịch thuật.
- Thiết kế giao diện web cho phép người dùng nhập văn bản và nhận bản dịch.

## 2. Công nghệ sử dụng

**Backend:**

- Python Flask (hoặc Node.js với Express)
- Hugging Face API (Mô hình Helsinki-NLP/opus-mt-en-vi cho dịch tiếng Anh sang tiếng Việt)

**Frontend:**

- HTML, JavaScript (Fetch API)
- Bootstrap (tùy chọn, để thiết kế giao diện đẹp hơn)

## 3. Hướng dẫn thực hiện

### Bước 1: Đăng ký API Key của Hugging Face

- Đăng ký tài khoản tại [Hugging Face](https://huggingface.co/join)
- Lấy API Token trong phần Settings > Access Tokens
- API sử dụng: [Helsinki-NLP/opus-mt-en-vi](https://huggingface.co/Helsinki-NLP/opus-mt-en-vi) (dịch tiếng Anh sang tiếng Việt)

### Bước 2: Cài đặt môi trường

- Nếu dùng Python (Flask Backend):

  ```bash
  pip install flask requests
  ```


- Nếu dùng Node.js (Express Backend):

  ```bash
  npm install express axios cors body-parser
  ```


### Bước 3: Xây dựng Backend

**Với Python Flask**

Tạo file `app.py` với nội dung sau:

```python
from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

API_URL = "https://api-inference.huggingface.co/models/Helsinki-NLP/opus-mt-en-vi"
API_TOKEN = "YOUR_HUGGING_FACE_API_TOKEN"

headers = {"Authorization": f"Bearer {API_TOKEN}"}

@app.route('/translate', methods=['POST'])
def translate():
    data = request.get_json()
    input_text = data.get('text')
    if not input_text:
        return jsonify({'error': 'No text provided'}), 400

    payload = {"inputs": input_text}
    response = requests.post(API_URL, headers=headers, json=payload)

    if response.status_code != 200:
        return jsonify({'error': 'Translation API request failed'}), 500

    result = response.json()
    translated_text = result[0]['translation_text']
    return jsonify({'translated_text': translated_text})

if __name__ == '__main__':
    app.run(debug=True)
```


Chạy server:

```bash
python app.py
```


Mở trình duyệt và thử API: [http://localhost:5000/translate](http://localhost:5000/translate)

**Với Node.js (Express)**

Tạo file `server.js` với nội dung:

```javascript
const express = require('express');
const axios = require('axios');
const bodyParser = require('body-parser');
const cors = require('cors');

const app = express();
const PORT = 5000;

const API_URL = 'https://api-inference.huggingface.co/models/Helsinki-NLP/opus-mt-en-vi';
const API_TOKEN = 'YOUR_HUGGING_FACE_API_TOKEN';

app.use(bodyParser.json());
app.use(cors());

app.post('/translate', async (req, res) => {
  const { text } = req.body;
  if (!text) {
    return res.status(400).json({ error: 'No text provided' });
  }

  try {
    const response = await axios.post(
      API_URL,
      { inputs: text },
      { headers: { Authorization: `Bearer ${API_TOKEN}` } }
    );

    const translatedText = response.data[0].translation_text;
    res.json({ translated_text: translatedText });
  } catch (error) {
    res.status(500).json({ error: 'Translation API request failed' });
  }
});

app.listen(PORT, () => {
  console.log(`Server is running on http://localhost:${PORT}`);
});
```


Chạy server:

```bash
node server.js
```


### Bước 4: Xây dựng Giao diện Web

Tạo file `index.html` với nội dung:

```html
<!DOCTYPE html>
<html lang="vi">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Dịch Văn Bản</title>
  <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
</head>
<body>
  <div class="container mt-5">
    <h1 class="mb-4">Dịch Văn Bản</h1>
    <div class="mb-3">
      <label for="inputText" class="form-label">Văn bản tiếng Anh:</label>
      <textarea class="form-control" id="inputText" rows="4"></textarea>
    </div>
    <button class="btn btn-primary" onclick="translateText()">Dịch</button>
    <div class="mt-4">
      <h5>Bản dịch tiếng Việt:</h5>
      <p id="result" class="border p-3"></p>
    </div>
  </div>

  <script>
    async function translateText() {
      const text = document.getElementById('inputText').value;
      const response = await fetch('http://localhost:5000/translate', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ text }),
      });

      if (!response.ok) {
        document.getElementById('result').innerText = 'Có lỗi xảy ra khi dịch văn bản.';
        return;
      }

      const data = await response.json();
      document.getElementById('result').innerText = data.translated_text;
    }
  </script>
</body>
</html>
```