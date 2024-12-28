"""Tests for conversation.py."""
import pytest
from conversation_tree import conversation as conv

def test_node_creation():
    node = conv.ConversationNode("Test Prompt", "Test Response")
    assert node.get_prompt() == "Test Prompt"
    assert node.get_response() == "Test Response"
    assert len(node.get_children()) == 0

@pytest.fixture
def sample_root() -> conv.ConversationNode:
    thread_root = conv.ConversationNode("Root prompt.", "Root response.")
    thread_a = thread_root.add_child("Prompt A", "Response A")
    thread_b = thread_root.add_child("Prompt B", "Response B")
    thread_a1 = thread_a.add_child("Prompt A1", "Response A1")
    thread_a2 = thread_a.add_child("Prompt A2", "Response A2")
    thread_b1 = thread_b.add_child("Prompt B1", "Response B1")
    return thread_root

@pytest.fixture
def sample_leaf(sample_root):
    thread_a2 = sample_root.get_children()[0].get_children()[1]
    return thread_a2

def test_get_root(sample_leaf, sample_root):
    assert sample_leaf.get_root() is sample_root

def test_get_thread_messages(sample_leaf):
    expected_messages = [
        {'role': 'user', 'content': 'Root prompt.'},
        {'role': 'assistant', 'content': 'Root response.'},
        {'role': 'user', 'content': 'Prompt A'},
        {'role': 'assistant', 'content': 'Response A'},
        {'role': 'user', 'content': 'Prompt A2'},
        {'role': 'assistant', 'content': 'Response A2'}
        ]
    assert conv.generate_thread_messages(sample_leaf) == expected_messages
