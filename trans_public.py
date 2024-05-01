import customtkinter as ctk
import pyttsx3
import threading
import pyperclip
import requests
import hashlib
import time
import uuid
from langdetect import detect, DetectorFactory

NTH_LANGUAGE_PACK_IN_SYSTEM = 2
VOICE_RATE = 130  # words per minute
VOICE_VOLUME = 0.8  # [0.0,1.0]

PAGEFONT = 'Futura Std'
JAPANESE_FONT = 'DFSoGei-W5'
CHINESE_FONT = 'Aa我有点方'

SOURCE_LAN = 'ja'
DESTINATION_LAN = 'zh-cn'

ORIGINAL_TEXT = "Original (Japanese):"
DESTINATION_TEXT = "Translated (Chinese):"

APP_KEY = ''
SECRET_KEY = ''
API = ""

DetectorFactory.seed = 0


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
    appKey = APP_KEY
    secretKey = SECRET_KEY
    salt = str(uuid.uuid4())
    curtime = str(int(time.time()))

    signStr = appKey + truncate(text) + salt + curtime + secretKey
    sign = hashlib.sha256(signStr.encode('utf-8')).hexdigest()

    params = {
        'q': text,
        'from': src,
        'to': dest,
        'appKey': appKey,
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
        self.is_speaking = False
        self.read_button = None
        self.history_slider = None
        self.text_area_original = None
        self.text_area_translated = None
        self.current_clipboard_content = ""
        self.translation_history = []
        self.root = ctk.CTk()
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        self.setup_ui()
        self.update_clipboard_content()
        self.root.mainloop()

    def setup_ui(self):
        self.root.title("Clipboard Translator")
        self.root.geometry('600x500')

        self.root.grid_rowconfigure(1, weight=1)
        self.root.grid_rowconfigure(3, weight=1)
        self.root.grid_columnconfigure(0, weight=1)

        label_original = ctk.CTkLabel(self.root, text=ORIGINAL_TEXT, font=(PAGEFONT, 15), corner_radius=15)
        label_original.grid(row=0, column=0, sticky='nsew')

        original_frame = ctk.CTkFrame(self.root)
        original_frame.grid(row=1, column=0, sticky='nsew')
        original_frame.grid_columnconfigure(0, weight=1)
        self.text_area_original = ctk.CTkTextbox(original_frame, wrap='word', font=(JAPANESE_FONT, 30), height=5)
        self.text_area_original.grid(row=0, column=0, padx=10, pady=5, sticky='nsew')
        scrollbar_original = ctk.CTkScrollbar(original_frame, command=self.text_area_original.yview)
        scrollbar_original.grid(row=0, column=1)
        self.text_area_original.configure(yscrollcommand=scrollbar_original.set)

        label_translated = ctk.CTkLabel(self.root, text=DESTINATION_TEXT, font=(PAGEFONT, 15), corner_radius=15)
        label_translated.grid(row=2, column=0, sticky='nsew')

        translated_frame = ctk.CTkFrame(self.root)
        translated_frame.grid(row=3, column=0, sticky='nsew')
        translated_frame.grid_columnconfigure(0, weight=1)
        self.text_area_translated = ctk.CTkTextbox(translated_frame, wrap='word', font=(CHINESE_FONT, 30), height=5)
        self.text_area_translated.grid(row=0, column=0, padx=10, pady=5, sticky='nsew')
        scrollbar_translated = ctk.CTkScrollbar(translated_frame, command=self.text_area_translated.yview)
        scrollbar_translated.grid(row=0, column=1)
        self.text_area_translated.configure(yscrollcommand=scrollbar_translated.set)

        control_frame = ctk.CTkFrame(self.root)
        control_frame.grid(row=4, column=0, sticky='nsew')
        control_frame.grid_columnconfigure(0, weight=1)

        self.history_slider = ctk.CTkSlider(control_frame, from_=0, to=100,
                                            number_of_steps=len(self.translation_history) - 1,
                                            command=self.on_history_scroll)
        self.history_slider.grid(row=0, column=0, padx=10, pady=5, sticky='nsew')

        self.read_button = ctk.CTkButton(control_frame, font=(PAGEFONT, 15), text="Read Original",
                                         command=self.read_original_text)
        self.read_button.grid(row=0, column=1, padx=10, pady=5, sticky='nsew')

    def read_original_text(self):
        if self.is_speaking:
            return

        def speak():
            self.is_speaking = True
            engine = pyttsx3.init()
            voices = engine.getProperty('voices')
            japanese_voice = next((voice for voice in voices if 'ja' in voice.languages), None)
            if japanese_voice:
                engine.setProperty('voice', japanese_voice.id)
            engine.setProperty('rate', 150)
            engine.setProperty('volume', 0.8)
            original_text = self.text_area_original.get("1.0", "end-1c")
            engine.say(original_text)
            engine.runAndWait()
            self.is_speaking = False

        thread = threading.Thread(target=speak)
        thread.start()

    def on_history_scroll(self, value):
        index = int(value)
        if 0 <= index < len(self.translation_history):
            original_text, translated_text = self.translation_history[index].split(' -> ')
            self.update_text_areas(original_text, translated_text)

    def update_text_areas(self, original_text, translated_text):
        self.text_area_original.delete('1.0', 'end')
        self.text_area_original.insert('insert', original_text)
        self.text_area_translated.delete('1.0', 'end')
        self.text_area_translated.insert('insert', translated_text)

    def update_history_list(self, original_text, translated_text):
        entry = f"{original_text} -> {translated_text}"
        if len(self.translation_history) >= 10:
            self.translation_history.pop(0)  # Remove the oldest entry
        self.translation_history.append(entry)
        self.history_slider.configure(to=len(self.translation_history) - 1)  # Update the slider's range

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
