import os
import sys
import types 

from dotenv import load_dotenv
from google import genai
from google.genai import types
from functions.get_files_info import schema_get_files_info

system_prompt = """
You are a helpful AI coding agent.

When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

- List files and directories

All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
"""

def main():

    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key)

    args = sys.argv
    user_prompt = args[1]

    available_functions = types.Tool(
    function_declarations=[
        schema_get_files_info,
        ]
    )
    
    config=types.GenerateContentConfig(
    tools=[available_functions], system_instruction=system_prompt
    )

    
    prompt_info = ai_respose_return(ai_response(user_prompt, client, config))
    verbose(args, prompt_info)


def ai_response(user_prompt, client, config = types.GenerateContentConfig(system_instruction=system_prompt)):
    user_prompt = user_prompt

    messages = [
    types.Content(role="user", parts=[types.Part(text=user_prompt)]),
    ]

    response = client.models.generate_content(
    model="gemini-2.0-flash-001",
    contents=messages,
    config= config
    )

    return response


def ai_respose_return(response):
    prompt_tokens = response.usage_metadata.prompt_token_count
    response_tokens = response.usage_metadata.candidates_token_count

    if hasattr(response.candidates[0].content.parts[0],  "function_call"):
        try:
            response_function_calls = response.candidates[0].content.parts[0].function_call # reaching response function_calls
            if response_function_calls is not None:
                print(f"Calling function: {response_function_calls.name}({response_function_calls.args})")
                return (response, prompt_tokens, response_tokens, response_function_calls)
        except Exception as e:
            return f"Error: function calls problem"
    print(response.text)    
    return (response, prompt_tokens, response_tokens)


def verbose (args, prompt_info):
    if  "--verbose" in args:
        print(f"User prompt: {prompt_info[0]}")
        print(f"Prompt tokens: {prompt_info[2]}")
        print(f"Response tokens: {prompt_info[3]}")
    pass

if len(sys.argv) < 2:
    print("error")
    sys.exit(1)

elif __name__ == "__main__":
    main()