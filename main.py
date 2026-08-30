from google import genai
from google.genai import types
import os
from rich.console import Console
from rich.markdown import Markdown
import sys
import argparse

def args():
    # argument parser
    parser = argparse.ArgumentParser(description="CLI interface for AI")

    # -s / --short argument
    parser.add_argument(
        "-s", "--short",
        action="store_true",
        help="Make AI response short."
    )

    # add -m / --message argument
    parser.add_argument(
        "-m", "--message",
        type=str,
        nargs = "+", # allows messages without quotes
        help="Add message for AI"
    )

    args = parser.parse_args()

    # check if a user sent a message
    if not args.message:
        return None

    user_prompt = " ".join(args.message)

    # --short arg handling

    system_instruction = ""
    if args.short:
        system_instruction = "IMPORTANT: Keep your response extremely brief, direct, and concise. No conversational fluff. "

    # combine args with full prompt for the AI
    final_prompt = f"{system_instruction}\nUser Question: {user_prompt}"

    return final_prompt

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

argument_prompt = args()
print(argument_prompt)

if argument_prompt:
    ask(argument_prompt)
else:
  while True:
      user_input = input("> ")

      if user_input == "exit":
          break

      print(ask(user_input))