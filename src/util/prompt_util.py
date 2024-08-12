import json
from typing import List
from model.RuleNode import RuleNode

class PromptEngineeringUtil:

    @staticmethod
    def get_prompt_json(rule: RuleNode, child_rules: List[RuleNode]) -> str:
        child_rule_name_summary = []

        for child_rule in child_rules:
            child_name = child_rule.name.replace('"', '\\"')
            child_summary = child_rule.name.replace('"', '\\"')
            child_rule_name_summary.append(f"{child_name}\\n")
            child_rule_name_summary.append(f"{child_summary}\\n")

        template = (
            "You are an AI language model trained to understand the TIBCO Object Star legacy code.\n"
            "Please create a detailed explanation of the below code and also explain the purpose of the code:\n\n"
            "%s\n\n"
            "The summary of dependent child rules is as below. Use that as look up whenever the above parent rule has references.\n\n"
            "%s\n\n"
            "Facilitating understanding for modern developers who haven't previously worked with legacy code.\n\n"
            "Reply only in markdown format with headings, sub-headings, pointers, code blocks, etc.\n"
            "Explanation(Include: Purpose, Highlighting Dependencies, Data Store Dependencies, Tagging and Grouping, User Stories Creation):\n"
        )

        message = template % (rule.code, ''.join(child_rule_name_summary))
        message = message.replace("\n", "\\n").replace("\r", "\\r")

        prompt_json = json.dumps({
            "model": "wizardcoder",
            "prompt": message,
            "options": {"num_ctx": 4096}
        })

        return prompt_json