# 🚀 DichThuat_Pro - Clipboard Translator

Công cụ dịch thuật "nhanh như chớp", được thiết kế tối giản để hòa nhập hoàn hảo vào môi trường làm việc của bạn. Chỉ cần Copy, bản dịch sẽ xuất hiện ngay lập tức trên dải thông báo chuyên nghiệp dưới đáy màn hình.

![Version](https://img.shields.io/badge/version-3.0.0-blue)
![Engine](https://img.shields.io/badge/engine-GoogleTranslate-orange)
![Platform](https://img.shields.io/badge/platform-windows-lightgrey)

## ✨ Tính năng nổi bật

- ⚡ **Auto-Translate (Dịch tự động)**: Không cần phím tắt phức tạp! Chỉ cần nhấn `Ctrl + C` (Copy), ứng dụng sẽ tự động phát hiện và dịch ngay lập tức.
- 🧠 **Smart Clean PDF**: Tự động phát hiện và xử lý lỗi xuống dòng khi copy từ file PDF, giúp bản dịch liền mạch và chính xác hơn.
- 🖥️ **Professional Overlay**: 
  - Dải thông báo màu đen than (`#1C1C1C`) sang trọng.
  - Hiển thị văn bản dạng **One-Line** (một dòng) gọn gàng, không che khuất nội dung làm việc.
  - Luôn nổi (Always on Top) nhưng không làm phiền.
- 🚀 **Autostart**: Tích hợp sẵn tùy chọn "Khởi động cùng Windows" để ứng dụng luôn sẵn sàng mỗi khi bạn mở máy.
- 🌐 **Google Translate**: Sử dụng bộ máy dịch thuật Google Translate cho tốc độ nhanh và hỗ trợ đa dạng nội dung.

## 🛠️ Yêu cầu hệ thống

- Windows 10/11
- Python 3.x (nếu chạy source)
- Internet (để kết nối API dịch)

## 🚀 Hướng dẫn sử dụng

### 1. Cài đặt & Chạy
- **Cách đơn giản nhất**: Vào thư mục `dist`, chạy file `DichThuat_Pro.exe`.
- Ứng dụng sẽ chạy ngầm dưới khay hệ thống (System Tray) và hiện dải đen "Sẵn sàng..." dưới đáy màn hình.

### 2. Dịch thuật
1.  Bôi đen đoạn văn bản cần dịch (trên Web, Word, PDF...).
2.  Nhấn **`Ctrl + C`**.
3.  Nhìn xuống đáy màn hình để xem kết quả ngay lập tức.

### 3. Cài đặt nâng cao
- Click chuột phải vào icon ở khay hệ thống -> Chọn **Cài đặt**.
- Tại đây bạn có thể:
    - Bật/Tắt chế độ dịch tự động.
    - Bật/Tắt tính năng **Khởi động cùng Windows**.

## 📦 Hướng dẫn đóng gói (Build .exe)

Để tạo file `.exe` từ mã nguồn:
1. Cài đặt thư viện: `pip install -r requirements.txt`
2. Chạy file `build.bat` (click đúp chuột).
3. File sản phẩm sẽ nằm trong thư mục `dist/`.

---
**DichThuat_Pro** - *Copy là Dịch.*
