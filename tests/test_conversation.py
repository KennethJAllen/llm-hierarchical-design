"""Tests for conversation.py."""
import pytest
from src import conversation as conv

def test_node_creation():
    node = conv.ConversationNode("Test Prompt", "Test Response")
    assert node.get_prompt() == "Test Prompt"
    assert node.get_response() == "Test Response"
    assert len(node.get_children()) == 0

@pytest.fixture(name='sample_root')
def fixture_sample_root() -> conv.ConversationNode:
    tree_root = conv.ConversationNode("Root prompt.", "Root response.")
    thread_a = tree_root.add_child("Prompt A", "Response A")
    thread_b = tree_root.add_child("Prompt B", "Response B")
    thread_a.add_child("Prompt A1", "Response A1") # thread A1
    thread_a.add_child("Prompt A2", "Response A2") # thread A2
    thread_b.add_child("Prompt B1", "Response B1") # thread B1
    return tree_root

@pytest.fixture(name='sample_thread')
def fixture_sample_thread(sample_root: conv.ConversationNode) -> conv.ConversationNode:
    thread_a = sample_root.get_children()[0]
    return thread_a

@pytest.fixture(name='sample_leaf')
def fixture_sample_leaf(sample_root: conv.ConversationNode):
    thread_a2 = sample_root.get_children()[0].get_children()[1]
    return thread_a2

def test_get_root(sample_leaf: conv.ConversationNode, sample_root: conv.ConversationNode):
    assert sample_leaf.get_root() is sample_root

def test_get_thread_messages(sample_leaf: conv.ConversationNode):
    expected_messages = []
    expected_messages.append({"role": "system", "content": "You are a project assistant."})
    expected_messages.append({'role': 'user', 'content': 'Root prompt.'})
    expected_messages.append({'role': 'assistant', 'content': 'Root response.'})
    expected_messages.append({'role': 'user', 'content': 'Prompt A'})
    expected_messages.append({'role': 'assistant', 'content': 'Response A'})
    expected_messages.append({'role': 'user', 'content': 'Prompt A2'})
    expected_messages.append({'role': 'assistant', 'content': 'Response A2'})
    assert conv.generate_thread_messages(sample_leaf) == expected_messages

def test_delete(sample_thread: conv.ConversationNode):
    root = sample_thread.get_parent()
    sample_thread.delete()
    assert sample_thread.get_parent() is None
    assert sample_thread.get_children() is None
    assert len(root.get_children()) == 1

def test_get_thread(sample_leaf: conv.ConversationNode):
    thread = sample_leaf.get_thread()
    root = sample_leaf.get_root()
    expected_thread = [root, root.get_children()[0], sample_leaf]
    thread = sample_leaf.get_thread()
    assert thread == expected_thread
