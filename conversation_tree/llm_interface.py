import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv() # Load environment variables from a .env file

def format_query(query: str) -> dict[str, str]:
    """Formats the query string for input into messages."""
    return {'role': 'user', 'content': query}

def query_llm(messages: list[dict[str,str]], model="gpt-4o-mini") -> str:
    """Queries the LLM and returns the response as a string."""
    api_key = os.getenv("OPENAI_API_KEY")
    client = OpenAI(api_key=api_key)
    response = client.chat.completions.create(
        messages = messages,
        model = model)
    response = response.choices[0].message.content
    return response

if __name__ == "__main__":
    # {"role": "system", "content": "You are a project assistant."}
    pass
