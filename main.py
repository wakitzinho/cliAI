from google import genai
from google.genai import types
import os
from rich.console import Console
from rich.markdown import Markdown
import argparse

def args():
    # argument parser
    parser = argparse.ArgumentParser(description="CLI interface for AI")

    # -q / quick question mode
    parser.add_argument(
        "-q", "--quick",
        action="store_true",
        help="Stay in shell after the response. "
    )

    # -v / answer in detail
    parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="AI will give a verbose, detailed explanation. "
    )

    # -cs / answer only in code but very optimized code.
    parser.add_argument(
        "-cs", "--codeShort",
        action="store_true",
        help="Make AI only answer in code but the ai will optimize it."
    )

    # -c / answer only in code arg
    parser.add_argument(
        "-c", "--code",
        action="store_true",
        help="Make AI only respond in code."

    )

    # -s / --short
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
        help="Your message for AI"
    )

    args = parser.parse_args()

    # check if a user sent a message
    if not args.message:
        return None

    user_prompt = " ".join(args.message)

    # arg handling
    system_instruction = ""
    if args.short:
        system_instruction = "IMPORTANT: Keep your response extremely brief, direct, and concise. No conversational fluff. "
    elif args.code:
        system_instruction = "IMPORTANT: only respond in code and anything helpful for example how to setup. "
    elif args.codeShort:
        system_instruction = "IMPORTANT: only respond in code and anything helpful for example how to setup. Also VERY IMPORTANT the code shall be very optimized and should not have anything unnecessary. "
    elif args.verbose:
        system_instruction = "IMPORTANT: answer with a detailed and verbose response. "

    # combine args with full prompt for the AI
    final_prompt = f"{system_instruction}\nUser Question: {user_prompt}"

    # return the final prompt
    return final_prompt, args.quick



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
    return response
    #console.print(Markdown(response.text))

# main loop

def main():

    argument_prompt, quick = args()
    print(argument_prompt, quick) # debugging if i need to

    # if used directly from shell normally
    if argument_prompt:
        user_input = argument_prompt
        response = ask(user_input)
        console.print(Markdown(response.text))
        return


    # if it has quick mode enabled: answer once and return to shell
    if quick:
        response = ask(argument_prompt)
        console.print(Markdown(response.text))
        return

    # normal mode: use normal loop
    while True:

        user_input = input("> ")

        if user_input == "exit":
            break

        response = ask(user_input)
        console.print(Markdown(response.text))


if __name__ == "__main__":
    main()