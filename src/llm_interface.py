"""Contains the logic for the LLM interface."""

import os
from dotenv import load_dotenv
import openai
import anthropic

load_dotenv() # Load environment variables from a .env file

def format_query(query: str) -> dict[str, str]:
    """Formats the query string for input into messages."""
    return {'role': 'user', 'content': query}

def query_llm(messages: list[dict[str,str]], model=None) -> str:
    """
    Queries the LLM and returns the response as a string.
    inputs:
        messages - The context window
        model (optional) - the LLM model to use
            Currently supported models are gpt and claude.
            e.g. model = "gpt-4o-mini" or "claude-3-5-haiku-latest"
    """
    api_key = os.getenv("OPENAI_API_KEY")
    if api_key is not None:
        try:
            response = _query_openai_llm(messages, api_key, model=model)
            return response
        except openai.NotFoundError:
            pass

    api_key = os.getenv("ANTHROPIC_API_KEY")
    if api_key is not None:
        try:
            response = _query_anthropic_llm(messages, api_key, model=model)
            return response
        except anthropic.NotFoundError:
            pass

    raise ValueError("API key not found or model not valid. If missing, create a .env file in the project's root directory with an OPENAI_API_KEY or an ANTHROPIC_API_KEY.")

def _query_openai_llm(messages: list[dict[str,str]], api_key: str, model: str=None) -> str:
    """Query the OpenAI api with the given message and model (if provided)."""
    if model is None:
        model = "gpt-4o-mini"
    client = openai.OpenAI(api_key=api_key)
    completion = client.chat.completions.create(
        messages = messages,
        model = model)
    response = completion.choices[0].message.content
    return response

def _query_anthropic_llm(messages: list[dict[str,str]], api_key: str, model: str=None) -> str:
    """Query the Anthropic api with the given message and model (if provided)."""
    if model is None:
        model = "claude-3-5-haiku-latest"
    client = anthropic.Anthropic(api_key=api_key)
    completion = client.messages.create(
        max_tokens = 1024,
        messages = messages,
        model = model)
    response = completion.content[0].text
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
    test_message = format_query(test_prompt)
    test_response = query_llm([test_message], model="claude-3-5-haiku-latest")
    print(test_response)
