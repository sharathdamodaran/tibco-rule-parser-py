from typing import List
from .Rule import Rule

class RuleNode:
    def __init__(self, name: str, code: str, summary: str, rule:Rule, child_rule: List[str]):
        self.name = name
        self.code = code
        self.summary = summary
        self.rule = rule
        self.child_rule = child_rule