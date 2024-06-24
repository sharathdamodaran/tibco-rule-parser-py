import os
from typing import Dict
from pathlib import Path
import model.RuleNode, model.Node, model.Relationship

def write_rules_to_files(base_path, rule_folder, file_name):
    rule_start_flag = False
    rule_counter = 0
    rule = ""

    os.makedirs(base_path + rule_folder, exist_ok=True)

    try:
        with open(base_path + file_name, 'r') as file:
            lines = file.readlines()
            for line in lines:
                rule_start_condition = line.strip() != '' and not rule_start_flag
                rule_end_condition = line.strip() == '' and rule_start_flag
                if rule_end_condition:
                    rule_start_flag = False
                    rule_name = "Rule" + str(rule_counter + 1)
                    rule_path = base_path + rule_folder + rule_name + ".txt"
                    with open(rule_path, 'w') as rule_file:
                        rule_file.write(rule.strip())
                    rule = ""
                    rule_counter += 1
                elif rule_start_condition:
                    rule_start_flag = True
                if rule_start_flag:
                    rule+=line.strip()+"\n"
    except IOError as e:
        print(e)

def create_parent_child_rule_map(base_path: str, rule_folder: str):
    directory_path = os.path.join(base_path, rule_folder)
    rule_map = {}

    for path in os.listdir(directory_path):
        add_rules_and_child_rules(rule_map, os.path.join(directory_path, path))

    return rule_map

def add_rules_and_child_rules(rule_map, path):
    is_first_line = True
    rule_name = ""
    code = ""
    child_rule_name_list = []

    with open(path, 'r') as file:
        lines = file.readlines()
        for line in lines:
            code += line
            if is_first_line:
                rule_name = extract_rule_name(line)
                is_first_line = False
            elif "CALL" in line:
                child_rule_name = extract_child_rule_name(line)
                child_rule_name_list.append(child_rule_name)

    rule_map[rule_name] = model.RuleNode(rule_name, code, "", child_rule_name_list)        

def extract_rule_name(line):
    name = line
    if ";" in line:
        name=line[:line.index(";")]
        
    has_parameters = "(" in name
    if has_parameters:
        name = name[:name.index("(")]
        
    return name

def extract_child_rule_name(line):
    child_rule_name = line
    if ";" in line:
        child_rule_name=line[:line.index(";")]

    has_parameters = "(" in child_rule_name
    if has_parameters:
        child_rule_name = child_rule_name[child_rule_name.index("CALL") + 5:child_rule_name.index("(")]
    else:
        child_rule_name = child_rule_name[child_rule_name.index("CALL") + 5:]
        
    return child_rule_name

def create_neo4j_entries(rule_map){
    TODO
}

def create_node_and_relationship(neo4j, base_path, rule_name, rule):
    # file_path = base_path + "rules.json"
    # with open(file_path, 'w') as file:
    #     file.write("")

    node = model.Node(rule_name, ["Rule", "Node"], {"code": rule.code})
    neo4j.create_node(node)
    # with open(file_path, 'a') as file:
    #     file.write(json.dumps(node.__dict__) + "\n")

    for child_rule in rule.child_rule:
        sub_node = model.Node(child_rule, ["Rule", "Node"], None)
        neo4j.create_node(sub_node)
        # with open(file_path, 'a') as file:
        #     file.write(json.dumps(sub_node.__dict__) + "\n")
        relationship = model.Relationship(rule_name + "_" + child_rule, ["Relationship"], node, sub_node, None)
        neo4j.create_relationship(relationship)
        # with open(file_path, 'a') as file:
        #     file.write(json.dumps(relationship.__dict__) + "\n")
        
base_path = "src/resources/"
rule_folder = "rules/"
file_name = "MultiRuleExample.txt"
# write_rules_to_files(base_path, rule_folder, file_name)
parent_child_rule_map = create_parent_child_rule_map(base_path,rule_folder)