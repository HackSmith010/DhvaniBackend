import speech_recognition as sr
import cv2
import os
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

# Download necessary NLTK data
nltk.download('punkt_tab')
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('averaged_perceptron_tagger')
nltk.download('wordnet')

# Directory where sign language videos are stored
# '' = 'assets'  # Adjust this path to where your videos are stored

def recognize_speech_from_mic():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Please speak something...")
        audio_data = recognizer.listen(source, timeout=7, phrase_time_limit=10)

        try:
            text = recognizer.recognize_google(audio_data)
            print(f"Recognized Text: {text}")
            return text.lower()
        except sr.UnknownValueError:
            print("Sorry, I could not understand the audio.")
            return None
        except sr.RequestError as e:
            print(f"Could not request results from Google Speech Recognition service; {e}")
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
        video_path = os.path.join('', f"{word}.mp4")
        if not os.path.exists(video_path):
            print(f"No video found for word: {word}, splitting into characters.")
            for char in word:
                char_video_path = os.path.join('', f"{char}.mp4")
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

    # Initialize background subtractor
    # back_sub = cv2.createBackgroundSubtractorMOG2()

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        # Apply background subtraction
        # fg_mask = back_sub.apply(frame)

        # Optionally, you can perform additional processing to refine the mask
        # E.g., applying morphological operations to remove noise

        cv2.imshow('Sign Language', frame)

        if cv2.waitKey(40) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    while True:
        text = recognize_speech_from_mic()
        if text:
            words = process_text(text)
            play_sign_language_videos(words)
        else:
            print("Try speaking again.")
