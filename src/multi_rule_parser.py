import os
from pathlib import Path
from rule_parser import create_rule
from model.RuleNode import RuleNode
from model.Node import Node
from model.Relationship import Relationship
from repository.neo4j_repository import Neo4jRepository

def write_rules_to_files(base_path, rule_folder, rule_name):
    os.makedirs(base_path + rule_folder, exist_ok=True)
    with open(base_path + rule_name, 'r') as file:
        rules = file.read().split(" ++++++++++++++++++++++++++++\n")
        for counter, rule in enumerate(rules,start=1):
            rule_path = base_path + rule_folder + "Rule" + str(counter)
            with open(rule_path, 'w') as rule_file:
                        rule_file.write(rule)

def create_parent_child_rule_map(base_path: str, rule_folder: str):
    directory_path = os.path.join(base_path, rule_folder)
    rule_map = {}

    for file_name in os.listdir(directory_path):
        code = ""
        file_path = os.path.join(directory_path, file_name)
        
        with open(file_path, 'r') as file:
            code = file.read()

        rule = create_rule(file_path)
        rule_map[rule.name] = RuleNode(rule.name, code, "", rule)        
    return rule_map

def create_neo4j_entries(rule_map):
    user = os.getenv("USER_NAME")
    password = os.getenv("PASSWORD")
    uri = os.getenv("URI")
    neo4j = Neo4jRepository(uri, user, password)
    for _, rule in rule_map.items():
        create_node_and_relationship(neo4j, rule)
    neo4j.close()

def create_node_and_relationship(neo4j, rule_node):

    node = Node(rule_node.name, ["Rule", "Node"], {"code": rule_node.code})
    neo4j.create_node(node)
    
    child_rules = [dep for dep in rule_node.rule.dependencies if dep.type == 'Rule']

    for child_rule in child_rules:
        sub_node = Node(child_rule.value, ["Rule", "Node"], None)
        neo4j.create_node(sub_node)
        relationship = Relationship(rule_node.name + "_" + child_rule.value, ["Relationship"], node, sub_node, None)
        neo4j.create_relationship(relationship)

base_path = "resources/"
rule_folder = "rules/"
rule_name = "rule_example3.md"
write_rules_to_files(base_path, rule_folder, rule_name)
rule_map = create_parent_child_rule_map(base_path, rule_folder)
create_neo4j_entries(rule_map)
