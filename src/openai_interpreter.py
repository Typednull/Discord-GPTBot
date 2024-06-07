import openai
from dotenv import load_dotenv
from discord import *
import os
from .command_parser import parse_response_to_json

load_dotenv()
APIKEY = os.getenv('OPEN_API_KEY')

def interpret_command(text):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4o",
            messages=[{"role": "system", "content": "You are an assistant that understands and executes Discord commands."},
                      {"role": "user", "content": text}]
        )
        parsed_response = response['choices'][0]['message']['content'].strip()
        print("OpenAI Response:", parsed_response)  # Log the raw response
        command_details = parse_response_to_json(parsed_response)
        print("Parsed Command Details:", command_details)  # Log the parsed details
        return command_details
    except Exception as e:
        print(f"Error with OpenAI API: {e}")
        return {'action': 'error', 'message': str(e)}
