import unittest
import sys
sys.path.append('src')
import model
from rule_parser import create_rule
import json

class TestRuleParser(unittest.TestCase):
    
    def setUp(self):
        self.maxDiff = None
    
    test_cases = [
        {"rule_location": "resources/single_rule_1.txt", "rule_output_location": "resources/single_rule_1.json"},
        {"rule_location": "resources/single_rule_2.txt", "rule_output_location": "resources/single_rule_2.json"},
        {"rule_location": "resources/single_rule_without_conditions.txt", "rule_output_location": "resources/single_rule_without_conditions.json"},
        {"rule_location": "resources/single_rule_without_errors.txt", "rule_output_location": "resources/single_rule_without_errors.json"},
    ]

    def test_rule_parser(self):
        for case in self.test_cases:
            rule_location = case["rule_location"]
            rule_output_location = case["rule_output_location"]
            
            rule = create_rule(rule_location)
            rule_dict = rule.to_dict()
            actual_output = json.dumps(rule_dict,indent=2)
            expected_output = ""
            with open(rule_output_location, 'r') as file:
                expected_output = file.read()
            self.assertMultiLineEqual(actual_output,expected_output)

if __name__ == '__main__':
    unittest.main()    