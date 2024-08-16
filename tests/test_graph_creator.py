import unittest
from unittest.mock import MagicMock, patch
import sys
sys.path.append('src')
from repository.neo4j_repository import Neo4jRepository
from repository.llm_repository import LLMRepository
from model.RuleNode import RuleNode
from util.rule_util import RuleUtil
from graph_creator import update_summaries
from graph_creator import update_node_levels

class TestUpdateSummaries(unittest.TestCase):
    @patch('graph_creator.os.getenv')
    @patch('graph_creator.Neo4jRepository')
    @patch('graph_creator.RuleUtil')
    @patch('graph_creator.LLMRepository')
    def test_update_summaries(self, mock_llm_repository, mock_rule_util, mock_neo4j_repository, mock_getenv):
        mock_getenv.side_effect = ["user", "password", "uri"]

        mock_neo4j = MagicMock(spec=Neo4jRepository)
        mock_neo4j_repository.return_value = mock_neo4j

        mock_rule_util_instance = MagicMock(spec=RuleUtil)
        mock_rule_util.return_value = mock_rule_util_instance

        mock_llm_repository_instance = MagicMock(spec=LLMRepository)
        mock_llm_repository.return_value = mock_llm_repository_instance

        mock_neo4j.get_max_level.return_value = 0

        mock_neo4j.get_nodes_at_level.return_value = ["rule1"]

        mock_rule = MagicMock(spec=RuleNode)
        mock_rule_util_instance.get_rule.return_value = mock_rule

        mock_child_rule = MagicMock(spec=RuleNode)
        mock_rule_util_instance.get_child_rules.return_value = [mock_child_rule]

        mock_rule_summary = "Rule Summary"
        mock_llm_repository_instance.translate_code.return_value = mock_rule_summary

        update_summaries()

        mock_neo4j_repository.assert_called_once_with("uri", "user", "password")
        mock_neo4j.get_max_level.assert_called_once()
        mock_neo4j.get_nodes_at_level.assert_called_once_with(0)
        mock_rule_util.assert_called_once_with(mock_neo4j)
        mock_rule_util_instance.get_rule.assert_called_once_with("rule1")
        mock_rule_util_instance.get_child_rules.assert_called_once_with("rule1")
        mock_llm_repository_instance.translate_code.assert_called_once_with("http://localhost:11434/api/generate", mock_rule, [mock_child_rule])
        mock_rule_util_instance.update_summary.assert_called_once_with("rule1", mock_rule_summary)
        mock_neo4j.close.assert_called_once()

class TestUpdateNodeLevels(unittest.TestCase):
    @patch('graph_creator.os.getenv')
    @patch('graph_creator.Neo4jRepository')
    def test_update_node_levels(self, mock_neo4j_repository, mock_getenv):
        mock_getenv.side_effect = ["user", "password", "uri"]

        mock_neo4j = MagicMock(spec=Neo4jRepository)
        mock_neo4j_repository.return_value = mock_neo4j

        mock_root_id = "root_id"
        mock_neo4j.get_root_node.return_value = mock_root_id

        update_node_levels()

        mock_neo4j_repository.assert_called_once_with("uri", "user", "password")
        mock_neo4j.get_root_node.assert_called_once()
        mock_neo4j.update_root_node_level.assert_called_once_with(mock_root_id)
        mock_neo4j.update_child_node_levels.assert_called_once_with(mock_root_id)
        mock_neo4j.close.assert_called_once()


if __name__ == '__main__':
    unittest.main()