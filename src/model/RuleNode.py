from typing import List
from .Rule import Rule

class RuleNode:
    def __init__(self, name: str, code: str, summary: str, child_rule: List[str]):
        self.name = name
        self.code = code
        self.summary = summary
        self.child_rule = child_rule