import unittest
import sys
sys.path.append('../../src')
from model.Dependency import Dependency

class TestDependency(unittest.TestCase):
    def test_with_rule_call(self):
        statement = "CALL rule_name;"
        is_dependency, dependency = Dependency.create(statement)
        self.assertTrue(is_dependency)
        self.assertEqual(dependency.type, "Rule")
        self.assertEqual(dependency.value, "rule_name")

    def test_with_rule_call_and_parameters(self):
        statement = "CALL rule_name(param1, param2)"
        is_dependency, dependency = Dependency.create(statement)
        self.assertTrue(is_dependency)
        self.assertEqual(dependency.type, "Rule")
        self.assertEqual(dependency.value, "rule_name")

    def test_with_rule_call_and_parameters_with_semicolon(self):
        statement = "CALL rule_name(param1, param2);"
        is_dependency, dependency = Dependency.create(statement)
        self.assertTrue(is_dependency)
        self.assertEqual(dependency.type, "Rule")
        self.assertEqual(dependency.value, "rule_name")
    
    def test_with_rule_call_inside(self):
        statement = "ROUND(LMXX_FN_DATEDIFF(DSP_MONDAY, BATCH_MONDAY));"
        is_dependency, dependency = Dependency.create(statement)
        self.assertTrue(is_dependency)
        self.assertEqual(dependency.type, "Rule")
        self.assertEqual(dependency.value, "LMXX_FN_DATEDIFF")

    def test_with_database_get(self):
        statement = "GET table_name"
        is_dependency, dependency = Dependency.create(statement)
        self.assertTrue(is_dependency)
        self.assertEqual(dependency.type, "Database")
        self.assertEqual(dependency.value, "table_name")

    def test_with_database_get_and_parameters(self):
        statement = "GET table_name(param1, param2)"
        is_dependency, dependency = Dependency.create(statement)
        self.assertTrue(is_dependency)
        self.assertEqual(dependency.type, "Database")
        self.assertEqual(dependency.value, "table_name")

    def test_with_database_get_and_parameters_with_semicolon(self):
        statement = "GET table_name(param1, param2);"
        is_dependency, dependency = Dependency.create(statement)
        self.assertTrue(is_dependency)
        self.assertEqual(dependency.type, "Database")
        self.assertEqual(dependency.value, "table_name")

    def test_with_invalid_statement(self):
        statement = "INVALID STATEMENT"
        is_dependency, dependency = Dependency.create(statement)
        self.assertFalse(is_dependency)
        self.assertIsNone(dependency)

if __name__ == '__main__':
    unittest.main()