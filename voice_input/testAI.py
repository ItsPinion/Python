import google.generativeai as genai

YOUR_API_KEY = "AIzaSyD40HwFaxMW0URyCsdI5In7ZmI3p9sFhKo"

genai.configure(api_key=YOUR_API_KEY)

# Set up the model
generation_config = {
    "temperature": 0.9,
    "top_p": 1,
    "top_k": 1,
    "max_output_tokens": 2048,
}

safety_settings = [
    {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
]

model = genai.GenerativeModel(
    model_name="gemini-pro",
    generation_config=generation_config,
    safety_settings=safety_settings
)

# Get user input for the prompt
user_prompt = input("Enter your prompt: ")

# Define the role and parts for the prompt
prompt_parts = [user_prompt]

# Generate content using the user-provided prompt
response = model.generate_content(user_prompt,stream=True)
for chunk in response:
  print(chunk.text, end="", flush=True)
print("\n")
  
