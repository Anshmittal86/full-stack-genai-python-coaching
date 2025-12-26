from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI()

response = client.responses.create(
    model="gpt-5.2",
    input="Hello, How are You?"
)

print(response.output_text)

