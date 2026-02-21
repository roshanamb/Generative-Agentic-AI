import json
import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
client = OpenAI(
    api_key=os.environ["GOOGLE_API_KEY"],
    base_url="https://generativelanguage.googleapis.com/v1beta"
)

# CoT (Chain of Thought) prompting is a technique used to improve the reasoning capabilities of language models.
# In CoT prompting, the model is encouraged to generate intermediate reasoning steps before arriving at a final answer. 


SYSTEM_PROMPT = '''
    You are an expert assistant in resolving user queries using chain of thought (CoT) prompting. 
    When a user asks a question, you will first break down the question into smaller sub-questions or steps, 
    and then provide a final answer based on the reasoning process.
    You work on START, PLAN & OUTPUT steps.
    - START: You will start by understanding the question and identifying the key components.
    - PLAN: You will then create a plan to solve the question by breaking it down into smaller sub-questions or steps.
    - OUTPUT: Finally, you will provide the final answer based on the reasoning process.

    Rules:
    - Stritly follow the format of the answer in JSON.
    - Only run one step at a time
    - The sequence of steps should be START -> PLAN -> OUTPUT. Do not skip any step.

    Output Format:
    { "step": "START | PLAN | OUTPUT",  "content": "string" }

    Examples:                
    START: Hey, can you ssolve 2 +3 * 5 /10 for me?
    PLAN: {"step": "START", "content": "I will first identify the key components of the question. 
                The question is asking to solve the expression 2 + 3 * 5 / 10."}
    PLAN: {"step": "PLAN", "content": "To solve this expression, I will follow the order of operations (BODMAS). 
                First, I will solve the multiplication and division from left to right, and then I will solve the addition."}
    PLAN: {"step": "PLAN", "content": "First, I will solve the multiplication: 3 * 5 = 15."}
    PLAN: {"step": "PLAN", "content": "Then, I will solve the division: 15 / 10 = 1.5. Finally, I will solve the addition: 2 + 1.5 = 3.5. So, the final answer is 3.5."}
    PLAN: {"step": "PLAN", "content": "Finally, I will solve the addition: 2 + 1.5 = 3.5."}
    PLAN: {"step": "OUTPUT", "content": "3.5"}
    
'''
message_history = [
    {"role": "system", "content": SYSTEM_PROMPT},
]

user_query = input("Enter your query: ")
message_history.append({"role": "user", "content": user_query})

while True:
    response = client.chat.completions.create(
        model="gemini-2.5-flash",
        response_format={"type": "json_object"},
        messages=message_history
    )

    raw_content = response.choices[0].message.content
    message_history.append({"role": "assistant", "content": raw_content})


#output:



