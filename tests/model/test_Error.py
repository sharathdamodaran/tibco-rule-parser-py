import unittest
import sys
sys.path.append('src')
from model.Error import Error

class TestError(unittest.TestCase):
   def test_error_with_single_statement(self):
        statements = "GETFAIL : \nMSG_LOG('ERROR');"
        error = Error(statements)
        self.assertEqual(error.type, "Exception")
        self.assertEqual(error.value, "GETFAIL")
        self.assertEqual(error.actions[0].value, "MSG_LOG('ERROR');")

   def test_error_with_multiple_statement(self):
        statements = "GETFAIL : \nMSG_LOG('ERROR'); \nMSG_EVENT('ERROR');"
        error = Error(statements)
        self.assertEqual(error.type, "Exception")
        self.assertEqual(error.value, "GETFAIL")
        self.assertEqual(error.actions[0].value, "MSG_LOG('ERROR');")
        self.assertEqual(error.actions[1].value, "MSG_EVENT('ERROR');")

if __name__ == '__main__':
    unittest.main()