import unittest

from objective_utils import get_objective, get_embedding_fn
from agent_files.objective_defs import CMO_queries, PRO_queries

class ObjectivesTestCase(unittest.TestCase):
    def setUp(self):
        self.embedding_fn = get_embedding_fn()
        
    def test_get_objective(self):
        for cmo_q in CMO_queries:
            objective = get_objective(task=cmo_q,
                                      embedding_fn=self.embedding_fn)
            self.assertEqual(str(objective.name), "CatalogMaintenanceObjective")
        for pro_q in PRO_queries:
            objective = get_objective(task=pro_q,
                                      embedding_fn=self.embedding_fn)
            self.assertEqual(str(objective.name), "PeriodicRevisitObjective")
