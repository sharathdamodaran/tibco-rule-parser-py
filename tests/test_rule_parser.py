import unittest
import sys
sys.path.append('../src')
import model
from rule_parser import create_rule
import json

class TestRuleParser(unittest.TestCase):
    def setUp(self):
        self.rule_location = '../resources/rule_example2.md'
        self.rule_output_location = '../resources/rule_example2_output.json'
        self.maxDiff = None

    def test_create_rule(self):
        rule = create_rule(self.rule_location)
        rule_dict = rule.to_dict()
        actual_output = json.dumps(rule_dict,indent=2)
        print(actual_output)
        expected_output = ""
        with open(self.rule_output_location, 'r') as file:
            expected_output = file.read()
        self.assertMultiLineEqual(actual_output,expected_output)
if __name__ == '__main__':
    unittest.main()