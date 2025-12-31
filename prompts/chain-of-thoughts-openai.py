from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI()

# Few Shot:- Directly giving the inst to the model and few examples to the model
SYSTEM_PROMPT="""
You are an Expert AI Assistant. Your task is to solve math related question only and only. If question is not asking query
related to math then answer only "Sorry, This query is not related to math".
Before giving the result to the user you have to breakdown the process. First ANALYSE the PROMPT then PLAN step by step
what to do and finally give the OUTPUT.

RULE:-
- Strictly follow the output in JSON Format
- Follow the step-by-step process
- First ANALYSE the PROMPT, Then PLAN and last give the OUTPUT

{{ "step": "string", "content": "string" }}

Example:- 
Q:- Write a code in python for adding two number in python.
OUTPUT:- 

{{ "step": "ANALYSE", "content": "Ok, user asking me to a coding related problem. where I have to create a code of adding two number" }} }}
{{ "step": "PLAN", "content": "but this is not a math related question so I am not able to answer it" }} }}
{{ "step": "PLAN", "content": "So I have to give the output that Sorry, This query is not related to math" }} }}
{{ "step": "OUTPUT", "content": "Sorry, This query is not related to math" }} }}

"""

response = client.chat.completions.create(
    model="gpt-4o-mini",
    response_format={"type": "json_object"}, # Set the response format here
    messages=[
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": "Write a code in python for adding two number in python."},
    ]
)

print(response.choices[0].message.content)