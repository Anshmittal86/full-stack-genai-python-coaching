from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(
    api_key="PASTE_YOUR_GEMINI_API_KEY_HERE",
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

# Few Shot:- Directly giving the inst to the model and few examples to the model
SYSTEM_PROMPT="""
You are a mathematician. You task is to solve only and only maths 
related problems if someone ask to you query which is not related to maths so say 'Sorry'

Example:- 
Q:- Write a code of adding two number in python.
Answer:- Sorry

Q:- What is addition of 2 and 4.
Answer:- 2 + 4 = 6
"""

response = client.chat.completions.create(
    model="gemini-2.5-flash",
    messages=[
        { "role": "system", "content": SYSTEM_PROMPT },
        { "role": "user", "content": "Write a code of adding two number in python." }
    ]
)

print(response.choices[0].message.content)