import os
import argparse
from dotenv import load_dotenv
from google import genai
from google.genai import types
from prompts import system_prompt
from call_function import available_functions




def main():
    parser = argparse.ArgumentParser(description="CHATBOT")
    parser.add_argument("user_prompt", type=str, help="User prompt")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()

    messages = [types.Content(role="user", parts=[types.Part(text=args.user_prompt)])]

    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        raise RuntimeError("GEMINI_API_KEY environment variable not set")
    
    
    client = genai.Client(api_key=api_key)
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents= messages,
        config=types.GenerateContentConfig(system_instruction=system_prompt, temperature=0, tools=[available_functions]),
    )
    if not response.usage_metadata:
        raise RuntimeError("Response have no metadata.") 


    if args.verbose:
        print(f"User prompt: {args.user_prompt}")
        print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {response.usage_metadata.candidates_token_count}")
    
    print("Response:")
    print(response.text)
    if response.function_calls:
        for call in response.function_calls:
            print(f"Calling function: {call.name}({call.args})")


if __name__ == "__main__":
    main()
