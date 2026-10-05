from tkinter import *
from tkinter import ttk, messagebox
from deep_translator import GoogleTranslator
from transformers import MarianMTModel, MarianTokenizer
from langdetect import detect
from textblob import TextBlob
import speech_recognition as sr
import re

LANGUAGES = {
    'af': 'Afrikaans', 'sq': 'Albanian', 'am': 'Amharic', 'ar': 'Arabic', 'hy': 'Armenian',
    'az': 'Azerbaijani', 'eu': 'Basque', 'be': 'Belarusian', 'bn': 'Bengali', 'bs': 'Bosnian',
    'bg': 'Bulgarian', 'ca': 'Catalan', 'ceb': 'Cebuano', 'ny': 'Chichewa', 'zh-cn': 'Chinese (Simplified)',
    'zh-tw': 'Chinese (Traditional)', 'co': 'Corsican', 'hr': 'Croatian', 'cs': 'Czech',
    'da': 'Danish', 'nl': 'Dutch', 'en': 'English', 'eo': 'Esperanto', 'et': 'Estonian',
    'tl': 'Filipino', 'fi': 'Finnish', 'fr': 'French', 'fy': 'Frisian', 'gl': 'Galician',
    'ka': 'Georgian', 'de': 'German', 'el': 'Greek', 'gu': 'Gujarati', 'ht': 'Haitian Creole',
    'ha': 'Hausa', 'haw': 'Hawaiian', 'iw': 'Hebrew', 'hi': 'Hindi', 'hmn': 'Hmong',
    'hu': 'Hungarian', 'is': 'Icelandic', 'ig': 'Igbo', 'id': 'Indonesian', 'ga': 'Irish',
    'it': 'Italian', 'ja': 'Japanese', 'jw': 'Javanese', 'kn': 'Kannada', 'kk': 'Kazakh',
    'km': 'Khmer', 'ko': 'Korean', 'ku': 'Kurdish (Kurmanji)', 'ky': 'Kyrgyz', 'lo': 'Lao',
    'la': 'Latin', 'lv': 'Latvian', 'lt': 'Lithuanian', 'lb': 'Luxembourgish', 'mk': 'Macedonian',
    'mg': 'Malagasy', 'ms': 'Malay', 'ml': 'Malayalam', 'mt': 'Maltese', 'mi': 'Maori',
    'mr': 'Marathi', 'mn': 'Mongolian', 'my': 'Myanmar (Burmese)', 'ne': 'Nepali', 'no': 'Norwegian',
    'ps': 'Pashto', 'fa': 'Persian', 'pl': 'Polish', 'pt': 'Portuguese', 'pa': 'Punjabi',
    'ro': 'Romanian', 'ru': 'Russian', 'sm': 'Samoan', 'gd': 'Scots Gaelic', 'sr': 'Serbian',
    'st': 'Sesotho', 'sn': 'Shona', 'sd': 'Sindhi', 'si': 'Sinhala', 'sk': 'Slovak',
    'sl': 'Slovenian', 'so': 'Somali', 'es': 'Spanish', 'su': 'Sundanese', 'sw': 'Swahili',
    'sv': 'Swedish', 'tg': 'Tajik', 'ta': 'Tamil', 'te': 'Telugu', 'th': 'Thai',
    'tr': 'Turkish', 'uk': 'Ukrainian', 'ur': 'Urdu', 'uz': 'Uzbek', 'vi': 'Vietnamese',
    'cy': 'Welsh', 'xh': 'Xhosa', 'yi': 'Yiddish', 'yo': 'Yoruba', 'zu': 'Zulu'
}


root = Tk()
root.geometry('1000x450')
root.resizable(0, 0)
root['bg'] = 'black'
root.title('Simple Translator')

Label(root, text="Simple Translator", font="Arial 20 bold", fg='white', bg='black').pack()

# Input and Output Labels
Label(root, text="Input Text", font='arial 13 bold', fg='white', bg='black').place(x=150, y=90)
Label(root, text="Translated Text", font='arial 13 bold', fg='white', bg='black').place(x=730, y=90)

# Input and Output Widgets
Input_text = Entry(root, font='arial 12 bold', width=40)
Input_text.place(x=30, y=130)
Output_text = Text(root, font='arial 12 bold', height=10, wrap=WORD, padx=5, pady=5, width=40)
Output_text.place(x=600, y=130)

# Sentiment Label
sentiment_label = Label(root, text="Sentiment: ", font='arial 10', fg='white', bg='black')
sentiment_label.place(x=30, y=350)

# Language Select Combo_boxes
languages = list(LANGUAGES.values())
source_lang = ttk.Combobox(root, values=languages, width=22)
source_lang.place(x=130, y=180)
source_lang.set('Source Language (Auto)')

dest_lang = ttk.Combobox(root, values=languages, width=22)
dest_lang.place(x=130, y=210)
dest_lang.set('Destination Language')


# Translation function with NLP and ML features
def custom_translate(text, src_lang, tgt_lang):
    try:
        model_name = f'Helsinki-NLP/opus-mt-{src_lang}-{tgt_lang}'
        tokenizer = MarianTokenizer.from_pretrained(model_name)
        model = MarianMTModel.from_pretrained(model_name)
        translated = model.generate(**tokenizer(text, return_tensors="pt", padding=True))
        return tokenizer.decode(translated[0], skip_special_tokens=True)
    except Exception as e:
        messagebox.showerror("Model Error", f"An error occurred with the translation model: {e}")


def detect_language(text):
    return detect(text)


def analyze_sentiment(text):
    blob = TextBlob(text)
    return blob.sentiment.polarity


def translate():
    try:
        src_text = Input_text.get()

        # Detect language if 'Auto' is selected
        if source_lang.get() == 'Source Language (Auto)':
            source_code = detect_language(src_text)
            source_lang.set(LANGUAGES.get(source_code, "Auto-detected"))
        else:
            source_code = list(LANGUAGES.keys())[list(LANGUAGES.values()).index(source_lang.get())]

        dest_code = list(LANGUAGES.keys())[list(LANGUAGES.values()).index(dest_lang.get())]

        # Perform translation
        translation = custom_translate(src_text, source_code, dest_code)

        # Display translation
        Output_text.delete(1.0, END)
        Output_text.insert(END, translation)

        # Sentiment Analysis
        sentiment = analyze_sentiment(src_text)
        sentiment_label.config(
            text=f"Sentiment: {'Positive' if sentiment > 0 else 'Negative' if sentiment < 0 else 'Neutral'}")

    except Exception as e:
        messagebox.showerror("Translation Error", f"An error occurred: {e}")


# Clear text fields
def clear():
    Input_text.delete(0, END)
    Output_text.delete(1.0, END)
    sentiment_label.config(text="Sentiment: ")


# Speech-to-Text function
def speech_to_text():
    if source_lang.get() not in LANGUAGES.values():
        messagebox.showerror("Error", "Please select a valid source language.")
        return

    language_code = list(LANGUAGES.keys())[list(LANGUAGES.values()).index(source_lang.get())]
    recognizer = sr.Recognizer()
    with sr.Microphone(device_index=1) as source:
        messagebox.showinfo("Info", "Speak now...")
        audio = recognizer.listen(source)
        try:
            text = recognizer.recognize_google(audio, language=language_code)
            Input_text.delete(0, END)
            Input_text.insert(END, text)
        except sr.UnknownValueError:
            messagebox.showerror("Error", "Could not understand your speech.")
        except sr.RequestError:
            messagebox.showerror("Error", "Network error.")


# Buttons
trans_btn = Button(root, text='Translate', font='arial 12 bold', pady=5, command=translate, bg='light blue',
                   activebackground='green')
trans_btn.place(x=455, y=130)

clear_btn = Button(root, text='Clear', font='arial 12 bold', pady=5, command=clear, bg='blue',
                   activebackground='light blue')
clear_btn.place(x=455, y=180)

speech_btn = Button(root, text='Speak', font='arial 12 bold', pady=5, command=speech_to_text, bg='orange',
                    activebackground='yellow')
speech_btn.place(x=455, y=230)

root.mainloop()
