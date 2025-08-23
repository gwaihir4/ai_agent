import os
import sys
import types 

from dotenv import load_dotenv
from google import genai
from google.genai import types
from functions.get_files_info import *
from functions.get_file_content import *
from functions.run_python import *
from functions.write_file import *


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
        schema_get_files_info, schema_get_file_content, schema_run_python, schema_write_file
        ]
    )

    config=types.GenerateContentConfig(
    tools=[available_functions], system_instruction=system_prompt
    )

    
    prompt_info = ai_respose_return(ai_response(user_prompt, client, config))
    if isverbose(args):
        print(f"User prompt: {user_prompt}")
        print(f"Prompt tokens: {prompt_info["prompt_tokens"]}")
        print(f"Response tokens: {prompt_info["response_tokens"]}")    

    try:
        function_capture = function_call(prompt_info["response_function_call"],isverbose(args))
        if hasattr(function_capture.parts[0],  "function_response"):
            if isverbose (args) and hasattr(function_capture.parts[0].function_response,  "response"):
                print (f"-> {function_capture.parts[0].function_response.response}")
    except Exception as e:
         print (f"Error: returning function call {e}")
    
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
            response_function_call = response.candidates[0].content.parts[0].function_call # reaching response function_calls
            if response_function_call is not None:
                print(f"Calling function: {response_function_call.name}({response_function_call.args})")
                return {"response": response, "prompt_tokens": prompt_tokens, "response_tokens" : response_tokens, "response_function_call": response_function_call}
        except Exception as e:
            return f"Error: function calls problem"
    # print(response.text)    
    return {"response": response, "prompt_tokens": prompt_tokens, "response_tokens" : response_tokens}

def function_call(function_call_part, verbose=False):

    function_dict = {"get_file_content" : get_file_content, "get_files_info" : get_files_info, "run_python_file": run_python_file, "write_file": write_file}
    if verbose == True:
        print(f"Calling function: {function_call_part.name}({function_call_part.args})")
    print(f" - Calling function: {function_call_part.name}")

    if function_call_part.name in function_dict:
        #initialize function call 
        function = function_dict[function_call_part.name]
        args = function_call_part.args
        args.update({"working_directory": "./calculator"})
        function_capture = types.Content(
                            role="tool",
                            parts=[
                            types.Part.from_function_response(
                            name=function_call_part.name,
                            response={"result": function(**args)},
                                    )
                                ],
                            )
        return function_capture
    else:
        raise Exception (f"Error: wrong function call")    

def isverbose (args):
    if  "--verbose" in args:
        return True
    return False

if __name__ == "__main__":
    main()