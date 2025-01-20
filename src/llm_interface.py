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

def generate_initial_prompt(user_input: str) -> str:
    """
    Generate a structured prompt for the LLM based on the user's input describing the main goal of their project.

    Inputs:
        user_input: The user's input describing the main goal.

    Returns:
        str: A structured initial prompt for the LLM.
    """
    prompt = (
        f"The user is working on a project with the following main goal:\n"
        f"'{user_input}'.\n\n"
        f"Please provide an initial response to help clarify or expand on this goal, "
        f"offering suggestions or potential directions they might consider."
    )
    return prompt

if __name__ == "__main__":
    test_prompt = generate_initial_prompt("Create a hierarchical conversation project with an LLM.")
    print(test_prompt)
