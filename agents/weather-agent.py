import json
import requests

from dotenv import load_dotenv
from openai import OpenAI

from pydantic import BaseModel,Field
from typing import Optional

load_dotenv()

client = OpenAI()

def get_weather(city: str):
    print("🔨 Tool Called: get_weather", city)
    
    url = f"https://wttr.in/{city}?format=%C+%t"
    response = requests.get(url)

    if response.status_code == 200:
        return f"The current weather of {city} is {response.text}."
    return "Something went wrong"

class MySchema(BaseModel):
    step: str = Field(..., description="This is ID for identification what ai step perform")
    content: Optional[str] = Field(None, description="This is content given by the ai")
    tool: Optional[str] = Field(None, description="The ID of tool to call")
    input: Optional[str] = Field(None, description="The input params for the tool")

available_tools = {
    "get_weather": get_weather
}

SYSTEM_PROMPT ="""
    You're an expert AI Assistant in resolving user queries using chain of thought. 
    You work on START, PLAN and OUTPUT steps.
    You need to first PLAN what needs to be done. The PLAN can be multiple steps. 
    Once you think enough PLAN has been done, finally you can give an OUTPUT.
    You can also access the tools to solve user query if you need as per available tools.
  
    
    Available Tools:
      - get_weather(city: str): Takes a city name as an input and returns the current weather for the city
    
    Rules:
    - Strictly Follow the given JSON output format
    - Only run one step at a time
    - The sequence of steps is START ( Where user gives an input), PLAN ( That can be multiple times), ACTION ( function calling based on the user query ), OBSERVE (understand the tool result) and finally OUTPUT ( which is going to the displayed to the user.)
    
    Output JSON Format:
    {
        "step": "string",
        "content": "string",
        "tool": "The name of function if the step is action",
        "input": "The input parameter for the function",
    }
    
    Example:
    Q: Hey, Can you solve 2 + 3 * 5 / 10
    START: Hey, Can you solve 2 + 3 * 5 / 10
    PLAN: { "step": "PLAN", "content": "Seems, like user is interested in math problem." }
    PLAN: { "step": "PLAN", "content": "looking at the problem, we should solve this using BODMAS method." }
    PLAN: { "step": "PLAN", "content": "Yes, The BODMAS is correct think to done here." }
    PLAN: { "step": "PLAN", "content": "first we must multiply 3 * 5 which is 15." }
    PLAN: { "step": "PLAN", "content": "Now the new equation is 2 + 15 / 10" }
    PLAN: { "step": "PLAN", "content": "We must perform divide that is 15 / 10 = 1.5" }
    PLAN: { "step": "PLAN", "content": "Now, the equation is 2 + 1.5" }
    PLAN: { "step": "PLAN", "content": "Now finally lets perform the addition of 2 + 1.5 which is 3.5" }
    PLAN: { "step": "PLAN", "content": "Great, we have solved and finally left with 3.5 as answer." }
    OUTPUT: { "step": "OUTPUT", "content": "3.5" }
    
    Example:
    Q: What is the weather of Delhi
    START: What is the weather of Delhi
    PLAN: { "step": "PLAN", "content": "Seems, like user is interested in weather report." }
    PLAN: { "step": "PLAN", "content": "First I have to see the list of available tools to check that any tool available for solving this query." }
    PLAN: { "step": "PLAN", "content": "Yes, We have a tool of get_weather to get the current info of weather based on city name." }
    PLAN: { "step": "PLAN", "content": "Now, I have to check how many parameters it should accepts." }
    PLAN: { "step": "PLAN", "content": "Ok, the tool of get_weather accept only one parameter which is city name to find the latest weather report." }
    ACTION: { "step": "ACTION", "tool": "get_weather", "input": "delhi" }
    OBSERVE: { "step": "OBSERVE", "tool": "get_weather", "output": "the weather of delhi is 25 C" }
    PLAN: { "step": "PLAN", "content": "Ok, The current weather of delhi is 25 C" }
    OUTPUT: { "step": "OUTPUT", "content": "The weather of delhi is 25 C" }
"""

message_history = [
    {"role": "system", "content": SYSTEM_PROMPT}
]

while True:
    user_query = input("👨: ")
    message_history.append({"role": "user", "content": user_query})

    while True:
        response = client.chat.completions.parse(
            model="gpt-4o-mini",
            response_format=MySchema,
            messages=message_history
        )

        raw_result = response.choices[0].message.content
        message_history.append({"role": "assistant", "content": raw_result})
        
        parsed_result = response.choices[0].message.parsed

        step = parsed_result.step
        content = parsed_result.content

        if step == "START":
            print(f"🔥: {content}")
            continue

        if step == "PLAN":
            print(f"🧠: {content}")
            continue
          
        if step == "ACTION":
            tool_name = parsed_result.tool
            tool_input = parsed_result.input
            print(f"🔨: Tool Name: {tool_name}, Input: {tool_input}")

            if available_tools.get(tool_name, False) != False:
                tool_output = available_tools[tool_name](tool_input)
                print(f"🔨: Tool Name: {tool_name}, Output: {tool_output}")
                
                message_history.append({"role": "assistant", "content": json.dumps({ "step": "OBSERVE", "input": tool_input, "output": tool_output })})
                continue
                

        if step == "OUTPUT":
            print(f"🤖: {content}")
            break   # exit inner loop after final answer