from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI()

response = client.responses.create(
    model="gpt-5-nano",
    input="Hello, How are You?Who are you?",
)

print(response.output_text)

