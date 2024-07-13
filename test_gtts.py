import os
import openai
import speech_recognition as sr
from gtts import gTTS

# Set up OpenAI API key
openai.api_key = os.getenv('OPENAI_API_KEY')

response = openai.ChatCompletion.create(
    model="gpt-4",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Say this is a test."},
    ]
)
print(response.choices[0].message['content'])
