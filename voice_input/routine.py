import speech_recognition as sr
from gtts import gTTS
import os
import pygame
from datetime import datetime

# Global variable to store the recognized text
recognized_text = ""


def text_to_speech(text):
    # Use Google Text-to-Speech to read the text out loud
    tts = gTTS(text=text, lang='en')
    tts.save('output.mp3')

    # Use pygame for audio playback
    pygame.mixer.init()
    pygame.mixer.music.load('output.mp3')
    pygame.mixer.music.play()

    # Wait for playback to finish
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)


def recognize_speech():
    global recognized_text

    # Initialize the recognizer
    recognizer = sr.Recognizer()

    # Use the microphone with device index 2 as the audio source
    mic_device_index = 2

    while True:
        with sr.Microphone(device_index=mic_device_index) as source:
            print("Waiting for 'Friday'...")
            recognizer.adjust_for_ambient_noise(
                source)  # Adjust for ambient noise

            try:
                # Capture audio from the microphone
                audio_data = recognizer.listen(source, timeout=10)

                print("Recognizing...")

                # Use Google Web Speech API to convert speech to text
                recognized_text = recognizer.recognize_google(audio_data)

                if "Friday" in recognized_text:
                    print(get_current_task())
                    text_to_speech(get_current_task())

                else:
                    print("Waiting for 'Friday'...")

            except sr.UnknownValueError:
                # Silence when it fails to understand during the "Friday" stage
                pass

            except sr.RequestError as e:
                print(
                    f"Could not request results from Google Web Speech API; {e}")

            except sr.WaitTimeoutError:
                print("Listening timed out. Waiting for input again.")


def get_current_task():
    current_time = datetime.now().time()
    formatted_time = current_time.strftime("%H:%M")

    if current_time >= datetime.strptime("09:30", "%H:%M").time() and current_time < datetime.strptime("10:00", "%H:%M").time():
        return f"[{formatted_time}] It's time to Wake up"

    elif current_time >= datetime.strptime("10:00", "%H:%M").time() and current_time < datetime.strptime("11:00", "%H:%M").time():
        return f"[{formatted_time}] It's time for Breakfast and relaxation"

    elif current_time >= datetime.strptime("11:00", "%H:%M").time() and current_time < datetime.strptime("13:00", "%H:%M").time():
        return f"[{formatted_time}] It's time for Study session 1"

    elif current_time >= datetime.strptime("13:00", "%H:%M").time() and current_time < datetime.strptime("14:00", "%H:%M").time():
        return f"[{formatted_time}] It's time for Lunch and some break"

    elif current_time >= datetime.strptime("14:00", "%H:%M").time() and current_time < datetime.strptime("16:00", "%H:%M").time():
        return f"[{formatted_time}] It's your Free time. Go nuts"

    elif current_time >= datetime.strptime("16:00", "%H:%M").time() and current_time < datetime.strptime("18:00", "%H:%M").time():
        return f"[{formatted_time}] It's time for Study session 2"

    elif current_time >= datetime.strptime("18:00", "%H:%M").time() and current_time < datetime.strptime("19:00", "%H:%M").time():
        return f"[{formatted_time}] It's time for Snack and some break"

    elif current_time >= datetime.strptime("19:00", "%H:%M").time() and current_time < datetime.strptime("21:00", "%H:%M").time():
        return f"[{formatted_time}] It's time for Study session 3"

    elif current_time >= datetime.strptime("21:00", "%H:%M").time() and current_time < datetime.strptime("23:00", "%H:%M").time():
        return f"[{formatted_time}] It's your Free time. Go nuts"

    elif current_time >= datetime.strptime("23:00", "%H:%M").time() or current_time < datetime.strptime("01:00", "%H:%M").time():
        return f"[{formatted_time}] It's time for Dinner and some break"

    elif current_time >= datetime.strptime("01:00", "%H:%M").time() and current_time < datetime.strptime("09:30", "%H:%M").time():
        return f"[{formatted_time}] It's your Free time. Go nuts"

    else:
        return f"[{formatted_time}] It's time for Sleep"


if __name__ == "__main__":
    recognize_speech()
