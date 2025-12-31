from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI()

# Zero Shot:- We give direct instruction to perform some action
SYSTEM_PROMPT="You are a mathematician. You task is to solve only and only maths related problems if someone ask to you query which is not related to maths so say 'Sorry I am not able to answer that.' "

response = client.responses.create(
    model="gpt-5-nano",
    instructions=SYSTEM_PROMPT,
    input="What is square root of 5",
)

print(response.output_text)