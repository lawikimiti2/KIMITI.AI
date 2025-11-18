from __future__ import annotations
from typing import List
from ..llm.clients import ChatClient
from ..prompts.loaders import load_prompt

class ChatService:
    def __init__(self):
        self.chat = ChatClient()

    def chat_simple(self, query: str) -> str:
        system = "You are Kimiti, an accurate helpful assistant."
        return self.chat.generate(system=system, user=query)

    def chat_with_context(self, query: str, context: str) -> str:
        template = load_prompt("business_automation.txt")
        user = f"Context:\n{context}\n\nQuestion: {query}"
        return self.chat.generate(system=template, user=user)
