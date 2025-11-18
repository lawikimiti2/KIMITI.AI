from __future__ import annotations
from app.services.tender_service import TenderService

class FakeChat:
    def __init__(self):
        self.calls = []
    def generate(self, system: str, user: str) -> str:
        self.calls.append((system[:16], len(user)))
        if 'BOQ' in system or 'boq' in system:
            return '[{"item":"A","quantity":1,"unit":"u","rate":10}]'
        if 'risk' in system:
            return '- risk1\n- risk2'
        return 'summary'

def test_tender_extraction_monkeypatch(monkeypatch):
    svc = TenderService()
    monkeypatch.setattr(svc, 'chat', FakeChat())
    s = svc.summarize('x')
    b = svc.parse_boq('y')
    r = svc.analyze_risks('z')
    assert s == 'summary'
    assert b and b[0]['item'] == 'A'
    assert r == ['risk1', 'risk2']
