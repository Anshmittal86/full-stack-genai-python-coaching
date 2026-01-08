import os
import json
import requests
from dotenv import load_dotenv
from openai import OpenAI
from pathlib import Path
import subprocess
from pydantic import BaseModel, Field
from typing import Optional

load_dotenv()

client = OpenAI()

def get_weather(city: str):
    """ Get current weather info of city """
    print("🔨 Tool Called: get_weather", city)
    
    url = f"https://wttr.in/{city}?format=%C+%t"
    response = requests.get(url)

    if response.status_code == 200:
        return f"The current weather of {city} is {response.text}."
    return "Something went wrong"


def run_shell(input_json: str) -> str: 
    print("🔨 Tool Called: run_shell", json.loads(input_json)["cmd"])
    params = json.loads(input_json)
    cmd = params["cmd"]
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=30)
        output = result.stdout + result.stderr
        return f"Exit code: {result.returncode}\nOutput: {output}"
    except subprocess.TimeoutExpired:
        return "Command timed out"
    except Exception as e:
        return f"Error running command: {str(e)}"


def read_file(file_path: str) -> str:
    """Reads the content of a file at the given path."""
    print("🔨 Tool Called: read_file", file_path)
    try:
        with open(file_path, 'r') as f:
            return f.read()
    except Exception as e:
        return f"Error reading file: {str(e)}"
    

def write_file(input_json: str) -> str:
    print(f"📋 RAW: {repr(input_json[:200])}...") 
    
    try:
        params = json.loads(input_json)
    except json.JSONDecodeError as e:
        return f"❌ JSON Error: {str(e)[:100]}. Input was malformed."
    
    file_path = params.get("file_path")
    content = params.get("content")
    
    if not file_path or content is None:
        return "❌ Missing file_path or content in params"
    
    try:
        Path(file_path).parent.mkdir(parents=True, exist_ok=True)
        with open(file_path, 'w') as f:
            f.write(content)
        return f"✅ File written: {file_path}"
    except Exception as e:
        return f"❌ Write error: {str(e)}"

def list_directory(dir_path: str = ".") -> str:
    """Lists files and directories in the given path."""
    print("🔨 Tool Called: list_directory", dir_path)
    try:
        items = os.listdir(dir_path)
        return "\n".join(items)
    except Exception as e:
        return f"Error listing directory: {str(e)}"


available_tools = {
    "get_weather": get_weather,
    "run_shell": run_shell,
    "read_file": read_file,
    "write_file": write_file,
    "list_directory": list_directory,
}

  

SYSTEM_PROMPT ="""
    You're an expert AI Assistant in resolving user queries using chain of thought. 
    You work on START, PLAN and OUTPUT steps.
    You need to first PLAN what needs to be done. The PLAN can be multiple steps. 
    Once you think enough PLAN has been done, finally you can give an OUTPUT.
    You can also access the tools to solve user query if you need as per available tools.
  
    
    Available Tools:
      - get_weather(city: str): Takes a city name as an input and returns the current weather for the city
      - read_file(file_path: str): Reads content from a file 
      - list_directory(dir_path: str): Lists files in directory
      - write_file(input_json: str): {"file_path": "file.py", "content": "code here"}
      - run_shell(input_json: str): {"cmd": "ls", "cwd": "."}
    
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

class MyOutputSchema(BaseModel):
  step: str = Field(..., description="This is a ID of the step, Example: PLAN | ACTION | OBSERVE | OUTPUT etc.")
  content: Optional[str] = Field(None, description="The optional string for the step.")
  tool: Optional[str] = Field(None, description="The ID of tool to call")
  input: Optional[str] = Field(None, description="The input params for the tool")

  
message_history = [
    {"role": "system", "content": SYSTEM_PROMPT}
]

while True:
    user_query = input("👨: ")
    message_history.append({"role": "user", "content": user_query})

    while True:
        response = client.chat.completions.parse( # parse method to use Validation schema
            model="gpt-4o",
            response_format=MyOutputSchema,
            messages=message_history
        )

        raw_result = response.choices[0].message.content
        message_history.append({"role": "assistant", "content": raw_result})
        
        parsed_result = response.choices[0].message.parsed # parsed by Validation schema
        
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
        
        else:
            print(f"❌ Unknown step: {step}")
            break  

