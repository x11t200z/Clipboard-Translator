import pyperclip
import tkinter as tk
from deep_translator import GoogleTranslator
from threading import Thread
import time

# Hàm dịch văn bản
def translate_text(text):
    try:
        return GoogleTranslator(source='auto', target='vi').translate(text)
    except Exception as e:
        return f"Translation error: {e}"

# Hàm lắng nghe clipboard
def monitor_clipboard():
    global last_clipboard_text
    while True:
        try:
            # Lấy nội dung clipboard
            clipboard_text = pyperclip.paste()
            if clipboard_text != last_clipboard_text:
                last_clipboard_text = clipboard_text
                translated_text = translate_text(clipboard_text)
                update_gui(clipboard_text, translated_text)
        except Exception as e:
            print(f"Error monitoring clipboard: {e}")
        time.sleep(0.5)  # Giảm tải CPU

# Hàm cập nhật giao diện
def update_gui(original, translated):
    #original_text_var.set(f"Original:\n{original}")
    #translated_text_var.set(f"Translated:\n{translated}")
    
    translated_text.delete(1.0, tk.END)  # Xóa toàn bộ nội dung hiện tại
    translated_text.insert(tk.END, translated)  # Thêm văn bản dịch vào Text widget
    

# Hàm cập nhật wraplength
def update_wraplength(event):
    # Lấy chiều rộng của cửa sổ và cập nhật wraplength
    """
    # Hiển thị dạng Label widget
    global root, original_label, translated_label
    window_width = root.winfo_width()
    translated_label.config(wraplength=window_width - 20)  # 20 là độ lệch cho padding
    original_label.config(wraplength=window_width - 20)  # 20 là độ lệch cho padding
    """
# Giao diện hiển thị
def create_gui():
    
    global original_text_var, translated_text_var, root, original_label, translated_label, translated_text
    root = tk.Tk()
    root.title("Clipboard Translator by x11t200z")
    root.geometry("900x600")
    
    # Tạo frame để chứa Text và Scrollbar
    frame = tk.Frame(root)
    frame.pack(pady=10, fill=tk.BOTH, expand=True)
    
    # Tạo Scrollbar
    scrollbar = tk.Scrollbar(frame, orient="vertical")
    
    # Tạo widget Text để hiển thị văn bản đã dịch
    translated_text = tk.Text(frame, wrap="word", yscrollcommand=scrollbar.set, font=(None, 18), height=10, width=80)
    translated_text.pack(side="left", fill=tk.BOTH, expand=True)

    # Cấu hình scrollbar để cuộn văn bản
    scrollbar.config(command=translated_text.yview)
    scrollbar.pack(side="right", fill="y")

    """
    # Hiển thị văn bản gốc
    original_text_var = tk.StringVar()
    original_label = tk.Label(root, textvariable=original_text_var, justify="left", font=(None, 18))
    original_label.pack(pady=10, fill=tk.X)

    # Hiển thị văn bản đã dịch
    translated_text_var = tk.StringVar()
    translated_label = tk.Label(root, textvariable=translated_text_var, justify="left", fg="blue", font=(None, 18),anchor="w")
    translated_label.pack(pady=10, fill=tk.X)
    """

    # Bắt đầu luồng lắng nghe clipboard
    monitor_thread = Thread(target=monitor_clipboard, daemon=True)
    monitor_thread.start()

    # Cập nhật giá trị wraplength mỗi khi cửa sổ thay đổi kích thước
    root.bind("<Configure>", update_wraplength)

    root.mainloop()

# Biến lưu trạng thái clipboard cuối cùng
last_clipboard_text = ""

# Chạy giao diện
create_gui()


"""
Xuất/update lại chương trình
pyinstaller --onefile --windowed translate.py

pyinstaller --onefile --windowed --icon=icon.ico translate.py
"""