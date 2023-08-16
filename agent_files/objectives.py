from dataclasses import dataclass
from typing import List, Optional

from agent_files.objective_defs import CMO_schema, CMO_description, CMO_examples
from agent_files.objective_defs import PRO_schema, PRO_description, PRO_examples

@dataclass
class Objective:
    name: str
    schema: str
    description: str
    examples: Optional[List[str]]


catalog_maintenance = Objective(name='CatalogMaintenanceObjective',
                                schema=CMO_schema,
                                description=CMO_description,
                                examples=CMO_examples
                                )

periodic_revisit = Objective(name='PeriodicRevisitObjective',
                             schema=PRO_schema,
                             description=PRO_description,
                             examples=PRO_examples
                             )

kv_objectives = {
    CMO_description: catalog_maintenance,
    PRO_description: periodic_revisit,
    }
