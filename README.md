# Conversation Tree

**Conversation Tree** is a project that uses a LLM to facilitate tree-like conversations for project structuring.
Instead of linear conversations, this tool allows users to branch conversations out into multiple threads, while maintaining the context window, aiding in the iterative development of project components.

---

## Features
- Supports branching conversations for flexible project planning.
- Keeps the entire conversation tree within the context window.
- Designed for top-down project structuring.

---

## Prerequisites
Before using this project, ensure you have the following installed:
- UV
---

## Setup

### 1. Clone the Repository
```bash
git clone https://github.com/KennethJAllen/conversation-tree
cd conversation-tree
```
### 2. Install Dependencies
Use UV to create the virtual environment.

### 3. Create a `.env` File

The project requires an OpenAI API key. Create a .env file in the root directory of the project:

```makefile
OPENAI_API_KEY=your_openai_api_key
```

Replace `your_openai_api_ke`  with your actual OpenAI API key.