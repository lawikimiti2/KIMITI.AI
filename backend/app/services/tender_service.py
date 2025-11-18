from __future__ import annotations
from typing import List, Dict, Any
from ..llm.clients import ChatClient
from ..prompts.loaders import load_prompt

class TenderService:
    def __init__(self):
        self.chat = ChatClient()

    def summarize(self, text: str) -> str:
        system = load_prompt("tender_summary.txt")
        return self.chat.generate(system=system, user=text)[:4000]

    def parse_boq(self, text: str) -> List[Dict[str, Any]]:
        system = load_prompt("boq_parse.txt")
        raw = self.chat.generate(system=system, user=text)
        import json
        try:
            data = json.loads(raw)
            if isinstance(data, list):
                return data
        except Exception:
            pass
        return []

    def analyze_risks(self, text: str) -> List[str]:
        system = load_prompt("risk_analysis.txt")
        raw = self.chat.generate(system=system, user=text)
        return [r.strip("- \n") for r in raw.splitlines() if r.strip()]

    def proposal(self, context: str) -> str:
        system = load_prompt("technical_proposal.txt")
        return self.chat.generate(system=system, user=context)
