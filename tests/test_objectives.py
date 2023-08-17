import unittest

from objective_utils import get_objective, get_embedding_fn, calculate_confidence
from agent_files.objective_defs import CMO_queries, PRO_queries

from langchain.schema.output_parser import OutputParserException
from langchain.output_parsers import PydanticOutputParser
from agent_files.objectives import CatalogMaintenanceObjective, PeriodicRevisitObjective


class ObjectivesTestCase(unittest.TestCase):
    def setUp(self):
        self.embedding_fn = get_embedding_fn()
        
    def test_get_objective(self):
        for cmo_q in CMO_queries:
            objective, _ = get_objective(task=cmo_q,
                                      embedding_fn=self.embedding_fn)
            self.assertEqual(str(objective.name), "CatalogMaintenanceObjective")
        for pro_q in PRO_queries:
            objective, _ = get_objective(task=pro_q,
                                      embedding_fn=self.embedding_fn)
            self.assertEqual(str(objective.name), "PeriodicRevisitObjective")

    def test_confidence(self):
        test_cosine_sims = [1, 0.999, 0.99, 0.9]
        confidence_percentage = calculate_confidence(test_cosine_sims)
        self.assertEqual(f"{confidence_percentage:.2f}", "66.24")

    def test_pydantic(self):
        test_response1 = """{
        "objective_def_name": "CatalogMaintenanceObjective",
        "end_time_offset_minutes": 20,
        "objective_name": "Catalog Maintenance Objective",
        "priority": 10,
        "sensor_name": "RME01",
        "classification_marking": "U",
        "data_mode": "TEST"
        }
        """
        parser_1 = PydanticOutputParser(pydantic_object=CatalogMaintenanceObjective)
        parsed_response1 = parser_1.parse(test_response1)
        self.assertEqual(parsed_response1.sensor_name, "RME01")
        test_response2 = """{
        "objective_def_name": "PeriodicRevisitObjective",
        "target_id": 28884,
        "sensor_name": "RME00",
        "revisits_per_hour": 2,
        "data_mode": "TEST",
        "classification_marking": "U",
        "objective_name": "Periodic Revisit Objective"
        }
        """
        parser_2 = PydanticOutputParser(pydantic_object=PeriodicRevisitObjective)
        parsed_response2 = parser_2.parse(test_response2)
        self.assertEqual(parsed_response2.target_id, 28884)
