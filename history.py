# history.py

from langchain_core.messages import HumanMessage, AIMessage

class SimpleHistory:
    """Simple manual chat history manager."""
    def __init__(self):
        self.messages = []

    def add_user(self, text: str):
        self.messages.append(HumanMessage(content=text))

    def add_ai(self, text: str):
        self.messages.append(AIMessage(content=text))

    def to_list(self):
        return self.messages

    def format_for_prompt(self):
        # Useful if you want to insert history into your own prompt
        lines = []
        for msg in self.messages:
            role = "User" if isinstance(msg, HumanMessage) else "Assistant"
            lines.append(f"{role}: {msg.content}")
        return "\n".join(lines)
