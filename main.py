import os
import argparse
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
    model_name="gemini-2.5-flash"

    response = client.models.generate_content(
        model=model_name,
        contents=messages,
        config=types.GenerateContentConfig(
            system_instruction=system_prompt,
            tools=[available_functions]
        )
    )

    if not response.usage_metadata:
        raise RuntimeError("no metadata present on request")



    print("Response:")
    if args.verbose:
        print(f"User prompt: {args.user_prompt}")
        print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {response.usage_metadata.candidates_token_count}")

    calls = []

    if response.function_calls is not None:

        for function_call in response.function_calls:
            function_call_result = call_function(function_call, verbose=args.verbose)

            if len(function_call_result.parts) <= 0:
                raise Exception(f"Error: types.Content object of function_call had no non-empty parts")
            if function_call_result.parts[0].function_response is None:
                raise Exception(f"Error: function_response is None")
            if function_call_result.parts[0].function_response.response is None:
                raise Exception(f"Error: function_response.response is None")
            calls.append(function_call_result.parts[0])

            if args.verbose:
                print(f"-> {function_call_result.parts[0].function_response.response}")



    else:
        print(response.text)

if __name__ == "__main__":
    main()
