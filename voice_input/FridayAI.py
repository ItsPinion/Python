import os
import speech_recognition as sr
from gtts import gTTS
import pygame
import openai
from dotenv import load_dotenv
import time

# Load environment variables
load_dotenv()
OPENAI_KEY = os.getenv('OPENAI_KEY')

# Initialize OpenAI
client = openai.OpenAI(api_key="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")

# Global variable to store the recognized text
recognized_text = "hi"
response = {}

def recognize_speech_long(recognizer, source):
    global recognized_text

    try:
        # Change the timeout for the next listen to a longer duration
        audio_data = recognizer.listen(source, timeout=10)
        recognized_text = recognizer.recognize_google(audio_data)
        if recognized_text:
            print("You asked:", recognized_text)
            
            # Send the recognized text to OpenAI
            if recognized_text != "Friday":
                global response
                response = client.completions.create(
                    model="text-davinci-003",
                    prompt=recognized_text,
                    max_tokens=60
                )

            # Use Google Text-to-Speech to read the response out loud
            text_to_speech(response.choices[0].text.strip() or "sorry, can not!")

            # Add a delay of 5 seconds between requests
            time.sleep(5)

        else:
            print("No input received. Waiting for input again.")

    except sr.UnknownValueError:
        # Different behavior for UnknownValueError during long input stage
        print("Could not understand audio during long input. Try again.")
        text_to_speech("Could not understand. Try again.")

    except sr.RequestError as e:
        print(f"Could not request results from Google Web Speech API; {e}")

    except sr.WaitTimeoutError:
        print("Listening timed out. Waiting for input again.")


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
                    print("You said:", recognized_text)
                    text_to_speech("How can I assist you today?")
                    recognize_speech_long(recognizer, source)

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


if __name__ == "__main__":
    recognize_speech()
