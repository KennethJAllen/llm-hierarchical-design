import os
import sys
print(sys.path[0])
from dotenv import load_dotenv
from openai import OpenAI
from conversation_tree import conversation as conv

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
    test_messages = [{'role': 'user',
                      'content': 'This is my first message. I will refer back to it later.'},
                      {'role': 'assistant',
                       'content': "Got it! I'll remember this is your first message for future reference. Let me know how I can assist you!"},
                       {'role': 'user',
                        'content': 'This is my second message. I will refer back to it later.'},
                        {'role': 'assistant',
                         'content': 'Understood! This is your second message. Feel free to reference it anytime.'},
                         {'role': 'user',
                          'content': 'Repeat back to my my messages in order'}
                      ]
    test_response = query_llm(test_messages)
    print(test_response)
