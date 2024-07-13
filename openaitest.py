
# Example of a chat completion with OpenAI
# Make sure to install the openai package: pip install openai

import openai

# Set up OpenAI API key
openai.api_key = "os.getenv('API_KEY')"

# Prepare the messages
messages = [
    {"role": "system", "content": "You are a helpful assistant."},
    {"role": "user", "content": "What is the capital of France?"},
]

# Send the request
response = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=messages
)

# Print the response
print("Assistant:", response.choices[0]['message']['content'])
