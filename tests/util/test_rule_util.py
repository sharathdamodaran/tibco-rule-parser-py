import unittest
from unittest.mock import MagicMock
import sys
sys.path.append('src')
from repository.neo4j_repository import Neo4jRepository
from model.RuleNode import RuleNode
from util.rule_util import RuleUtil

class TestRuleUtil(unittest.TestCase):
    def setUp(self):
        self.neo4j_repository = MagicMock(spec=Neo4jRepository)
        self.rule_util = RuleUtil(self.neo4j_repository)

    def test_get_rule(self):
        id = "123"
        code = "Rule Code"
        properties = {'id': id, 'code': code}
        record = {'n': MagicMock(as_node=MagicMock(return_value=MagicMock(as_map=MagicMock(return_value=properties))))}
        self.neo4j_repository.get_node.return_value = record

        rule = self.rule_util.get_rule(id)

        self.assertEqual(rule.name, id)
        self.assertEqual(rule.code, code)
        self.assertEqual(rule.summary, '')
        self.assertIsNone(rule.child_rule)

    def test_update_summary(self):
        id = "123"
        summary = "Rule Summary"
        self.rule_util.update_summary(id, summary)

        self.neo4j_repository.update_property.assert_called_once_with(id, 'summary', summary)

    def test_get_child_rules(self):
        id = "123"
        child_id = "456"
        child_code = "Child Rule Code"
        child_summary = "Child Rule Summary"
        properties = {'id': child_id, 'code': child_code, 'summary': child_summary}
        record = {'c': MagicMock(as_node=MagicMock(return_value=MagicMock(as_map=MagicMock(return_value=properties))))}
        self.neo4j_repository.get_child_node.return_value = [record]

        child_rules = self.rule_util.get_child_rules(id)

        self.assertEqual(len(child_rules), 1)
        self.assertEqual(child_rules[0].name, child_id)
        self.assertEqual(child_rules[0].code, child_code)
        self.assertEqual(child_rules[0].summary, child_summary)
        self.assertEqual(child_rules[0].child_rule, [])

if __name__ == '__main__':
    unittest.main()