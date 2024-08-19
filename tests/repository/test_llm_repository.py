import unittest
from unittest.mock import patch
import json
import sys
sys.path.append('src')
from model.RuleNode import RuleNode
from model.Rule import Rule
from model.LLMResponse import LLMResponse
from repository.llm_repository import LLMRepository

class TestLLMRepository(unittest.TestCase):
    @patch('requests.Session.post')
    def test_translate_code(self, mock_post):
        mock_response = [
            {"response": "Translation 1", "model":"wizard_coder", "created_at": "2024-07-12 09:55:22", "done": "false"},
            {"response": "Translation 2", "model":"wizard_coder", "created_at": "2024-07-12 09:55:23", "done": "false"},
            {"response": "Translation 3", "model":"wizard_coder", "created_at": "2024-07-12 09:55:24", "done": "true"}
        ]
        mock_post.return_value.iter_lines.return_value = (json.dumps(line) for line in mock_response)

        rule = RuleNode("parent_rule", "Parent Rule Code", "Parent Rule Summary", Rule("", ""))
        child_rules = [
            RuleNode("child_rule1", "Child Rule 1 Code", "Child Rule 1 Summary", Rule("", "")),
            RuleNode("child_rule2", "Child Rule 2 Code", "Child Rule 2 Summary", Rule("", "")),
            RuleNode("child_rule3", "Child Rule 3 Code", "Child Rule 3 Summary", Rule("", ""))
        ]
        endpoint_url = "http://test.com/translate"

        repository = LLMRepository()

        result = repository.translate_code(endpoint_url, rule, child_rules)

        expected_result = "Translation 1Translation 2Translation 3"
        self.assertEqual(result, expected_result)

if __name__ == '__main__':
    unittest.main()