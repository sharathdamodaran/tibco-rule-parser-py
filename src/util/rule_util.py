from typing import List, Dict, Any
from repository.neo4j_repository import Neo4jRepository
from model.RuleNode import RuleNode

class RuleUtil:
    def __init__(self, neo4j_repository: Neo4jRepository):
        self.neo4j = neo4j_repository

    def get_rule(self, id: str) -> RuleNode:
        record = self.neo4j.get_node(id)
        properties = dict(record['n'].items())
        code = properties.get('code', '')
        rule = RuleNode(properties['id'], code, '', None, None)
        return rule

    def update_summary(self, id: str, summary: str):
        self.neo4j.update_property(id, 'summary', summary)

    def get_child_rules(self, id: str) -> List[RuleNode]:
        child_rules = []
        records = self.neo4j.get_child_node(id)
        for record in records:
            properties = dict(record['c'].items())
            code = properties.get('code', '')
            summary = properties.get('summary', '')
            child_rules.append(RuleNode(properties['id'], code, summary, None, None))
        return child_rules