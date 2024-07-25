import unittest
import sys
sys.path.append('../../src')
from model.Condition import Condition
from model.ActionStatement import ActionStatement
from model.Expression import Expression

class TestExpression(unittest.TestCase):
    def test_init_with_single_condition(self):
        condition = Condition("JOBTITLE = 'SENIOR ANALYST';  | Y")
        conditions = [
            condition
        ]
        is_new, action = ActionStatement.create_or_update("GET EMPLOYEES(REGION) WHERE POSITION = JOBTITLE; | 2", None)
        action_statements = [
            action
        ]
        expression = Expression(0, action_statements, conditions)
        self.assertEqual(expression.type, "Condition")
        self.assertEqual(expression.value, "JOBTITLE = 'SENIOR ANALYST';")
        self.assertEqual(len(expression.actions), 1)
        self.assertEqual(expression.actions[0].value, "GET EMPLOYEES(REGION) WHERE POSITION = JOBTITLE;")

    def test_init_with_single_condition(self):
        condition = Condition("JOBTITLE = 'SENIOR ANALYST';  | Y N")
        conditions = [
            condition
        ]
        is_new, action1 = ActionStatement.create_or_update("RATE = 0.02; | 1  ", None)
        is_new, action2 = ActionStatement.create_or_update("RATE = 0.05; |   1", None)
        is_new, action3 = ActionStatement.create_or_update("GET EMPLOYEES(REGION) WHERE POSITION = JOBTITLE; | 2 2", None)
        action_statements = [
            action1, action2, action3
        ]
        expression1 = Expression(0, action_statements, conditions)
        self.assertEqual(expression1.type, "Condition")
        self.assertEqual(expression1.value, "JOBTITLE = 'SENIOR ANALYST';")
        self.assertEqual(len(expression1.actions), 2)
        self.assertEqual(expression1.actions[0].value, "RATE = 0.02;")
        expression2 = Expression(1, action_statements, conditions)
        self.assertEqual(expression2.type, "Default")
        self.assertEqual(len(expression2.actions), 2)
        self.assertEqual(expression2.actions[0].value, "RATE = 0.05;")

if __name__ == '__main__':
    unittest.main()