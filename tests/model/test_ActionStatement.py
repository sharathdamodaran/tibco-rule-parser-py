import unittest
import sys
sys.path.append('src')
from model.ActionStatement import ActionStatement

class TestActionStatement(unittest.TestCase):
    def test_create_or_update_single_line_statement(self):
        prev_action = ActionStatement("GET EMPLOYEES(REGION) WHERE POSITION = JOBTITLE;            |     2")
        action_statement = "FORALL EMPLOYEES.SALARY * RATE;                             | 2 2 3"
        result = ActionStatement.create_or_update(action_statement, prev_action)
        self.assertEqual(result[0], True)
        self.assertEqual(result[1].statement, "FORALL EMPLOYEES.SALARY * RATE;")
        self.assertEqual(result[1].values, [True, True, True])

    def test_create_or_update_multi_line_statement(self):
        prev_action = ActionStatement()
        prev_action.statement = "FORALL EMPLOYEES.SALARY * RATE;"
        prev_action.values = [True, True, True]
        action_statement = "EMPLOYEES.SALARY = EMPLOYEES.SALARY + RAISE;|"
        result = ActionStatement.create_or_update(action_statement, prev_action)
        self.assertEqual(result[0], False)
        print(result[1].statement)
        self.assertEqual(result[1].statement, "FORALL EMPLOYEES.SALARY * RATE;\nEMPLOYEES.SALARY = EMPLOYEES.SALARY + RAISE;")
        self.assertEqual(result[1].values, [True, True, True])

if __name__ == '__main__':
    unittest.main()