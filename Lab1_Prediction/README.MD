## Lab 1 - Phân loại hình ảnh với mô hình MobileNet trên TensorFlow Hub

## Mục tiêu
- Làm quen với TensorFlow Hub và mô hình MobileNet.
- Hiểu cách sử dụng mô hình đã được huấn luyện sẵn để phân loại hình ảnh.
- Thực hành tiền xử lý hình ảnh và sử dụng mô hình AI để đưa ra dự đoán.

## Yêu cầu chuẩn bị

### 1. Phần mềm và công cụ:
- **Python 3.x**
- **Thư viện cần thiết**:
  - TensorFlow
  - TensorFlow Hub
  - Matplotlib
  - PIL (Python Imaging Library)

- **IDE**: Google Colab hoặc môi trường Python trên máy cá nhân.

### 2. Kiến thức nền:
- Biết cách cài đặt và sử dụng các thư viện Python.
- Hiểu cơ bản về xử lý hình ảnh và cấu trúc của các mô hình Deep Learning.

## Nội dung thực hiện

### **Bước 1: Thiết lập môi trường**
1. Tạo một dự án trên Google Colab hoặc cài đặt các thư viện cần thiết trên máy cá nhân bằng lệnh:
```bash
pip install tensorflow tensorflow-hub matplotlib pillow
```
2. Kiểm tra phiên bản TensorFlow:
```python
import tensorflow as tf
print("TensorFlow Version:", tf.__version__)
```
Nếu không có lỗi, bạn đã sẵn sàng thực hiện bài Lab.

### **Bước 2: Tải mô hình MobileNet từ TensorFlow Hub**
1. Import các thư viện cần thiết:
```python
import tensorflow_hub as hub
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
```
2. Tải mô hình MobileNet từ TensorFlow Hub:
```python
model_url = "https://tfhub.dev/google/tf2-preview/mobilenet_v2/classification/4"
model = hub.load(model_url)
print("Model loaded successfully!")
```
3. Hiểu mô hình MobileNet:
- **MobileNet** là một mô hình nhẹ, được tối ưu hóa cho các thiết bị có tài nguyên hạn chế.
- Nó được huấn luyện trên tập dữ liệu ImageNet với 1.000 nhãn khác nhau.

### **Bước 3: Chuẩn bị dữ liệu đầu vào**
1. Tải và hiển thị hình ảnh mẫu:
```python
image_path = "https://upload.wikimedia.org/wikipedia/commons/9/9a/Pug_600.jpg"  # URL hình ảnh
image = Image.open(tf.keras.utils.get_file("pug.jpg", image_path)).resize((224, 224))
plt.imshow(image)
plt.axis('off')
plt.show()
```
Chú ý: MobileNet yêu cầu kích thước ảnh là 224x224 pixel.

2. Tiền xử lý hình ảnh:
```python
def preprocess_image(image):
    image = np.array(image) / 255.0  # Chuẩn hóa pixel về khoảng [0, 1]
    return image[np.newaxis, ...]  # Thêm batch dimension

processed_image = preprocess_image(image)
print("Image preprocessed successfully!")
```

### **Bước 4: Chạy dự đoán với mô hình**
1. Thực hiện dự đoán:
```python
predictions = model(processed_image)
predicted_class = np.argmax(predictions, axis=-1)
print("Predicted class index:", predicted_class)
```
Hàm `np.argmax` tìm chỉ số của lớp có xác suất cao nhất.

2. Tải danh sách nhãn lớp từ ImageNet:
```python
labels_path = "https://storage.googleapis.com/download.tensorflow.org/data/ImageNetLabels.txt"
labels = tf.keras.utils.get_file("ImageNetLabels.txt", labels_path)

with open(labels, "r") as f:
    labels = f.read().splitlines()

print("Predicted label:", labels[predicted_class[0]])
```
- File chứa danh sách nhãn được cung cấp bởi TensorFlow Hub.

### **Bước 5: Hiển thị kết quả**
1. Vẽ kết quả dự đoán trên hình ảnh:
```python
plt.imshow(image)
plt.title(f"Prediction: {labels[predicted_class[0]]}")
plt.axis('off')
plt.show()
```
Hình ảnh sẽ hiển thị cùng với nhãn dự đoán.
---