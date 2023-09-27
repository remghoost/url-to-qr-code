import tkinter as tk
from tkinter import filedialog
import qrcode
from PIL import Image, ImageTk, ImageGrab
import pyperclip
import io
import win32clipboard
import win32con
import os
import atexit

class URLToQRApp:
    def __init__(self, root):
        self.root = root
        self.root.title("URL to QR Code")
        
        self.create_gui()
        self.clipboard_monitor()

    def clipboard_monitor(self):
        self.prev_clipboard_data = ""
        self.update_qr_code()
        self.root.after(1000, self.clipboard_monitor)

    def update_qr_code(self):
        clipboard_data = pyperclip.paste()

        if clipboard_data.startswith("http://") or clipboard_data.startswith("https://"):
            if clipboard_data != self.prev_clipboard_data:
                self.prev_clipboard_data = clipboard_data
                self.generate_qr_code(clipboard_data)
        else:
            self.prev_clipboard_data = ""

        self.root.after(1000, self.update_qr_code)

    def create_gui(self):
        self.qr_code_label = tk.Label(self.root, width=200, height=200)
        self.qr_code_label.pack()

        self.save_button = tk.Button(self.root, text="Save", command=self.save_qr_code)
        self.save_button.pack()

        self.copy_to_clipboard_button = tk.Button(self.root, text="Copy to Clipboard", command=self.copy_qr_code_to_clipboard)
        self.copy_to_clipboard_button.pack()

    def generate_qr_code(self, url):
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(url)
        qr.make(fit=True)

        img = qr.make_image(fill_color="black", back_color="white")
        img = img.resize((200, 200), Image.LANCZOS)
        self.qr_code_image = ImageTk.PhotoImage(img)
        self.qr_code_label.config(image=self.qr_code_image)
        if os.path.exists("temp.png"):
            os.remove("temp.png")
        self.copy_qr_code_to_clipboard()

    def save_qr_code(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png")])
        if file_path:
            img = qrcode.make(pyperclip.paste())
            img.save(file_path)

    def copy_qr_code_to_clipboard(self):
        if os.path.exists("temp.png"):
            print("TEMP FILE EXISTS")
            image = Image.open("temp.png")
            image = image.convert("RGB")

            image_stream = io.BytesIO()
            image.save(image_stream, format="BMP")
            image_data = image_stream.getvalue()[14:]  # Skip the BMP header  

            win32clipboard.OpenClipboard()
            win32clipboard.EmptyClipboard()
            win32clipboard.SetClipboardData(win32con.CF_DIB, image_data)
            win32clipboard.CloseClipboard()
            return
        else:
            print("DOESN'T EXIST")
            pass

        if hasattr(self, 'qr_code_image'):
            print("PULLING FROM QR CODE IN GUI")

            img = qrcode.make(pyperclip.paste())
            img.save("temp.png")

            image = Image.open("temp.png")
            image = image.convert("RGB")

            image_stream = io.BytesIO()
            image.save(image_stream, format="BMP")
            image_data = image_stream.getvalue()[14:]  # Skip the BMP header  

            win32clipboard.OpenClipboard()
            win32clipboard.EmptyClipboard()
            win32clipboard.SetClipboardData(win32con.CF_DIB, image_data)
            win32clipboard.CloseClipboard()

            # os.remove("temp.png")

def remove_temp_file():
    try:
        os.remove("temp.png")
    except FileNotFoundError:
        pass

atexit.register(remove_temp_file)

if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("250x250")
    app = URLToQRApp(root)
    root.mainloop()
