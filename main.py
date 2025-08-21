import os
import sys 
from dotenv import load_dotenv
from google import genai
from google.genai import types

def main():

    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key)

    args = sys.argv
    user_prompt = args[1]

    prompt_info = ai_response(user_prompt)
    verbose(args, prompt_info)
        
def ai_response(user_prompt):
    user_prompt = user_prompt
    messages = [
    types.Content(role="user", parts=[types.Part(text=user_prompt)]),
    ]
    response = client.models.generate_content(
    model="gemini-2.0-flash-001",
    contents=messages,
    )
    prompt_tokens = response.usage_metadata.prompt_token_count
    response_tokens = response.usage_metadata.candidates_token_count
    print (response.text)
    return [user_prompt, response, prompt_tokens, response_tokens]

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