"""Tests for llm_interface.py."""
import pytest
from src import llm_interface as llm

def test_format_query():
    test_query = 'Respond with "test".'
    expected_message = {'role': 'user', 'content': 'Respond with "test".'}
    assert llm.format_query(test_query) == expected_message

def test_query_llm():
    """
    Tests querying the LLM.
    Due to the random nature of LLMs, there is a chance this will fail.
    """
    test_query = 'Reply with "test".'
    test_message = [llm.format_query(test_query)]
    expected_response = "test"
    response = llm.query_llm(test_message)
    assert response == expected_response

@pytest.fixture(name='sample_messages')
def fixture_sample_messages() -> list[dict[str,str]]:
    messages = []
    messages.append({'role': 'user', 'content': 'This is my first message. I will refer back to it later.'})
    messages.append({'role': 'assistant','content': "Got it! I'll remember this is your first message for future reference."})
    messages.append({'role': 'user','content': 'This is my second message. I will refer back to it later.'})
    messages.append({'role': 'assistant','content': 'Understood! This is your second message. Feel free to reference it anytime.'})
    messages.append({'role': 'user','content': 'Repeat back to my my messages in order'})
    return messages

def test_message_order_openai(sample_messages):
    """
    Tests the order that messages are input.
    Due to the randomness of LLMs, there is a chance this can fail.
    """
    response = llm.query_llm(sample_messages, model="gpt-4o-mini")
    first_message_index = response.find('first')
    second_message_index = response.find('second')
    # check that the words 'first' and 'second' exist in the message.
    assert first_message_index != -1
    assert second_message_index != -1
    # Checl that the word 'first' comes before the word 'second'.
    assert first_message_index < second_message_index

def test_message_order_anbthropic(sample_messages):
    """
    Tests the order that messages are input.
    Due to the randomness of LLMs, there is a chance this can fail.
    """
    response = llm.query_llm(sample_messages, model="claude-3-5-haiku-latest")
    first_message_index = response.find('first')
    second_message_index = response.find('second')
    # check that the words 'first' and 'second' exist in the message.
    assert first_message_index != -1
    assert second_message_index != -1
    # Checl that the word 'first' comes before the word 'second'.
    assert first_message_index < second_message_index
