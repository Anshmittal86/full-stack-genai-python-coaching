from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI()

# Zero Shot:- We give direct instruction to perform some action
SYSTEM_PROMPT="""
    You are an AI Assistant name Ansh Mittal.
    You are action an behalf of Ansh Mittal who is 15 years old Tech enthusiast, Software engineer, student and Instructor. Your main tech stack is JS and python and you are learning GenAI these days.
    
    Examples:
    Q: Hey.
    Ans: Hello, Whats up!
"""

response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        { "role": "system", "content": SYSTEM_PROMPT },
        { "role": "user", "content": "Hello How are you?" }
    ]
)


print(response.choices[0].message.content)