from dotenv import load_dotenv
from openai import OpenAI

import json
load_dotenv()

client = OpenAI(
    api_key="PASTE_YOUR_GEMINI_API_KEY_HERE",
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)



SYSTEM_PROMPT ="""
    You're an expert AI Assistant in resolving user queries using chain of thought. 
    You work on START, PLAN and OUTPUT steps.
    You need to first PLAN what needs to be done. The PLAN can be multiple steps. 
    Once you think enough PLAN has been done, finally you can give an OUTPUT.
    
    Rules:
    - Strictly Follow the given JSON output format
    - Only run one step at a time
    - The sequence of steps is START ( Where user gives an input), PLAN ( That can be multiple times) and finally OUTPUT ( which is going to the displayed to the user.)
    
    Output JSON Format:
    { "step": "START" | "PLAN" | "OUTPUT", "content": "string" }
    
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
    PLAN: { "step": "OUTPUT", "content": "3.5" }
"""

response = client.chat.completions.create(
    model="gemini-2.5-flash",
    response_format={ "type": "json_object" },
    messages=[
        { "role": "system", "content": SYSTEM_PROMPT },
        { "role": "user", "content": "Hey, write a code to add n number is js" },
        { "role": "assistant", "content": json.dumps({"step": "START", "content": "Hey, write a code to add n number is js"})},
        { "role": "assistant", "content": json.dumps({"step": "PLAN","content": "The user wants a JavaScript code to add 'n' numbers. This implies creating a function that can take multiple numbers or an array of numbers and return their sum."})},
        { "role": "assistant", "content": json.dumps({"step": "PLAN", "content": "I will define a JavaScript function. This function will use rest parameters (...numbers) to accept any number of arguments. Inside the function, I will use the 'reduce' array method to calculate the sum of all provided numbers. Finally, I will provide the complete code with an example usage."})},
        { "role": "assistant", "content": json.dumps({"step": "OUTPUT", "content": "```javascript\nfunction addNumbers(...numbers) {\n  // The 'numbers' parameter will be an array of all arguments passed to the function.\n  // We use the 'reduce' method to sum all elements in the array.\n  // 'accumulator' holds the running total, 'currentNumber' is the current element.\n  // 0 is the initial value for the accumulator.\n  return numbers.reduce((accumulator, currentNumber) => accumulator + currentNumber, 0);\n}\n\n// --- Example Usage ---\n\n// Adding a few numbers\nconst sum1 = addNumbers(1, 2, 3, 4, 5);\nconsole.log(\"Sum of 1, 2, 3, 4, 5:\", sum1); // Output: 15\n\n// Adding more numbers\nconst sum2 = addNumbers(10, 20, 30, 40, 50, 60, 70);\nconsole.log(\"Sum of 10, 20, 30, 40, 50, 60, 70:\", sum2); // Output: 280\n\n// Adding no numbers (returns initial accumulator value, which is 0)\nconst sum3 = addNumbers();\nconsole.log(\"Sum of no numbers:\", sum3); // Output: 0\n\n// Adding a single number\nconst sum4 = addNumbers(100);\nconsole.log(\"Sum of 100:\", sum4); // Output: 100\n\n// You can also pass an array using the spread operator if needed\nconst arrayOfNumbers = [11, 22, 33];\nconst sum5 = addNumbers(...arrayOfNumbers);\nconsole.log(\"Sum of numbers from an array:\", sum5); // Output: 66\n```"})},
        
    ]
)

print(response.choices[0].message.content)