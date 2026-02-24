import json
import os
from dotenv import load_dotenv
from openai import OpenAI
import requests
from pydantic import BaseModel, Field
from typing import Optional

load_dotenv()
client = OpenAI(
    api_key=os.environ["GOOGLE_API_KEY"],
    base_url="https://generativelanguage.googleapis.com/v1beta"
)

def get_weather_info(location: str) -> str:
    url = f"https://wttr.in/{location.lower()}?format=%C+%t"
    response = requests.get(url)
    if response.status_code == 200:
        return f"Current weather in {location} is : {response.text.strip()}"
    
    return f"Something went wrong in getting weather info for {location}"

SYSTEM_PROMPT = '''
    You are an expert assistant in resolving user queries using chain of thought (CoT) prompting. 
    When a user asks a question, you will first break down the question into smaller sub-questions or steps, 
    and then provide a final answer based on the reasoning process.
    You work on START, PLAN, TOOL & OUTPUT steps.
    - START: You will start by understanding the question and identifying the key components.
    - PLAN: You will then create a plan to solve the question by breaking it down into smaller sub-questions or steps.
    - TOOL: If needed, you will use a tool from available tools to gather additional information
    - OUTPUT: Finally, you will provide the final answer based on the reasoning process.
    For every tool call, wait for the observe step to get the output of the tool before proceeding to the next step in the plan.
    
    Rules:
    - Stritly follow the format of the answer in JSON.
    - Only run one step at a time
    - The sequence of steps should be START -> PLAN -> TOOL -> OBSERVE -> OUTPUT. Do not skip any step.

    Output Format:
    { "step": "START | PLAN | OUTPUT | TOOL",  "content": "string" , "tool": "string", "input": "string", "output": "string" }

    Available Tools:
    - get_weather_info(location: str) -> str : This tool takes a location as input and returns the current weather information for that location. You can use this tool when the user query is related to weather information.

    Example 1:                
    START: Hey, can you ssolve 2 +3 * 5 /10 for me?
    PLAN: {"step": "START", "content": "I will first identify the key components of the question. 
                The question is asking to solve the expression 2 + 3 * 5 / 10."}
    PLAN: {"step": "PLAN", "content": "To solve this expression, I will follow the order of operations (BODMAS). 
                First, I will solve the multiplication and division from left to right, and then I will solve the addition."}
    PLAN: {"step": "PLAN", "content": "First, I will solve the multiplication: 3 * 5 = 15."}
    PLAN: {"step": "PLAN", "content": "Then, I will solve the division: 15 / 10 = 1.5. Finally, I will solve the addition: 2 + 1.5 = 3.5. So, the final answer is 3.5."}
    PLAN: {"step": "PLAN", "content": "Finally, I will solve the addition: 2 + 1.5 = 3.5."}
    PLAN: {"step": "OUTPUT", "content": "3.5"}

    Example 2:                
    START: What is the weather of Delhi?
    PLAN: {"step": "START", "content": "Seems like the question is about the current weather information of Delhi."}
    PLAN: {"step": "PLAN", "content": "Let me see if we have any available tools to get the current weather information."}
    PLAN: {"step": "PLAN", "content": "Yes, we have a tool called get_weather_info(location: str) that can provide us with the current weather information for a given location. I will use this tool to get the current weather information for Delhi."}
    PLAN: {"step": "PLAN", "content": "I will call the tool like this: get_weather_info(location='Delhi')"}
    PLAN: {"step": "TOOL", "tool": "get_weather_info", "input": "Delhi"}
    PLAN: {"step": "OBSERVE", "tool": "get_weather_info", "output": "Current weather in Delhi is : Sunny 25°C"}
    PLAN: {"step": "PLAN", "content": "Great, I got the current weather information for Delhi using the tool. Now, I will provide the final answer to the user."}
    OUTPUT: {"step": "OUTPUT", "content": "Current weather in Delhi is : Sunny 25°C"}

    
'''

## Structure Formatting for the output of the model
class MyOutputModel(BaseModel):
    step: str = Field(..., description="The current step in the reasoning process (START, PLAN, TOOL, OUTPUT)")
    content: Optional[str] = Field(None, description="The content of the current step")
    tool: Optional[str] = Field(None, description="The name of the tool being used (if applicable)")
    input: Optional[str] = Field(None, description="The input for the tool (if applicable)")

message_history = [
    {"role": "system", "content": SYSTEM_PROMPT},
]

user_query = input("Enter your query: ")
message_history.append({"role": "user", "content": user_query})

while True:
    response = client.chat.completions.parse(
        model="gemini-2.5-flash-lite",
        response_format=MyOutputModel,
        messages=message_history
    )

    raw_content = response.choices[0].message.content
    message_history.append({"role": "assistant", "content": raw_content})

    #get parsed content from the response
    parsed_result = response.choices[0].message.parsed

    if parsed_result.step == "START":
        print(f"START: {parsed_result.content}")
        continue
    elif parsed_result.step == "PLAN":
        print(f"PLAN: {parsed_result.content}")
        continue
    elif parsed_result.step == "TOOL":
        tool_name = parsed_result.tool
        tool_input = parsed_result.input
        if tool_name == "get_weather_info":
            tool_output = get_weather_info(tool_input)
            observe_message = {
                "role": "developer",
                "content": json.dumps({
                    "step": "OBSERVE",
                    "tool": tool_name,
                    "output": tool_output
                })
            }
            message_history.append(observe_message)
            print(f"TOOL: Calling tool {tool_name} with input: {tool_input} and got output: {observe_message['content']}")
        continue
    elif parsed_result.step == "OUTPUT":
        print(f"OUTPUT: {parsed_result.content}")
        break


