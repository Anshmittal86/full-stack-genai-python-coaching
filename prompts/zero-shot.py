from google import genai
from dotenv import load_dotenv
from google.genai import types

load_dotenv()

client = genai.Client()


# Zero Shot:- We give direct instruction to perform some action

SYSTEM_PROMPT="You are expert in Mathematics. Your task is to perform action only and only related to maths. If user query is not related to mathematics then not answer it and only and only say sorry"

response = client.models.generate_content(
    model="gemini-2.5-flash",
    config=types.GenerateContentConfig(
    system_instruction=SYSTEM_PROMPT),
    contents='what is the weather of Muzaffarnagar!'
)

print(response.text)