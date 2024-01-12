import concurrent.futures
import google.generativeai as genai
import os
import speech_recognition as sr
from gtts import gTTS
import pygame
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
YOUR_API_KEY = os.getenv('YOUR_API_KEY')

genai.configure(api_key=YOUR_API_KEY)

# Set up the model
generation_config = {
    "temperature": 0.9,
    "top_p": 1,
    "top_k": 1,
    "max_output_tokens": 400,
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
    
    # Use concurrent.futures to process chunks in parallel
    with concurrent.futures.ThreadPoolExecutor() as executor:
        output_files = list(executor.map(process_chunk, response))
    
    # Play the generated files sequentially
    play_files(output_files)

def process_chunk(chunk):
    text = chunk.text.replace('•', '  *')
    tts = gTTS(text=text, lang='en')
    output_file = f'output_{hash(chunk)}.mp3'
    tts.save(output_file)
    return output_file

def play_files(output_files):
    pygame.mixer.init()

    for file in output_files:
        pygame.mixer.music.load(file)
        pygame.mixer.music.play()

        # Wait for playback to finish
        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)

def recognize_speech_long(recognizer, source):
    goon = True
    while goon:
        try:
            audio_data = recognizer.listen(source, timeout=60)
            recognized_text = recognizer.recognize_google(audio_data)
            if recognized_text:
                print("You asked:", recognized_text)
                user_prompt = recognized_text
                prompt_parts = [user_prompt]
                ai_stream_reply(prompt_parts)
                print("\nAnything else?")
                text_to_speech("Anything else?")
                    

            else:
                print("No input received. Waiting for input again.")
                goon = False

        except sr.UnknownValueError:
            print("Could not understand audio during long input. Try again.")
            goon = False

        except sr.RequestError as e:
            print(f"Could not request results from Google Web Speech API; {e}")
            goon = False
        except sr.WaitTimeoutError:
            print("Listening timed out. Waiting for input again.")
            goon = False

def text_to_speech(text):
    tts = gTTS(text=text, lang='en')
    tts.save('output.mp3')
    pygame.mixer.init()
    pygame.mixer.music.load('output.mp3')
    pygame.mixer.music.play()

    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)

def recognize_speech():
    recognizer = sr.Recognizer()
    mic_device_index = 2

    while True:
        with sr.Microphone(device_index=mic_device_index) as source:
            print("Waiting for 'Friday'...")
            recognizer.adjust_for_ambient_noise(source)

            try:
                audio_data = recognizer.listen(source, timeout=10)
                print("Recognizing...")
                recognized_text = recognizer.recognize_google(audio_data)

                if "Friday" in recognized_text:
                    print("You said:", recognized_text)
                    text_to_speech("How can I assist you today?")
                    recognize_speech_long(recognizer, source)

                else:
                    print("Waiting for 'Friday'...")

            except sr.UnknownValueError:
                pass

            except sr.RequestError as e:
                print(f"Could not request results from Google Web Speech API; {e}")

            except sr.WaitTimeoutError:
                print("Listening timed out. Waiting for input again.")

if __name__ == "__main__":
    recognize_speech()
