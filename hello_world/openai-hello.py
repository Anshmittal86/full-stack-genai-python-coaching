from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI()

response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        { "role": "system", "content": "You are a helpful assistant." },
        { "role": "user", "content": "Hello? How are you!" }
    ]
)

print(response.choices[0].message.content)