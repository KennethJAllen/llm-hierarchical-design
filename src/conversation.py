from __future__ import annotations  # Enables postponed evaluation of type hints
from src import llm_interface as llm

class ConversationNode:
    """Contains the conversation tree logic."""
    def __init__(self, prompt: str, response: str = ""):
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

    def add_child(self, prompt: str, response: str = ""):
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

    def get_thread(self):
        """Returns a list of all nodes leading to this node starting from the root."""
        if self.get_parent() is not None:
            thread = self.get_parent().get_thread()
        else:
            thread = []
        thread.append(self)
        return thread

    def delete(self) -> None:
        """
        Removes the node and all children nodes from the tree by setting parent and children to None, and removing from parent node list.
        """
        # remove from parent's list of children
        self._parent._children.remove(self)
        self._parent = None
        self._children = None

    def generate_response_from_llm(self) -> None:
        """Query the LLM with the node's prompt and sets the llm's output to the response."""
        # Generate the context window.
        messsages = generate_thread_messages(self)
        response = llm.query_llm(messsages)
        self._response = response

    def __repr__(self):
        return f"ConversationNode(prompt={self._prompt},response={self._response})"

def generate_thread_messages(node: ConversationNode) -> list[dict[str, str]]:
    """Generates the context messages for the LLM a conversation node."""
    if node.get_parent() is not None:
        messages = generate_thread_messages(node.get_parent())
    else:
        messages = []
        messages.append({"role": "system", "content": "You are a project assistant."})
    return messages + node.to_message()

if __name__ == "__main__":
    pass
