import tkinter as tk
from tkinter import scrolledtext
import pyperclip
import requests
import hashlib
import time
import uuid
from langdetect import detect, DetectorFactory

DetectorFactory.seed = 0
JAPANESE_FONT = 'DFSoGei-W5'
CHINESE_FONT = 'Aa我有点方'
SOURCE_LAN = 'ja'
DESTINATION_LAN = 'zh-cn'
ORIGINAL_TEXT = "Original (Japanese):"
DESTINATION_TEXT = "Translated (Chinese):"
APP_KEY = '5cc81ccc3cbf4d8b'
SECRET_KEY = 'za8BOL2O9FHpIjHrBpvi3rScUnPo7ebL'
API = "https://openapi.youdao.com/api"


def truncate(q):
    if len(q) <= 20:
        return q
    return q[0:10] + str(len(q)) + q[-10:]


def is_japanese_text(text):
    try:
        language = detect(text)
        return language == SOURCE_LAN
    except Exception as e:
        return False


def translate_text(text, src=SOURCE_LAN, dest=DESTINATION_LAN):
    app_key = APP_KEY
    secret_key = SECRET_KEY
    salt = str(uuid.uuid4())
    curtime = str(int(time.time()))

    sign_str = app_key + truncate(text) + salt + curtime + secret_key
    sign = hashlib.sha256(sign_str.encode('utf-8')).hexdigest()

    params = {
        'q': text,
        'from': src,
        'to': dest,
        'appKey': app_key,
        'salt': salt,
        'sign': sign,
        'signType': 'v3',
        'curtime': curtime,
    }

    try:
        response = requests.post(API, params=params)
        translated_text = response.json()['translation'][0]
        return translated_text
    except Exception as e:
        return f"Error: {e}"


class ClipboardTranslator:
    def __init__(self):
        self.text_area_translated = None
        self.text_area_original = None
        self.root = tk.Tk()
        self.setup_ui()
        self.current_clipboard_content = ""
        self.update_clipboard_content()
        self.root.mainloop()

    def setup_ui(self):
        self.root.title("Clipboard Translator")
        self.root.geometry('600x400')

        label_original = tk.Label(self.root, text=ORIGINAL_TEXT, font=('Arial', 10, 'bold'))
        label_original.pack(anchor='nw', fill=tk.X)
        text_area_original = scrolledtext.ScrolledText(self.root, wrap=tk.WORD, font=(JAPANESE_FONT, 20), height=5, bg='light grey', fg='black')
        text_area_original.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        label_translated = tk.Label(self.root, text=DESTINATION_TEXT, font=('Arial', 10, 'bold'))
        label_translated.pack(anchor='nw', fill=tk.X)
        text_area_translated = scrolledtext.ScrolledText(self.root, wrap=tk.WORD, font=(CHINESE_FONT, 20), height=10, bg='light yellow', fg='black')
        text_area_translated.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        self.text_area_original = text_area_original
        self.text_area_translated = text_area_translated

    def update_text_areas(self, original_text, translated_text):
        self.text_area_original.delete('1.0', tk.END)
        self.text_area_original.insert(tk.INSERT, original_text)

        self.text_area_translated.delete('1.0', tk.END)
        self.text_area_translated.insert(tk.INSERT, translated_text)

    def check_clipboard_change(self):
        time.sleep(0.5)
        clipboard_content = pyperclip.paste()
        if isinstance(clipboard_content, str) and clipboard_content != self.current_clipboard_content:
            if is_japanese_text(clipboard_content):
                self.current_clipboard_content = clipboard_content
                translated_text = translate_text(clipboard_content)
                self.update_text_areas(clipboard_content, translated_text)

    def update_clipboard_content(self):
        self.check_clipboard_change()
        self.root.after(1000, self.update_clipboard_content)


if __name__ == "__main__":
    ClipboardTranslator()