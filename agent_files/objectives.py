from dataclasses import dataclass
from typing import List, Optional
from pydantic import BaseModel, Field, validator, StrictInt
from datetime import datetime

from agent_files.objective_defs import CMO_description, CMO_examples, CMO_schema, CMO_required, CMO_data
from agent_files.objective_defs import PRO_description, PRO_examples, PRO_schema, PRO_required, PRO_data
from agent_files.objective_defs import SO_schema, SO_required, SO_description, SO_data, SO_examples
from agent_files.objective_defs import SFO_schema, SFO_required, SFO_description, SFO_data, SFO_examples
from agent_files.objective_defs import QWO_schema, QWO_required, QWO_description, QWO_data, QWO_examples

@dataclass
class Objective:
    name: str
    obj_name: str
    schema: str
    required: str
    description: str
    data: dict
    examples: Optional[List[str]]


catalog_maintenance = Objective(name='CatalogMaintenanceObjective',
                                obj_name='Catalog Maintenance Objective',
                                schema=CMO_schema,
                                required=CMO_required,
                                description=CMO_description,
                                data=CMO_data,
                                examples=CMO_examples
                                )

periodic_revisit = Objective(name='PeriodicRevisitObjective',
                             obj_name='Periodic Revisit Objective',
                             schema=PRO_schema,
                             required=PRO_required,
                             description=PRO_description,
                             data=PRO_data,
                             examples=PRO_examples
                             )

search_def = Objective(name='SearchObjective',
                       obj_name='Search Objective',
                       schema=SO_schema,
                       required=SO_required,
                       description=SO_description,
                       data=SO_data,
                       examples=SO_examples
                       )

schedule_filler_def = Objective(name='ScheduleFillerObjective',
                                obj_name='Schedule Filler Objective',
                                schema=SFO_schema,
                                required=SFO_required,
                                description=SFO_description,
                                data=SFO_data,
                                examples=SFO_examples
                                )

quality_window_def = Objective(name='QualityWindowObjective',
                               obj_name='Quality Window Objective',
                               schema=QWO_schema,
                               required=QWO_required,
                               description=QWO_description,
                               data=QWO_data,
                               examples=QWO_examples
                               )


kv_objectives = {
    CMO_description: catalog_maintenance,
    PRO_description: periodic_revisit,
    SO_description: search_def,
    SFO_description: schedule_filler_def,
    QWO_description: quality_window_def,
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
    target_id: StrictInt = Field(description="5 Digit RSO satcat id.")
    sensor_name: str = Field(description="Name of Sensor to perform periodic revisit with.")
    data_mode: str = Field(description="String type for the Machina Common DataModeType being generated.")
    classification_marking: str = Field(description="Classification level of objective intents.")
    revisits_per_hour: int = Field(default=1, description="Desired number of times to observe each target each hour.")
    hours_to_plan: int = Field(default=24, description="Maximum hours to plan.")
    objective_name: str = Field(default="Periodic Revisit Objective", description="Name for this objective.")
    objective_start_time: datetime = Field(default=None, description="The earliest time when the objective should begin execution.")
    objective_end_time: datetime = Field(default=None, description="The earliest time when the objective should end execution.")
    priority: int = Field(default=2, description="Astroplan Scheduler Priority, defaults to 2 (3rd highest priority).")

    @validator("target_id", pre=True)
    def validate_target_id(cls, field):
        if field is None or field == "":
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

class SearchObjective(BaseModel):
    target_id: StrictInt = Field(description="5 Digit RSO satcat id")
    sensor_name: str = Field(description="Name of Sensor to perform search")
    data_mode: str = Field(description="String type for the Machina Common DataModeType being generated.")
    classification_marking: str = Field(description="Classification level of objective intents.")
    initial_offset: int = Field(default=30, description="Amount of time before the RSO's current state to start the search at (s). Defaults to 30. Max is 1800.")
    final_offset: int = Field(default=30, description="Amount of time after the RSO's current state to start the search at (s). Defaults to 30. Max is 1800.")
    objective_name: str = Field(default="Search Objective", description="The common name for this objective.")
    frame_overlap_percentage: float = Field(default=0.5, description="Percentage of frames that will overlap from one to the next. Defaults to 0.5")
    objective_start_time: datetime = Field(default=None, description="The earliest time when the objective should begin execution.")
    objective_end_time: datetime = Field(default=None, description="The earliest time when the objective should end execution.")
    number_of_frames: int = Field(default=None, description="Optional number of frames for the search.")
    integration_time: int = Field(default=None, description="Optional integration time for the search.")
    priority: int = Field(default=0, description="Astroplan Scheduler Priority, defaults to 0 (highest priority).")
    end_time_offset_minutes: int = Field(default=20, description="Amount of minutes into the future to let astroplan schedule an intent. Defaults to 20 minutes.")

    @validator("initial_offset", "final_offset")
    def validate_offsets(cls, value):
        if value < 0 or value > 1800:
            raise ValueError("Offsets must be between 0 and 1800 seconds")
        return value

    @validator("frame_overlap_percentage")
    def validate_frame_overlap_percentage(cls, value):
        if value < 0 or value > 1:
            raise ValueError("Frame overlap percentage must be between 0 and 1")
        return value
    
    @validator("target_id", pre=True)
    def validate_target_id(cls, field):
        if field is None or field == "":
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

class ScheduleFillerObjective(BaseModel):
    sensor_name: str = Field(description="Name of Sensor to perform Schedule Filler with.")
    data_mode: str = Field(description="String type for the Machina Common DataModeType being generated.")
    classification_marking: str = Field(description="Classification level of objective intents.")
    scheduling_density: float = Field(default=15.0, description="Length of intent scheduling blocks (minutes).")
    hours_to_plan: int = Field(default=24, description="Maximum hours to plan.")
    objective_name: str = Field(default="New Schedule Filler Objective", description="The common name for this objective.")
    objective_start_time: datetime = Field(default=None, description="The earliest time when the objective should begin execution.")
    objective_end_time: datetime = Field(default=None, description="The earliest time when the objective should end execution.")
    priority: int = Field(default=10, description="Astroplan Scheduler Priority.")

    @validator("sensor_name", "data_mode", "classification_marking")
    def validate_required_fields(cls, field):
        if field == "":
            raise ValueError(f"{field} must be filled in!")
        return field

## For QualityWindowObjective def
class StateVector(BaseModel):
    timestamp: datetime
    x_kilometers: float
    y_kilometers: float
    z_kilometers: float
    x_dot_kilometers_per_second: float
    y_dot_kilometers_per_second: float
    z_dot_kilometers_per_second: float

class Payload(BaseModel):
    satNo: int
    priority: int
    state_vector: StateVector
    window_start: datetime
    window_end: datetime
    position_accuracy: float
    velocity_accuracy: int
    
class QualityWindowObjective(BaseModel):
    sensor_name: str = Field(description="String Name of Sensor to perform Quality Window with.")
    #payload_list: str = Field(description="list[dict] of payload info needed for this objective.")
    payload_list: List[Payload] = Field(description="List[Payload] of payload info needed for this objective.")
    data_mode: str = Field(description="String type for the Machina Common DataModeType being generated.", default="REAL")
    classification_marking: str = Field(description="Classification level of objective intents.", default="U")
    scheduling_density: float = Field(default=5.0, description="Scheduling density for the objective.")
    hours_to_plan: int = Field(default=24, description="Number of hours to plan for the objective.")
    objective_name: str = Field(default="Quality Window Objective", description="The common name for this objective.")
    objective_start_time: datetime = Field(default=None, description="The earliest time when the objective should begin execution.")
    objective_end_time: datetime = Field(default=None, description="The earliest time when the objective should end execution.")
    priority: int = Field(default=1, description="Astroplan Scheduler Priority.")

    @validator("sensor_name", "payload_list", "data_mode", "classification_marking")
    def validate_fields(cls, field):
        if field == "":
            raise ValueError(f"{field} must be filled in!")
        return field
