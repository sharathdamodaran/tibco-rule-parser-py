from typing import List
from .Rule import Rule

class RuleNode:
    def __init__(self, name: str, code: str, summary: str, rule: Rule):
        self.name = name
        self.code = code
        self.summary = summary
        self.rule = rule