import os
import argparse
import sys
import time
from dotenv import load_dotenv
from google import genai
from google.genai import types
from prompts import system_prompt
from call_function import available_functions, call_function





def main():
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key)

    parser = argparse.ArgumentParser(description="Chatbot")
    parser.add_argument("user_prompt", type=str, help="User prompt")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()
    messages = [types.Content(role="user", parts=[types.Part(text=args.user_prompt)])]

    for _ in range(20):

        final_response = generate_content(client, messages, args.verbose)
        if final_response:
            print("Final response:")
            print(final_response)
            return


    print("Maximum iterations reached without a final response")
    sys.exit(1)


def generate_content(client, messages, verbose):
    time.sleep(10)
    function_responses = []

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=messages,
        config=types.GenerateContentConfig(
            tools=[available_functions],
            system_instruction=system_prompt
        ),
    )

    if response.candidates:
        for candidate in response.candidates:
            if candidate.content:
                messages.append(candidate.content)

    if not response.function_calls:
        return response.text


    for function_call in response.function_calls:
        function_call_result = call_function(function_call, verbose=verbose)

        if (
                not function_call_result.parts
                or not function_call_result.parts[0].function_response
                or not function_call_result.parts[0].function_response.response
        ):
            raise RuntimeError("Error: Function check failed")
        function_responses.append(function_call_result.parts[0])

        if verbose:
            print(f"-> {function_call_result.parts[0].function_response.response}")


    messages.append(types.Content(role="user", parts=function_responses))
    return None


if __name__ == "__main__":
    main()
