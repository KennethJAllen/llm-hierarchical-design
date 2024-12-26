import os
from dotenv import load_dotenv
from openai import OpenAI

class ConversationNode:
    def __init__(self, prompt, response):
        self.prompt = prompt
        self.response = response
        self.children = []

    def add_child(self, prompt, response):
        child = ConversationNode(prompt, response)
        self.children.append(child)
        return child

class ConversationTree:
    def __init__(self, root_prompt, root_response):
        self.root = ConversationNode(root_prompt, root_response)

def generate_context(node: ConversationNode):
    if node is None:
        return []
    context = generate_context(node.parent) if hasattr(node, "parent") else []
    context.append({"role": "user", "content": node.prompt})
    context.append({"role": "assistant", "content": node.response})
    return context

def query_llm(prompt, model="gpt-4o-mini"):
    load_dotenv()
    api_key = os.getenv("OPENAI_API_KEY")
    client = OpenAI(api_key=api_key)
    response = client.chat.completions.create(
        messages=[
        {
            "role": "user",
            "content": prompt,
        }],
    model=model)
    return response.choices[0].message.content

if __name__ == "__main__":
    response_content = query_llm("Hello.")
    print(response_content)
