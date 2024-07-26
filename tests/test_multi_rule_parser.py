import unittest
from unittest.mock import patch, call
import sys
sys.path.append('src')
import model
from multi_rule_parser import create_parent_child_rule_map
from multi_rule_parser import write_rules_to_files

class TestWriteRulesToFiles(unittest.TestCase):
    @patch('multi_rule_parser.os.makedirs')
    @patch('builtins.open', create=True)
    def test_write_rules_to_files(self, mock_open, mock_makedirs):
        base_path = "resources/"
        rule_folder = "rules/"
        rule_name = "multi_rule_1.txt"
        file_content = """
        Rule 1 Content
        ++++++++++++++++++++++++++++++++++++++
        Rule 2 Content
        """
        
        mock_open.return_value.__enter__.return_value.read.return_value = file_content
        
        write_rules_to_files(base_path, rule_folder, rule_name)
        
        mock_makedirs.assert_called_once_with(base_path + rule_folder, exist_ok=True)
        
        expected_calls = [
            call("resources/multi_rule_1.txt", 'r'),
            call(base_path + rule_folder + "Rule1", 'w'),
            call(base_path + rule_folder + "Rule2", 'w')
        ]
        self.assertEqual(mock_open.call_args_list, expected_calls)
        
class TestCreateParentChildRuleMap(unittest.TestCase):        
    @patch('multi_rule_parser.os.makedirs')
    @patch('multi_rule_parser.os.listdir')
    @patch('builtins.open', create=True)
    def test_create_parent_child_rule_map(self, mock_open, mock_listdir, mock_makedirs):
        base_path = "resources/"
        rule_folder = "rules/"
        ast_folder = "ast/"
        file_content = """1
 Page 1                                    Saved On:                By
 EMPLOYEES_RAISE(JOBTITLE, REGION);
 LOCAL RAISE, RATE;
 +---------------------------------------------------------------------------+
 | Summary : Call this rule to invoke update mode in batch                   |
 | Keywords: FRAMEWORK,BATCH,UPDATE                                          |
 | Unit    : FRAME                                         Library: SITE     |
 +---------------------------------------------------------------------------+
 ------------------------------------------------------------+--------------
 RATE = 0.1;                                                 | 1            
 GET EMPLOYEES(REGION) WHERE POSITION = JOBTITLE;            | 2            
 FORALL EMPLOYEES.SALARY * RATE;                             | 3            
      EMPLOYEES.SALARY = EMPLOYEES.SALARY + RAISE;           |     
      CALL REPLACE_SALARY(REGION);                           |   
      CALL MSGLOG(EMPLOYEES.LNAME ||‘NOW EARNS‘||            |  
      EMPLOYEES.SALARY);                                     |       
 END;                                                        | 
 ------------------------------------------------------------+--------------"""

        mock_listdir.return_value = ['Rule1']

        mock_open.return_value.__enter__.return_value.read.return_value = file_content
        

        rule_map = create_parent_child_rule_map(base_path, rule_folder)

        mock_listdir.assert_called_once_with(base_path + rule_folder)
        mock_makedirs.assert_called_once_with(base_path + ast_folder, exist_ok=True)
        
        expected_calls = [
            call(base_path + rule_folder + "Rule1", 'r'),
            call(base_path + rule_folder + "Rule1", 'r'),
            call(base_path + ast_folder + "EMPLOYEES_RAISE.json", 'w')
        ]
        self.assertEqual(mock_open.call_args_list, expected_calls)
        self.assertEqual(len(rule_map), 1)
        self.assertIn("EMPLOYEES_RAISE", rule_map)
        rule_node = rule_map["EMPLOYEES_RAISE"]
        self.assertEqual(rule_node.name, "EMPLOYEES_RAISE")

if __name__ == '__main__':
    unittest.main()