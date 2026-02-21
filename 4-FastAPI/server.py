import os
from fastapi import Body, FastAPI
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
client = OpenAI(
    api_key=os.environ["GOOGLE_API_KEY"],
    base_url="https://generativelanguage.googleapis.com/v1beta"
)

app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/contact")
def read_contact():
    return {"Hello": "Contact Page"}

@app.post("/chat")
def chat(
    message: str = Body(..., description="The user's message to the chatbot")
):
    response = client.chat.completions.create(
        model="gemini-2.5-flash",
        messages=[
            {
                "role": "user",
                "content": message
            }
        ]
    )
    return {"response": response.choices[0].message.content}