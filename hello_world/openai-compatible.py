from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(
    api_key="AIzaSyCZJiJ6TdlAFJpXbO67T48Cge611ccyluE",
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

SYSTEM_PROMPT="You are expert in Mathematics. Your task is to perform action only and only related to maths. If user query is not related to mathematics then not answer it and only and only say sorry"


response = client.chat.completions.create(
    model="gemini-2.5-flash",
    messages=[
            {   "role": "system",
                "content": SYSTEM_PROMPT
            },
            {
                "role": "user",
                "content": "What is the weather of meerut!"
            }
        ]
)

print(response.choices[0].message.content)

