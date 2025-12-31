from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI()

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

response = client.responses.create(
    model="gpt-4o-mini",
    instructions=SYSTEM_PROMPT,
    input="Hey, Write a code in python for adding two numbers.",
)

print(response.output_text)