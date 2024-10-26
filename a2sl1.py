import speech_recognition as sr
import cv2
import os
import nltk
import tkinter as tk
from tkinter import messagebox
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

nltk.download('punkt')
nltk.download('stopwords')
nltk.download('averaged_perceptron_tagger')
nltk.download('wordnet')

# Directory where sign language videos are stored
VIDEO_DIR = ''  # Adjust this path to where your videos are stored

def recognize_speech_from_mic():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        # Adjust for ambient noise to reduce delay
        recognizer.adjust_for_ambient_noise(source, duration=0.5)
        print("Please speak something...")

        try:
            # Reduced timeout and phrase_time_limit to make recognition faster
            audio_data = recognizer.listen(source, timeout=3, phrase_time_limit=5)
            text = recognizer.recognize_google(audio_data)
            print(f"Recognized Text: {text}")
            return text.lower()
        except sr.UnknownValueError:
            print("Sorry, I could not understand the audio.")
            return None
        except sr.RequestError as e:
            print(f"Could not request results from Google Speech Recognition service; {e}")
            return None
        except sr.WaitTimeoutError:
            print("Listening timed out while waiting for phrase to start.")
            return None


def process_text(text):
    words = word_tokenize(text)
    stop_words = set(stopwords.words('english'))
    lemmatizer = WordNetLemmatizer()

    filtered_text = []
    for word in words:
        if word not in stop_words:
            filtered_text.append(lemmatizer.lemmatize(word))

    return filtered_text

def play_sign_language_videos(words):
    for word in words:
        video_path = os.path.join(VIDEO_DIR, f"{word}.mp4")
        if not os.path.exists(video_path):
            print(f"No video found for word: {word}, splitting into characters.")
            for char in word:
                char_video_path = os.path.join(VIDEO_DIR, f"{char}.mp4")
                if os.path.exists(char_video_path):
                    play_video(char_video_path)
                else:
                    print(f"No video found for character: {char}")
        else:
            play_video(video_path)

def play_video(video_path):
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print(f"Error opening video file: {video_path}")
        return

   
    screen_res = (1366, 768) 
    screen_width, screen_height = screen_res

    video_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    video_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))


    x = (screen_width - video_width) // 2
    y = (screen_height - video_height) // 2

    cv2.namedWindow('Sign Language', cv2.WINDOW_NORMAL)
    cv2.moveWindow('Sign Language', x, y)

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        cv2.imshow('Sign Language', frame)

        if cv2.waitKey(40) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()


def on_audio_input():
    text = recognize_speech_from_mic()
    if text:
        words = process_text(text)
        play_sign_language_videos(words)
    else:
        messagebox.showerror("Error", "Could not recognize any speech. Please try again.")

def on_text_input():
    text = text_input.get("1.0", tk.END).strip()
    if text:
        words = process_text(text)
        play_sign_language_videos(words)
    else:
        messagebox.showerror("Error", "No text entered. Please enter some text.")

# Tkinter GUI
root = tk.Tk()
root.title("Speech-to-Sign Language Converter")

audio_button = tk.Button(root, text="Convert Speech to Sign Language", command=on_audio_input)
audio_button.pack(pady=10)

text_label = tk.Label(root, text="Or enter text below:")
text_label.pack()

text_input = tk.Text(root, height=5, width=40)
text_input.pack(pady=10)

text_button = tk.Button(root, text="Convert Text to Sign Language", command=on_text_input)
text_button.pack(pady=10)

root.mainloop()
