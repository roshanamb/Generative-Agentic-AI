import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
client = OpenAI(
    api_key=os.environ["GOOGLE_API_KEY"],
    base_url="https://generativelanguage.googleapis.com/v1beta"
)

# ZERO_SHOT PROMPT : Directly asking the model to perform a task without providing any examples. 

# The system prompt is used to set the behavior of the assistant, 
# and the user prompt is used to ask a question or give a command.
SYSTEM_PROMPT = "You should only & only answer coding related questions. If the question is not coding related, " \
                "respond with 'Sorry, I can only answer coding related questions.'"

USER_PROMPT = "Hey, can you tell be what is square of (a+b)?"
USER_PROMPT_Outside_Context = "What is the capital of France?"

response = client.chat.completions.create(
    model="gemini-2.5-flash",
    messages=[
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": USER_PROMPT},
        {"role": "user", "content": USER_PROMPT_Outside_Context},
    ],)
print(response.choices[0].message.content)

#output:
# The square of (a+b) is a^2 + 2ab + b^2.
# Sorry, I can only answer coding related questions.
