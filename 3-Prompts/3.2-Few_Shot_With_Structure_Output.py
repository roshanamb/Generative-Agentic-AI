import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
client = OpenAI(
    api_key=os.environ["GOOGLE_API_KEY"],
    base_url="https://generativelanguage.googleapis.com/v1beta"
)

# FEW SHOT PROMPT : Asking the model to perform a task with few example. 

# The system prompt is used to set the behavior of the assistant, 
# and the user prompt is used to ask a question or give a command.
SYSTEM_PROMPT = '''
    You should only & only answer coding related questions. If the question is not coding related, respond with "Sorry, I can only answer coding related questions."
    Here are some examples of coding related questions and their answers:

    Rules:
    - Stritly follow the format of the answer in JSON.

    Output Format:
    {
        "code": "string" or null,    
        "IsCodingQuestion": boolean, 
    }

    Examples:                
    Q: What is the square of (a+b)?
    A: {"code": null, "IsCodingQuestion": false}

    Q: Write a code in python to add 2 numbers. A: Here is a code in python to add 2 numbers:
    A: {"code": "def add(a, b):\n        return a + b", "IsCodingQuestion": true}

'''

QUESTIONS = [
  "Write Python code to print Fibonacci series up to n numbers.",
  "What is the capital of France?",
  "What is the square of (a+b)?"
]

single_user_content = "Please answer each labelled question separately.\n\n" + \
  "\n\n".join(f"Q{i+1}: {q}" for i,q in enumerate(QUESTIONS)) + \
  "\n\nRespond with `Answer 1:`, `Answer 2:`, ... for each."

response = client.chat.completions.create(
    model="gemini-2.5-flash",
    messages=[
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": single_user_content}
    ],)

print(response.choices[0].message.content)

#output:
#Answer 1: {"code": "def fibonacci_series(n):\n    a, b = 0, 1\n    series = []\n    while len(series) < n:\n        series.append(a)\n        a, b = b, a + b\n    return series\n\n# Example usage:\n# n_terms = 10\n# print(fibonacci_series(n_terms))",    "IsCodingQuestion": true}
# Answer 2: {"code": null,    "IsCodingQuestion": false}
# Answer 3: {"code": null,    "IsCodingQuestion": false}

