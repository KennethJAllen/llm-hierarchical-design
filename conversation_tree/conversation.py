from __future__ import annotations  # Enables postponed evaluation of type hints

class ConversationNode:
    """Contains the conversation tree logic."""
    def __init__(self, prompt: str, response: str):
        self._prompt = prompt
        self._response = response
        self._parent = None
        self._children = []

    def get_prompt(self) -> str:
        """Returns the LLM prompt corresponding to the response."""
        return self._prompt

    def get_response(self) -> str:
        """Returns the LLM response from the prompt."""
        return self._response

    def get_parent(self) -> ConversationNode | None:
        """Returns the parent node."""
        return self._parent

    def get_children(self) -> list[ConversationNode]:
        """Returns a list of all children nodes."""
        return self._children

    def get_root(self) -> ConversationNode:
        """Returns the root of the tree."""
        if self._parent is None:
            return self
        return self._parent.get_root()

    def add_child(self, prompt: str, response: str):
        """Adds a child node."""
        child = ConversationNode(prompt, response)
        child._parent = self
        self._children.append(child)
        return child

    def to_message(self) -> list[dict[str, str]]:
        """Format the prompt and response for message input into LLM."""
        prompt_message = {"role": "user", "content": self._prompt}
        response_message = {"role": "assistant", "content": self._response}
        return [prompt_message, response_message]

    def __repr__(self):
        return f"ConversationNode(prompt={self._prompt},response={self._response})"

def generate_thread_messages(node: ConversationNode) -> list[dict[str, str]]:
    """Generates the context messages for the LLM a conversation node."""
    if node.get_parent() is not None:
        messages = generate_thread_messages(node.get_parent())
    else:
        messages = []
    return messages + node.to_message()

if __name__ == "__main__":
    thread_root = ConversationNode("Root prompt.", "Root response.")
    thread_a = thread_root.add_child("Prompt A", "Response A")
    thread_b = thread_root.add_child("Prompt B", "Response B")
    thread_a1 = thread_a.add_child("Prompt A1", "Response A1")
    thread_a2 = thread_a.add_child("Prompt A2", "Response A2")
    thread_b1 = thread_b.add_child("Prompt B1", "Response B1")
    test_messages = generate_thread_messages(thread_a2)
    print(test_messages)
