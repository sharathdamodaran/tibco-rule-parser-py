import unittest
import sys
sys.path.append('../../src')
from model.Rule import Rule

class TestRule(unittest.TestCase):
    def test_rule_with_declaration_and_summary(self):
        declaration_section = """LOCAL var1, var2, var3;
        RuleName(param1, param2, param3);"""
        summary_section = """| Summary : This is a rule summary                     | 
        | Keywords: FRAMEWORK,BATCH,UPDATE                                          |
        | Unit    : FRAME                                         Library: SITE     |"""

        rule = Rule(declaration_section, summary_section)
        rule.process_declaration_section(declaration_section)

        self.assertEqual(rule.variables, ["var1", "var2", "var3"])
        self.assertEqual(rule.parameters, ["param1", "param2", "param3"])
        self.assertEqual(rule.summary, "This is a rule summary")
        self.assertEqual(rule.unit, "FRAME")

    def test_rule_with_invalid_statement(self):
        declaration_section = "INVALID STATEMENT"
        summary_section = "INVALID SUMMARY"
        rule = Rule(declaration_section, summary_section)

        self.assertEqual(rule.variables, [])
        self.assertEqual(rule.parameters, [])

    def test_rule_with_empty_declaration_and_summary(self):
        declaration_section = ""
        summary_section = """| Summary : This is a rule summary                     | 
        | Keywords: FRAMEWORK,BATCH,UPDATE                                          |
        | Unit    : FRAME                                         Library: SITE     |"""

        rule = Rule(declaration_section, summary_section)
        rule.process_declaration_section(declaration_section)

        self.assertEqual(rule.variables, [])
        self.assertEqual(rule.parameters, [])
        self.assertEqual(rule.summary, "This is a rule summary")
        self.assertEqual(rule.unit, "FRAME")
        
    def test_rule_with_declaration_and_empty_summary(self):
        declaration_section = """LOCAL var1, var2, var3;
        RuleName(param1, param2, param3);"""
        summary_section = ""

        rule = Rule(declaration_section, summary_section)
        rule.process_declaration_section(declaration_section)

        self.assertEqual(rule.variables, ["var1", "var2", "var3"])
        self.assertEqual(rule.parameters, ["param1", "param2", "param3"])

if __name__ == '__main__':
    unittest.main()