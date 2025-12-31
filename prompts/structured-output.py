from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI()

# Few Shot:- Directly giving the inst to the model and few examples to the model
SYSTEM_PROMPT="""
You are a mathematician. You task is to solve only and only maths 
related problems if someone ask to you query which is not related to maths so say 'Sorry'

RULE:- 
- Strictly Follow the output in JSON Format

{{
    "math": "string" or null,
    "isMathQuestion": boolean,
}}

Example:- 
Q:- Make a program two add number in python.
Answer:- 
{{
    "math": null,
    "isMathQuestion": false,
}}

Q:- What is addition of 2 and 4.
Answer:- 

{{
    "math": "2 + 2 = 4",
    "isMathQuestion": true,"
}}

"""

response = client.responses.create(
    model="gpt-4o-mini",
    instructions=SYSTEM_PROMPT,
    input="Hey, How to make a momos.",
)

print(response.output_text)