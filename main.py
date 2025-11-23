import os
import sys
from google import genai
from dotenv import load_dotenv
from google.genai import types

from system_prompt import system_prompt
from call_functions import call_function, available_functions



def main():
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key)
    
    verbose = "--verbose" in sys.argv
    args = []
    for arg in sys.argv[1:]:
        if not arg.startswith("--"):
            args.append(arg)
    
    arg = sys.argv[1:]
    if not args:
        print("error")
        sys.exit(1)
    user_prompt = " ".join(args)
    
    if verbose:
        print(f"User prompt: {user_prompt}\n")

    messages=[types.Content(role='user',parts=[types.Part(text=user_prompt)])]

    
    
    
    # python
    def generate_content(client, messages, verbose):
        response = client.models.generate_content(
            model="gemini-2.0-flash-001",
            contents=messages,
            config=types.GenerateContentConfig(
                tools=available_functions,
                system_instruction=system_prompt,
            ),
        )

        if verbose:
            print("Prompt tokens:", response.usage_metadata.prompt_token_count)
            print("Response tokens:", response.usage_metadata.candidates_token_count)
            
        if response.candidates:
            for c in response.candidates:
                messages.append(c.content)
        if not response.function_calls:
            return response.text
        
        function_r = []
        for function_call_part in response.function_calls:
            function_call_result = call_function(function_call_part, verbose)
            if (
                not function_call_result.parts
                or not function_call_result.parts[0].function_response
            ):
                raise RuntimeError("Function call did not produce a function_response.response")
            if verbose:
                print(f"-> {function_call_result.parts[0].function_response.response}")
            function_r.append(function_call_result.parts[0])
        if not function_r:
            raise Exception("no function responses generated, exiting.")
        messages.append(types.Content(role='user',parts=function_r))


    for i in range(20):
        try:
            res = generate_content(client, messages, verbose)
            if res:
                print(f"Final response:\n{res}")
                break
        except Exception as e:
            if verbose:
                print(f"Error: {e}")
            break
       
        
  
    
        
if __name__ == "__main__":
    main()
