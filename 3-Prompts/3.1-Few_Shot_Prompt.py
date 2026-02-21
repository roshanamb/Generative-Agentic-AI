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

    Examples:                
    Q: What is the square of (a+b)?
    A: Sorry, I can only answer coding related questions.

    Q: Write a code in python to add 2 numbers. A: Here is a code in python to add 2 numbers:
    A: def add(a, b):
            return a + b

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
#Answer 1: Here is a Python code to print Fibonacci series up to n numbers:
'''python
def fibonacci_series(n):
    a, b = 0, 1
    series = []
    while a <= n:
        series.append(a)
        a, b = b, a + b
    return series

# Example usage:
n_limit = 100
fib_numbers = fibonacci_series(n_limit)
print(f"Fibonacci series up to {n_limit}: {fib_numbers}")
'''
# Answer 2: Sorry, I can only answer coding related questions.
# Answer 3: Sorry, I can only answer coding related questions.
