import unittest
import json
import sys
sys.path.append('src')
from model.RuleNode import RuleNode
from model.Rule import Rule
from util.prompt_util import PromptEngineeringUtil

class TestPromptEngineeringUtil(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None
        
    def test_get_prompt_json_with_child_rules(self):
        rule = RuleNode("parent_rule", "Parent Rule Code", "Parent Rule Summary", Rule("",""))
        child_rules = [
            RuleNode("child_rule1", "Child Rule 1 Code", "Child Rule 1 Summary", Rule("","")),
            RuleNode("child_rule2", "Child Rule 2 Code", "Child Rule 2 Summary", Rule("","")),
            RuleNode("child_rule3", "Child Rule 3 Code", "Child Rule 3 Summary", Rule("",""))
        ]

        expected_prompt_json = json.dumps({
            "model": "wizardcoder",
            "prompt": "You are an AI language model trained to understand the TIBCO Object Star legacy code.\\n"
            "Please create a detailed explanation of the below code and also explain the purpose of the code:\\n\\n"
            "Parent Rule Code\\n\\nThe summary of dependent child rules is as below. Use that as look up whenever the above parent rule has references.\\n\\n"
            "child_rule1\\nchild_rule1\\nchild_rule2\\nchild_rule2\\nchild_rule3\\nchild_rule3\\n\\n\\n"
            "Facilitating understanding for modern developers who haven't previously worked with legacy code.\\n\\n"
            "Reply only in markdown format with headings, sub-headings, pointers, code blocks, etc.\\n"
            "Explanation(Include: Purpose, Highlighting Dependencies, Data Store Dependencies, Tagging and Grouping, User Stories Creation):\\n",
            "options": {"num_ctx": 4096}
        })
        
        prompt_json = PromptEngineeringUtil.get_prompt_json(rule, child_rules)
        
        self.assertEqual(expected_prompt_json, prompt_json)

    def test_get_prompt_json_without_child_rules(self):
        rule = RuleNode("parent_rule", "Parent Rule Code", "Parent Rule Summary", Rule("", ""))
        child_rules = []

        expected_prompt_json = json.dumps({
            "model": "wizardcoder",
            "prompt": "You are an AI language model trained to understand the TIBCO Object Star legacy code.\\n"
            "Please create a detailed explanation of the below code and also explain the purpose of the code:\\n\\n"
            "Parent Rule Code\\n\\nThe summary of dependent child rules is as below. Use that as look up whenever the above parent rule has references.\\n\\n\\n\\n"
            "Facilitating understanding for modern developers who haven't previously worked with legacy code.\\n\\n"
            "Reply only in markdown format with headings, sub-headings, pointers, code blocks, etc.\\n"
            "Explanation(Include: Purpose, Highlighting Dependencies, Data Store Dependencies, Tagging and Grouping, User Stories Creation):\\n",
            "options": {"num_ctx": 4096}
        })

        prompt_json = PromptEngineeringUtil.get_prompt_json(rule, child_rules)
        self.assertEqual(prompt_json, expected_prompt_json)

if __name__ == '__main__':
    unittest.main()