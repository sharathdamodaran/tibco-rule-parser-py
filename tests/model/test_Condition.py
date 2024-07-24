import unittest
import sys
sys.path.append('../../src')
from model.Condition import Condition

class TestCondition(unittest.TestCase):
    def test_condition_with_single_value(self):
        statement = "condition_statement| Y "
        condition = Condition(statement)
        self.assertEqual(condition.condition_statement, "condition_statement")
        self.assertEqual(condition.values, [True])

    def test_condition_with_multiple_value(self):
        statement = "condition_statement| Y N"
        condition = Condition(statement)
        self.assertEqual(condition.condition_statement, "condition_statement")
        self.assertEqual(condition.values, [True, False])
        
    def test_condition_with_pipe(self):
        statement = "condition || statement| Y N"
        condition = Condition(statement)
        self.assertEqual(condition.condition_statement, "condition || statement")
        self.assertEqual(condition.values, [True, False])

if __name__ == '__main__':
    unittest.main()