from dataclasses import dataclass
from typing import List, Optional
from pydantic import BaseModel, Field, validator
from datetime import datetime

from agent_files.objective_defs import CMO_schema, CMO_description, CMO_examples
from agent_files.objective_defs import CMO_schema_short, CMO_required, CMO_data
from agent_files.objective_defs import PRO_schema, PRO_description, PRO_examples
from agent_files.objective_defs import PRO_schema_short, PRO_required, PRO_data

@dataclass
class Objective:
    name: str
    obj_name: str
    schema: str
    schema_short: str
    required: str
    description: str
    data: dict
    examples: Optional[List[str]]


catalog_maintenance = Objective(name='CatalogMaintenanceObjective',
                                obj_name='Catalog Maintenance Objective',
                                schema=CMO_schema,
                                schema_short=CMO_schema_short,
                                required=CMO_required,
                                description=CMO_description,
                                data=CMO_data,
                                examples=CMO_examples
                                )

periodic_revisit = Objective(name='PeriodicRevisitObjective',
                             obj_name='Periodic Revisit Objective',
                             schema=PRO_schema,
                             schema_short=PRO_schema_short,
                             required=PRO_required,
                             description=PRO_description,
                             data=PRO_data,
                             examples=PRO_examples
                             )

kv_objectives = {
    CMO_description: catalog_maintenance,
    PRO_description: periodic_revisit,
    }

class CatalogMaintenanceObjective(BaseModel):
    sensor_name: str = Field(description="String Names of Sensor to perform Catalog Maintenance with.")
    data_mode: str = Field(description="String type for the Machina Common DataModeType being generated.")
    classification_marking: str = Field(description="Classification level of objective intents.")
    patience_minutes: int = Field(default=30, description="Amount of time to wait until it's assumed a `SENT` intent failed.")
    end_time_offset_minutes: int = Field(default=20, description="Amount of minutes into the future to let astroplan schedule an intent.")
    objective_name: str = Field(default="Catalog Maintenance Objective", description="The common name for this objective.")
    objective_start_time: datetime = Field(default=None, description="The earliest time when the objective should begin execution.")
    objective_end_time: datetime = Field(default=None, description="The earliest time when the objective should end execution.")
    priority: int = Field(default=10, description="Astroplan Scheduler Priority.")

    @validator("sensor_name")
    def validate_sensor_name(cls, field):
        if field == "":
            raise ValueError("sensor_name must be filled in!")
        return field

    @validator("data_mode")
    def validate_data_mode(cls, field):
        if field == "":
            raise ValueError("data_mode must be filled in!")
        return field

    @validator("classification_marking")
    def validate_classification_marking(cls, field):
        if field == "":
            raise ValueError("classification_marking must be filled in!")
        return field
    
class PeriodicRevisitObjective(BaseModel):
    target_id: int = Field(description="5 Digit RSO satcat id.")
    sensor_name: str = Field(description="Name of Sensor to perform periodic revisit with.")
    data_mode: str = Field(description="String type for the Machina Common DataModeType being generated.")
    classification_marking: str = Field(description="Classification level of objective intents.")
    revisits_per_hour: int = Field(default=1, description="Desired number of times to observe each target each hour.")
    hours_to_plan: int = Field(default=24, description="Maximum hours to plan.")
    objective_name: str = Field(default="Periodic Revisit Objective", description="Name for this objective.")
    objective_start_time: datetime = Field(default=None, description="The earliest time when the objective should begin execution.")
    objective_end_time: datetime = Field(default=None, description="The earliest time when the objective should end execution.")
    priority: int = Field(default=2, description="Astroplan Scheduler Priority, defaults to 2 (3rd highest priority).")

    @validator("target_id")
    def validate_target_id(cls, field):
        if field is None:
            raise ValueError("target_id must be filled in!")
        return field

    @validator("sensor_name")
    def validate_sensor_name(cls, field):
        if field == "":
            raise ValueError("sensor_name must be filled in!")
        return field

    @validator("data_mode")
    def validate_data_mode(cls, field):
        if field == "":
            raise ValueError("data_mode must be filled in!")
        return field

    @validator("classification_marking")
    def validate_classification_marking(cls, field):
        if field == "":
            raise ValueError("classification_marking must be filled in!")
        return field