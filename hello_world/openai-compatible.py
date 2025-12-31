from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(
    api_key="PASTE_YOUR_GEMINI_API_KEY_HERE",
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

response = client.chat.completions.create(
    model="gemini-2.5-flash",
    messages=[
        { "role": "system", "content": "You are a helpful assistant." },
        { "role": "user", "content": "Hello? How are you!" }
    ]
)

print(response.choices[0].message.content)