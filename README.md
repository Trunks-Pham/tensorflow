```markdown
# Cài đặt TensorFlow trong Môi Trường Ảo

Để sử dụng TensorFlow trong một môi trường ảo, bạn có thể làm theo các bước dưới đây. Việc sử dụng môi trường ảo (virtual environment) sẽ giúp cô lập các thư viện và tránh xung đột với các dự án khác.

## Bước 1: Tạo Môi Trường Ảo

Để tạo một môi trường ảo mới, sử dụng lệnh sau:

```bash
python -m venv tensorflow_env
```

Lệnh này sẽ tạo ra một thư mục `tensorflow_env` trong thư mục hiện tại, nơi chứa môi trường ảo của bạn.

## Bước 2: Kích Hoạt Môi Trường Ảo

Sau khi môi trường ảo đã được tạo, bạn cần kích hoạt nó. Dưới đây là các lệnh kích hoạt môi trường ảo:

- Trên Windows:
  
  ```bash
  tensorflow_env\\Scripts\\activate
  ```

- Trên macOS/Linux:
  
  ```bash
  source tensorflow_env/bin/activate
  ```

Sau khi kích hoạt, bạn sẽ thấy dấu hiệu `(tensorflow_env)` xuất hiện trước dòng lệnh, cho biết môi trường ảo đang hoạt động.

## Bước 3: Cài Đặt TensorFlow trong Môi Trường Ảo

Bây giờ, bạn có thể cài đặt TensorFlow trong môi trường ảo bằng lệnh sau:

```bash
pip install tensorflow
```

Mọi cài đặt TensorFlow giờ đây chỉ có hiệu lực trong môi trường ảo này.

## Bước 4: Thoát Khỏi Môi Trường Ảo

Nếu bạn muốn thoát khỏi môi trường ảo, chỉ cần gõ lệnh sau:

```bash
deactivate
```

Sau khi thoát, môi trường ảo sẽ không còn hoạt động, và bạn sẽ quay lại môi trường hệ thống mặc định.

---