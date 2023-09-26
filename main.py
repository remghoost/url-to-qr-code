import tkinter as tk
from tkinter import filedialog
import pyperclip
import qrcode
from PIL import Image, ImageTk

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
        img = img.resize((200, 200), Image.ANTIALIAS)
        self.qr_code_image = ImageTk.PhotoImage(img)
        self.qr_code_label.config(image=self.qr_code_image)

    def save_qr_code(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png")])
        if file_path:
            img = qrcode.make(pyperclip.paste())
            img.save(file_path)

if __name__ == "__main__":
    root = tk.Tk()
    app = URLToQRApp(root)
    root.mainloop()
