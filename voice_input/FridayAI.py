import google.generativeai as genai
import os
import speech_recognition as sr
from gtts import gTTS
import pygame
from dotenv import load_dotenv
import time

# Load environment variables
load_dotenv()
YOUR_API_KEY = os.getenv('YOUR_API_KEY')

genai.configure(api_key=YOUR_API_KEY)

# Set up the model
generation_config = {
    "temperature": 0.9,
    "top_p": 1,
    "top_k": 1,
    "max_output_tokens": 2048,
}
safety_settings = [
    {"category": "HARM_CATEGORY_HARASSMENT",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_HATE_SPEECH",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_DANGEROUS_CONTENT",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
]
model = genai.GenerativeModel(
    model_name="gemini-pro",
    generation_config=generation_config,
    safety_settings=safety_settings
)

def ai_stream_reply(prompt_parts):
    response = model.generate_content(prompt_parts, stream=True)
    for chunk in response:
        print(chunk.text, end="", flush=True)
        text = chunk.text
        text = text.replace('•', '  *')
        text_to_speech(text)

def recognize_speech_long(recognizer, source):
    goon = True
    while goon:
        try:
            # Change the timeout for the next listen to a longer duration
            audio_data = recognizer.listen(source, timeout=60)
            recognized_text = recognizer.recognize_google(audio_data)
            if recognized_text:
                print("You asked:", recognized_text)

                # Send the recognized text to OpenAI
                if recognized_text != "Friday":

                    # Get user input for the prompt
                    user_prompt = recognized_text

                    # Define the role and parts for the prompt
                    prompt_parts = ["instruction: 'you are getting a voice input as text so if the text from the user doesnt finsih the sentence properly just ask the user `sorry but can you say that again?` nothing alse","instruction: always answer me with in 100 words only.", user_prompt]

                    # Generate content using the user-provided prompt
                    ai_stream_reply(prompt_parts)
                    text_to_speech("Anyting alse?")

                # Use Google Text-to-Speech to read the response out loud

            else:
                print("No input received. Waiting for input again.")
                goon = False

        except sr.UnknownValueError:
            # Different behavior for UnknownValueError during long input stage
            print("Could not understand audio during long input. Try again.")
            goon = False

        except sr.RequestError as e:
            print(f"Could not request results from Google Web Speech API; {e}")
            goon = False
        except sr.WaitTimeoutError:
            print("Listening timed out. Waiting for input again.")
            goon = False


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
