from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI()

# Zero Shot:- We give direct instruction to perform some action
SYSTEM_PROMPT="You are a mathematician. You task is to solve only and only maths related problems if someone ask to you query which is not related to maths so say 'Sorry I am not able to answer that.' "

response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        { "role": "system", "content": SYSTEM_PROMPT },
        { "role": "user", "content": "Write a code of adding two number in python." }
    ]
)


print(response.choices[0].message.content)