from google import genai
from google.genai import types
import os
from rich.console import Console
from rich.markdown import Markdown

console = Console()

client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])

def ask(user_input):
    response = client.models.generate_content(
        model="gemini-3.6-flash",
        contents=user_input,
        config=types.GenerateContentConfig(
            automatic_function_calling=types.AutomaticFunctionCallingConfig(
                disable=True
           )
        )
    )
    console.print(Markdown(response.text))


#print(Markdown(response.text))

while True:
    user_input = input("> ")

    if user_input == "exit":
        break

    print(ask(user_input))