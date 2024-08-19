import os
from repository.neo4j_repository import Neo4jRepository
from repository.llm_repository import LLMRepository
from model.RuleNode import RuleNode
from util.rule_util import RuleUtil
from typing import List

def update_node_levels():
    user = os.getenv("USER_NAME")
    password = os.getenv("PASSWORD")
    uri = os.getenv("URI")
    neo4j = Neo4jRepository(uri, user, password)
    root_id = neo4j.get_root_node()
    neo4j.update_root_node_level(root_id)
    neo4j.update_child_node_levels(root_id)
    neo4j.close()

def get_rule_summary(rule: RuleNode, child_rules: List[RuleNode]) -> str:
    llm_end_point = "http://localhost:11434/api/generate"
    llm_repository = LLMRepository()
    return llm_repository.translate_code(llm_end_point, rule, child_rules)

def update_summaries():
    user = os.getenv("USER_NAME")
    password = os.getenv("PASSWORD")
    uri = os.getenv("URI")
    neo4j = Neo4jRepository(uri, user, password)
    rules_util = RuleUtil(neo4j)
    max_level = neo4j.get_max_level()
    
    for level in range(max_level, -1, -1):
        rules = neo4j.get_nodes_at_level(level)
        for rule_id in rules:
            rule = rules_util.get_rule(rule_id)
            child_rules = rules_util.get_child_rules(rule_id)
            rule_summary = get_rule_summary(rule, child_rules)
            rules_util.update_summary(rule_id, rule_summary)
    
    neo4j.close()
    
# update_node_levels()
# update_summaries()    