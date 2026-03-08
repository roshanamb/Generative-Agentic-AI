from openai import OpenAI
import speech_recognition as sr
from dotenv import load_dotenv
import os

load_dotenv()

client = OpenAI()

def main():
    r = sr.Recognizer() # Initialize the recognizer

    # Use the microphone as source for input.
    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source) # Wait for a second to let the recognizer adjust the energy threshold based on the surrounding noise level  
        r.pause_threshold = 2              # seconds of non-speaking audio before a phrase is considered complete
        
        print("Speak Anything :")
        audio = r.listen(source)

        print("Processing Audio......")
        try:
            text = r.recognize_google(audio)
            print("You said : {}".format(text))
        except:
            print("Sorry could not recognize your voice")

        SYSTEM_PROMPT = '''
            You are an expert voice agent. You are given the transcript of the user's voice query. 
            You will analyze the query and provide a response based on the content of the query.
            What ever you speak will be converted back to audio using AI and played back to user. 
            So, make sure to provide a concise and clear response to the user's query.
        '''

        response = client.chat.completions.create(
            model="gpt-4.1-mini",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": text}
            ]
        )

        print("AI Response : {}".format(response.choices[0].message.content))

main()