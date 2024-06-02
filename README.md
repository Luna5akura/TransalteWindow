# TransalteWindow

The Clipboard Translator is a custom Tkinter-based desktop application that continuously monitors the clipboard for Japanese text, translates it to Chinese, and displays both the original and translated text. Additionally, it provides a feature to read the original Japanese text aloud using a text-to-speech engine. The application also maintains a history of recent translations and allows users to browse through them using a slider.

## Features

1. **Real-Time Clipboard Monitoring**: Automatically detects new Japanese text copied to the clipboard.
2. **Translation**: Translates detected Japanese text to Chinese using the Youdao translation API.
3. **Text-to-Speech**: Reads the original Japanese text aloud using the pyttsx3 library.
4. **Translation History**: Keeps a history of up to 10 recent translations.
5. **Custom Fonts and UI**: Uses specific fonts for Japanese and Chinese text, and a modern dark theme for the UI.

## Dependencies

The application requires the following Python libraries:

- `customtkinter`
- `pyttsx3`
- `threading`
- `pyperclip`
- `requests`
- `hashlib`
- `time`
- `uuid`
- `langdetect`

To install these dependencies, run:

```sh
pip install customtkinter pyttsx3 pyperclip requests langdetect
```


## Configuration

The application uses specific configuration constants:

- `NTH_LANGUAGE_PACK_IN_SYSTEM`: Index of the Japanese language pack in the system's TTS engine.
- `VOICE_RATE`: Speed of the speech.
- `VOICE_VOLUME`: Volume of the speech.
- `PAGEFONT`, `JAPANESE_FONT`, `CHINESE_FONT`: Fonts for various text elements.
- `SOURCE_LAN`, `DESTINATION_LAN`: Language codes for the source (Japanese) and destination (Chinese) languages.
- `ORIGINAL_TEXT`, `DESTINATION_TEXT`: Labels for the original and translated text areas.
- `APP_KEY`, `SECRET_KEY`, `API`: Credentials and endpoint for the Youdao translation API.

## Usage

To run the application, execute the following command in your terminal:

```sh
python clipboard_translator.py
```

## Detailed Functionality

### Clipboard Monitoring

The `try_access_clipboard` function attempts to read the clipboard content, retrying multiple times in case of failure. The `check_clipboard_change` method detects changes in the clipboard content, ensuring new Japanese text is processed and translated.

### Translation

The `translate_text` function sends a request to the Youdao translation API, handling the necessary authentication and parameters to get the translated text.

### Text-to-Speech

The `read_original_text` method initializes the pyttsx3 engine, selects the appropriate Japanese voice, and reads the original text aloud.

### History Management

The application maintains a list of recent translations, updating the UI to reflect the currently selected translation from the history slider.

## User Interface

The UI is built using the `customtkinter` library and includes the following components:
- Labels for original and translated text.
- Text areas for displaying the original Japanese text and translated Chinese text.
- A slider for browsing through the translation history.
- A button to trigger text-to-speech functionality.

### Main UI Setup

```python
def setup_ui(self):
    ...
```

This method initializes the main window, sets up grid configurations, and creates all necessary UI components, including labels, text areas, frames, sliders, and buttons.

### Authors and Acknowledgments

This project was developed by Luna5akura. It uses the Youdao translation API for translations and the pyttsx3 library for text-to-speech functionality. The UI is powered by `customtkinter`.

### License

This project is licensed under the MIT License - see the [MIT License](LICENSE)  file for details.

### Troubleshooting

- Ensure all dependencies are installed.

- Verify the correctness of the APP_KEY and SECRET_KEY for the Youdao translation API.

- Ensure the system's text-to-speech engine has the required Japanese language pack installed.

For any issues or contributions, please open an issue or submit a pull request on GitHub.