import os
from dotenv import load_dotenv

def get_openai_api_key():
    """Get OpenAI API key from environment variables."""
    load_dotenv()
    api_key = os.getenv('OPENAI_API_KEY')
    if not api_key:
        raise ValueError("OpenAI API key not found. Please set OPENAI_API_KEY in your .env file")
    return api_key

def get_serper_api_key():
    """Get Serper API key from environment variables."""
    load_dotenv()
    api_key = os.getenv('SERPER_API_KEY')
    if not api_key:
        raise ValueError("Serper API key not found. Please set SERPER_API_KEY in your .env file")
    return api_key

def pretty_print_result(result):
    """Pretty print the result from CrewAI."""
    print("\n=== Result ===")
    print(result)
    print("=============\n")
