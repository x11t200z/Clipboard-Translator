import tkinter as tk
from tkinter import ttk
import pyperclip
from deep_translator import GoogleTranslator
from threading import Thread
import time
import queue
import pystray
from PIL import Image, ImageDraw
import sys
import os
import winreg as reg
import re

class TranslatorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Clipboard Translator Settings")
        self.root.geometry("500x450")
        self.root.configure(bg="#FAFAFA")
        
        # Biến trạng thái
        self.last_clipboard_text = pyperclip.paste()
        self.overlay_enabled = True 
        self.overlay_window = None
        self.is_running = True
        self.auto_translate_mode = True
        self.app_name = "DichThuat_Pro"

        # Hàng đợi GUI
        self.gui_queue = queue.Queue()

        self.create_gui()
        self.setup_tray()

        # Luồng giám sát Clipboard
        self.monitor_thread = Thread(target=self.monitor_clipboard, daemon=True)
        self.monitor_thread.start()
        
        self.root.protocol("WM_DELETE_WINDOW", self.hide_window)
        self.check_queue()
        
        # Khởi tạo Popup ngay và ẩn cửa sổ chính
        self.create_overlay()
        self.hide_window()
        self.ensure_topmost()

    def create_gui(self):
        header_frame = ttk.Frame(self.root, padding="20")
        header_frame.pack(fill="x")
        
        ttk.Label(header_frame, text="Dịch Thuật Pro - Cài đặt", font=("Segoe UI", 12, "bold")).pack(side="left")
        
        controls = ttk.Frame(self.root, padding="20")
        controls.pack(fill="both", expand=True)

        # Các nút điều khiển
        self.auto_btn = ttk.Button(controls, text="Chế độ Tự động: BẬT", command=self.toggle_auto_mode)
        self.auto_btn.pack(fill="x", pady=5)

        self.start_btn = ttk.Button(controls, text=self.get_autostart_text(), command=self.toggle_autostart)
        self.start_btn.pack(fill="x", pady=5)

        ttk.Label(controls, text="\nTính năng thông minh:", font=("Segoe UI", 10, "bold")).pack(anchor="w")
        ttk.Label(controls, text="• Auto-Clean PDF: Đã kích hoạt (Tự động gộp dòng).", foreground="#2E7D32").pack(anchor="w")
        
        ttk.Label(controls, text="\nHướng dẫn:", font=("Segoe UI", 10, "bold")).pack(anchor="w")
        ttk.Label(controls, text="• Copy văn bản (Ctrl+C) để thấy kết quả dưới màn hình.", justify="left").pack(anchor="w")
        
        ttk.Button(controls, text="Thu nhỏ (Ẩn cửa sổ)", command=self.hide_window).pack(side="bottom", pady=20)

    # --- Logic Khởi động cùng Windows ---
    def get_autostart_text(self):
        return "Khởi động cùng Windows: BẬT" if self.is_autostart_enabled() else "Khởi động cùng Windows: TẮT"

    def is_autostart_enabled(self):
        try:
            key = reg.OpenKey(reg.HKEY_CURRENT_USER, r"Software\Microsoft\Windows\CurrentVersion\Run", 0, reg.KEY_READ)
            value, _ = reg.QueryValueEx(key, self.app_name)
            reg.CloseKey(key)
            return True
        except:
            return False

    def toggle_autostart(self):
        key_path = r"Software\Microsoft\Windows\CurrentVersion\Run"
        try:
            if self.is_autostart_enabled():
                key = reg.OpenKey(reg.HKEY_CURRENT_USER, key_path, 0, reg.KEY_SET_VALUE)
                reg.DeleteValue(key, self.app_name)
                reg.CloseKey(key)
            else:
                # Lấy đường dẫn file hiện tại (hỗ trợ cả khi chạy .exe)
                app_path = os.path.realpath(sys.executable) if getattr(sys, 'frozen', False) else os.path.realpath(__file__)
                key = reg.OpenKey(reg.HKEY_CURRENT_USER, key_path, 0, reg.KEY_SET_VALUE)
                reg.SetValueEx(key, self.app_name, 0, reg.REG_SZ, f'"{app_path}"')
                reg.CloseKey(key)
        except Exception as e:
            print(f"Lỗi Registry: {e}")
        
        self.start_btn.config(text=self.get_autostart_text())

    # --- Logic Xử lý văn bản PDF ---
    def clean_text(self, text):
        """Xử lý văn bản từ PDF: gộp các dòng bị ngắt quãng"""
        if not text: return ""
        # 1. Thay thế dấu xuống dòng đơn lẻ bằng khoảng trắng
        # (Chỉ giữ lại xuống dòng kép - biểu thị đoạn văn mới)
        text = re.sub(r'(?<!\n)\n(?!\n)', ' ', text)
        # 2. Xóa khoảng trắng thừa
        text = re.sub(r' +', ' ', text)
        return text.strip()

    def create_icon(self):
        image = Image.new('RGB', (64, 64), "#2196F3")
        dc = ImageDraw.Draw(image)
        dc.rectangle((16, 16, 48, 48), fill="white")
        return image

    def setup_tray(self):
        menu = (
            pystray.MenuItem('Cài đặt', self.show_window, default=True),
            pystray.MenuItem('Thoát', self.quit_app)
        )
        self.icon = pystray.Icon("translator", self.create_icon(), "Clipboard Translator", menu)
        Thread(target=self.icon.run, daemon=True).start()

    def hide_window(self):
        self.root.withdraw()

    def show_window(self, icon=None, item=None):
        self.root.after(0, self.root.deiconify)

    def quit_app(self, icon=None, item=None):
        self.is_running = False
        if self.icon: self.icon.stop()
        self.root.after(0, self.root.destroy)

    def check_queue(self):
        try:
            while True:
                task_type, data = self.gui_queue.get_nowait()
                if task_type == "update_overlay":
                    self.update_overlay_gui(data)
        except queue.Empty:
            pass
        finally:
            if self.is_running:
                self.root.after(50, self.check_queue)

    def ensure_topmost(self):
        if self.overlay_enabled and self.overlay_window and tk.Toplevel.winfo_exists(self.overlay_window):
            try:
                self.overlay_window.attributes('-topmost', True)
                self.overlay_window.lift()
            except: pass
        if self.is_running:
            self.root.after(3000, self.ensure_topmost)

    def monitor_clipboard(self):
        while self.is_running:
            if self.auto_translate_mode:
                try:
                    text = pyperclip.paste()
                    if text and text != self.last_clipboard_text:
                        self.last_clipboard_text = text
                        # Áp dụng Clean Text trước khi dịch
                        cleaned = self.clean_text(text)
                        self.translate_and_update(cleaned)
                except:
                    pass
            time.sleep(0.4) 

    def translate_and_update(self, text):
        try:
            res = GoogleTranslator(source='auto', target='vi').translate(text)
            if self.overlay_enabled:
                self.gui_queue.put(("update_overlay", res))
        except:
            self.gui_queue.put(("update_overlay", "Lỗi dịch: Vui lòng kiểm tra Internet."))

    def toggle_auto_mode(self):
        self.auto_translate_mode = not self.auto_translate_mode
        self.auto_btn.config(text=f"Chế độ Tự động: {'BẬT' if self.auto_translate_mode else 'TẮT'}")

    def update_overlay_gui(self, text):
        if self.overlay_window is None or not tk.Toplevel.winfo_exists(self.overlay_window):
            self.create_overlay()
        
        # CHỈNH SỬA: Loại bỏ hoàn toàn dấu xuống dòng để text luôn thẳng hàng
        # Thay thế xuống dòng bằng khoảng trắng
        one_line_text = text.replace('\n', ' ').replace('\r', '').strip()
        
        # Xử lý khoảng trắng kép nếu có
        import re
        one_line_text = re.sub(r' +', ' ', one_line_text)

        # Cắt ngắn nếu quá dài (tăng giới hạn lên vì màn hình rộng)
        if len(one_line_text) > 250: 
            one_line_text = one_line_text[:247] + "..."
            
        self.overlay_label.config(text=one_line_text)
        
        # Đảm bảo hiển thị nếu đang bị ẩn
        self.overlay_window.deiconify()

    def hide_overlay_translation(self):
        """Ẩn overlay cho đến khi có bản dịch mới"""
        if self.overlay_window:
            self.overlay_window.withdraw()

    def create_overlay(self):
        if self.overlay_window and tk.Toplevel.winfo_exists(self.overlay_window): return

        self.overlay_window = tk.Toplevel(self.root)
        self.overlay_window.overrideredirect(True)
        sw = self.root.winfo_screenwidth()
        sh = self.root.winfo_screenheight()
        h = 47
        w = sw - 250 
        self.overlay_window.geometry(f"{w}x{h}+0+{sh-h}")
        self.overlay_window.attributes('-topmost', True)
        self.overlay_window.attributes('-alpha', 1.0)
        self.overlay_window.configure(bg="#1C1C1C")

        self.overlay_label = tk.Label(self.overlay_window, text="Sẵn sàng...", 
                                   font=("Segoe UI", 11, "bold"), fg="#FFFFFF", bg="#1C1C1C",
                                   anchor="w", padx=20)   
        self.overlay_label.pack(side="left", fill="both", expand=True)
        
        # Nút đóng (X)
        close_btn = tk.Button(self.overlay_window, text="✕", 
                            font=("Segoe UI", 10), bg="#1C1C1C", fg="#AAAAAA",
                            activebackground="#333333", activeforeground="#FF5252",
                            bd=0, cursor="hand2", width=4,
                            command=self.hide_overlay_translation)
        close_btn.pack(side="right", fill="y")

if __name__ == "__main__":
    root = tk.Tk()
    app = TranslatorApp(root)
    root.mainloop()