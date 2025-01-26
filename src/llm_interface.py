import os
from dotenv import load_dotenv
from openai import OpenAI
from anthropic import Anthropic

load_dotenv() # Load environment variables from a .env file

def format_query(query: str) -> dict[str, str]:
    """Formats the query string for input into messages."""
    return {'role': 'user', 'content': query}

def query_llm(messages: list[dict[str,str]], model="gpt-4o-mini") -> str:
    """
    Queries the LLM and returns the response as a string.
    inputs:
        messages - The context window
        model (optional) - the LLM model to use
            Currently supported models are gpt and claude.
            e.g. model = "gpt-4o-mini" or "claude-3-5-haiku-latest"
    """
    if model[:3] == 'gpt':
        api_key = os.getenv("OPENAI_API_KEY")
        client = OpenAI(api_key=api_key)
        completion = client.chat.completions.create(
            messages = messages,
            model = model)
        response = completion.choices[0].message.content
    elif model[:6] == 'claude':
        # TODO: fix logic in rest of this function to be compatible with Anthropic API key
        api_key = os.getenv("ANTHROPIC_API_KEY")
        client = Anthropic(api_key=api_key)
        completion = client.messages.create(
            max_tokens = 1024,
            messages = messages,
            model = model)
        response = completion.content[0].text
    else:
        raise ValueError(f"Model not currently supported: {model}")
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
    message = format_query(test_prompt)
    response = query_llm([message], model="claude-3-5-haiku-latest")
    #response = query_llm([message])
    print(response)
