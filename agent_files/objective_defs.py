CMO_schema = '''{
  "title": "CatalogMaintenanceObjective",
  "type": "object",
  "properties": {
    "sensor_name": {
      "type": "string",
      "description": "String Names of Sensor to perform Catalog Maintenance with."
    },
    "data_mode": {
      "type": "string",
      "description": "String type for the Machina Common DataModeType being generated."
    },
    "classification_marking": {
      "type": "string",
      "description": "Classification level of objective intents."
    },
    "patience_minutes": {
      "type": "integer",
      "default": 30,
      "description": "Amount of time to wait until it's assumed a `SENT` intent failed."
    },
    "end_time_offset_minutes": {
      "type": "integer",
      "default": 20,
      "description": "Amount of minutes into the future to let astroplan schedule an intent."
    },
    "objective_name": {
      "type": "string",
      "default": "Catalog Maintenance Objective",
      "description": "The common name for this objective."
    },
    "objective_start_time": {
      "type": "string",
      "format": "date-time",
      "default": null,
      "description": "The earliest time when the objective should begin execution."
    },
    "objective_end_time": {
      "type": "string",
      "format": "date-time",
      "default": null,
      "description": "The earliest time when the objective should end execution."
    },
    "priority": {
      "type": "integer",
      "default": 10,
      "description": "Astroplan Scheduler Priority."
    }
  },
  "required": ["sensor_name", "data_mode", "classification_marking"]
}
'''

PRO_schema = '''{
  "title": "PeriodicRevisitObjective",
  "type": "object",
  "properties": {
    "target_id": {
      "type": "integer",
      "description": "5 Digit RSO satcat id."
    },
    "sensor_name": {
      "type": "string",
      "description": "Name of Sensor to perform periodic revisit with."
    },
    "data_mode": {
      "type": "string",
      "description": "String type for the Machina Common DataModeType being generated."
    },
    "classification_marking": {
      "type": "string",
      "description": "Classification level of objective intents."
    },
    "revisits_per_hour": {
      "type": "integer",
      "default": 1,
      "description": "Desired number of times to observe each target each hour."
    },
    "hours_to_plan": {
      "type": "integer",
      "default": 24,
      "description": "Maximum hours to plan."
    },
    "objective_name": {
      "type": "string",
      "default": "Periodic Revisit Objective",
      "description": "Name for this objective."
    },
    "objective_start_time": {
      "type": "string",
      "format": "date-time",
      "default": null,
      "description": "The earliest time when the objective should begin execution."
    },
    "objective_end_time": {
      "type": "string",
      "format": "date-time",
      "default": null,
      "description": "The earliest time when the objective should end execution."
    },
    "priority": {
      "type": "integer",
      "default": 2,
      "description": "Astroplan Scheduler Priority, defaults to 2 (3rd highest priority)."
    }
  },
  "required": ["target_id", "sensor_name", "data_mode", "classification_marking"]
}
'''

CMO_example_1 = '''{
        "objective_def_name": "CatalogMaintenanceObjective",
        "end_time_offset_minutes": 20,
        "objective_name": "Catalog Maintenance Objective",
        "priority": 10,
        "sensor_name": "RME00",
        "classification_marking": "U"
        }
'''

CMO_examples = [CMO_example_1]

PRO_example_1 = '''{
  "objective_def_name": "PeriodicRevisitObjective",
  "target_id": 28884,
  "sensor_name": "RME00",
  "revisits_per_hour": 2,
  "data_mode": "TEST",
  "objective_name": "Periodic Revisit Objective",
  }
'''

PRO_examples = [PRO_example_1]

## 119 tokens
PRO_description = """The PeriodicRevisitObjective class in Python 
is designed to create a specific observation objective for a given target, with parameters 
to configure the observation process such as sensor name, data mode, revisit frequency, 
and duration to plan. It sets an end time for the objective, either based on input or a 
default of 10 minutes from the current time, and includes handling for converting input 
string times to datetime objects. This class would be useful in applications that require 
scheduled monitoring or tracking of specific targets (such as celestial objects or satellites) 
through designated sensors, allowing for controlled and periodic observations.
"""

PRO_queries = [
    "Track object 54321 with sensor RME03, revisiting once per hour for the next 24 hours",
    "Track object 12345 with sensor RME08, revisiting twice per hour for the next 16 hours",
    "Set up a periodic revisit for satellite 27871 using sensor RME02 in TEST data mode."
]

## 108 tokens
CMO_description = """The CatalogMaintenanceObjective class 
represents a scheduling objective for catalog maintenance using a specific sensor 
and algorithm, most likely related to astronomical observations or tracking. It 
specifies parameters such as the sensor's name, data mode, scheduling priority, 
timing constraints, and classification marking, providing control over how the 
maintenance task is to be executed. By allowing precise configuration of these 
aspects, it seems to facilitate optimized scheduling in a system where timing 
and priority must be meticulously managed, such as in an observation or tracking 
environment. Useful for satellite or astronomical observation planning.
"""

CMO_queries = [
    (
        "Create a new catalog maintenance for sensor RME01, "
        "using the TEST data mode and a 'U' classification marking."
    ),
    (
        "Create a new maintenance for sensor RME09, "
        "using the TEST data mode, a 'U' classification marking, and "
        "a priority of 6."
    ),
    (
        "Create a new catalog maintenance for sensor RME12, "
        "using the TEST data mode, a 'V' classification marking, and "
        "wait for 45 mins before assuming the SENT intent failed."
    ),
    (
        "Create a new maintenance for sensor RME25, "
        "using the TEST data mode, a 'U' classification marking, and "
        "end the objective after 25 mins."
    )
]
