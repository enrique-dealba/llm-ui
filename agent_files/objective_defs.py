CMO_schema = '''{
  "title": "CatalogMaintenanceObjective",
  "type": "object",
  "sensor_name": { "type": "string" },
  "data_mode": { "type": "string" },
  "classification_marking": { "type": "string", "default": "U" },
  "patience_minutes": { "type": "integer", "default": 30 },
  "end_time_offset_minutes": { "type": "integer", "default": 20 },
  "objective_name": { "type": "string", "default": "Catalog Maintenance Objective" },
  "objective_start_time": { "type": "string", "format": "date-time" },
  "objective_end_time": { "type": "string", "format": "date-time" },
  "priority": { "type": "integer", "default": 10 },
  "required": ["sensor_name", "data_mode", "classification_marking"]
}
'''

CMO_required = "sensor_name, data_mode, classification_marking"

CMO_default = """{
  patience_minutes: 30,
  end_time_offset_minutes: 20,
  objective_name: "Catalog Maintenance Objective",
  objective_start_time: "",
  objective_end_time: "",
  priority: 10
}
"""

CMO_data = {
  "title": "CatalogMaintenanceObjective",
  "type": "object",
  "sensor_name": { "type": "string" },
  "data_mode": { "type": "string" },
  "classification_marking": { "type": "string", "default": "U" },
  "patience_minutes": { "type": "integer", "default": 30 },
  "end_time_offset_minutes": { "type": "integer", "default": 20 },
  "objective_name": { "type": "string", "default": "Catalog Maintenance Objective" },
  "objective_start_time": { "type": "string", "format": "date-time" },
  "objective_end_time": { "type": "string", "format": "date-time" },
  "priority": { "type": "integer", "default": 10 },
  "required": ["sensor_name", "data_mode", "classification_marking"]
}

PRO_schema = '''{
  "title": "PeriodicRevisitObjective",
  "type": "object",
  "target_id": { "type": "integer" },
  "sensor_name": { "type": "string" },
  "data_mode": { "type": "string" },
  "classification_marking": { "type": "string", "default": "U" },
  "revisits_per_hour": { "type": "integer", "default": 1 },
  "hours_to_plan": { "type": "integer", "default": 24 },
  "objective_name": { "type": "string", "default": "Periodic Revisit Objective" },
  "objective_start_time": { "type": "string", "format": "date-time" },
  "objective_end_time": { "type": "string", "format": "date-time" },
  "priority": { "type": "integer", "default": 2 },
  "required": ["target_id", "sensor_name", "data_mode", "classification_marking"]
}
'''

PRO_required = "target_id, sensor_name, data_mode, classification_marking"

PRO_default = """{
  revisits_per_hour: 1,
  hours_to_plan: 24,
  objective_name: "Periodic Revisit Objective",
  objective_start_time: "",
  objective_end_time: "",
  priority: 2,
}
"""

PRO_data = {
  "title": "PeriodicRevisitObjective",
  "type": "object",
  "target_id": { "type": "integer" },
  "sensor_name": { "type": "string" },
  "data_mode": { "type": "string" },
  "classification_marking": { "type": "string", "default": "U" },
  "revisits_per_hour": { "type": "integer", "default": 1 },
  "hours_to_plan": { "type": "integer", "default": 24 },
  "objective_name": { "type": "string", "default": "Periodic Revisit Objective" },
  "objective_start_time": { "type": "string", "format": "date-time" },
  "objective_end_time": { "type": "string", "format": "date-time" },
  "priority": { "type": "integer", "default": 2 },
  "required": ["target_id", "sensor_name", "data_mode", "classification_marking"]
}

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
  "revisits_per_hour": 3,
  "data_mode": "TEST",
  "classification_marking": "U",
  "objective_name": "Periodic Revisit Objective",
  }
'''

PRO_examples = [PRO_example_1]

## 119 tokens
PRO_description_prev = """The PeriodicRevisitObjective class in Python 
is designed to create a specific observation objective for a given target, with parameters 
to configure the observation process such as sensor name, data mode, revisit frequency, 
and duration to plan. It sets an end time for the objective, either based on input or a 
default of 10 minutes from the current time, and includes handling for converting input 
string times to datetime objects. This class would be useful in applications that require 
scheduled monitoring or tracking of specific targets (such as celestial objects or satellites) 
through designated sensors, allowing for controlled and periodic observations.
"""

PRO_description = """The PeriodicRevisitObjective class is designed to create a specific observation 
objective for a given target, with parameters to configure the observation process 
such as sensor name, data mode, revisit frequency, and duration. Periodic Revisit sets an end time 
for the objective, either based on input or a default of 10 minutes from the current time, 
and includes handling for converting input string times to datetime objects. Revisit is 
useful in applications that require scheduled monitoring or tracking of specific targets 
(such as celestial objects or satellites) through designated sensors, allowing for controlled 
and periodic observations.
"""

PRO_queries = [
    "Track object 54321 with sensor RME03, revisiting once per hour for the next 24 hours",
    "Track object 12345 with sensor RME08, revisiting twice per hour for the next 16 hours",
    "Set up a periodic revisit for satellite 27871 using sensor RME02 in TEST data mode."
]

## 108 tokens
CMO_description_prev = """The CatalogMaintenanceObjective class 
represents a scheduling objective for catalog maintenance using a specific sensor 
and algorithm, most likely related to astronomical observations or tracking. It 
specifies parameters such as the sensor's name, data mode, scheduling priority, 
timing constraints, and classification marking, providing control over how the 
maintenance task is to be executed. By allowing precise configuration of these 
aspects, it seems to facilitate optimized scheduling in a system where timing 
and priority must be meticulously managed, such as in an observation or tracking 
environment. Useful for satellite or astronomical observation planning.
"""

CMO_description = """The CatalogMaintenanceObjective class represents a scheduling objective for catalog 
maintenance using a specific sensor and algorithm, related to astronomical observations or 
tracking. Catalog Maintenance specifies parameters such as the sensor's name, data mode, scheduling priority, 
timing constraints, and classification marking, providing control over how the maintenance 
task is to be executed. By allowing precise configuration of these parameters, it facilitates 
optimized scheduling in a system where timing and priority are required, such as in an observation 
or tracking environment. CatalogMaintenanceObjective is useful for satellite or astronomical observation planning.
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
        "Create a new catalog maintenance for sensor RME25, "
        "using the TEST data mode, a 'U' classification marking, and "
        "end the objective after 25 mins."
    )
]

## Search Objective
SO_schema = """{
  "title": "SearchObjective",
  "type": "object",
  "target_id": { "type": "integer" },
  "sensor_name": { "type": "string" },
  "data_mode": { "type": "string" },
  "classification_marking": { "type": "string", "default": "U" },
  "initial_offset": { "type": "integer", "default": 30 },
  "final_offset": { "type": "integer", "default": 30 },
  "objective_name": { "type": "string", "default": "Search Objective" },
  "frame_overlap_percentage": { "type": "number", "default": 0.5 },
  "objective_start_time": { "type": "string", "format": "date-time" },
  "objective_end_time": { "type": "string", "format": "date-time" },
  "number_of_frames": { "type": "integer" },
  "integration_time": { "type": "integer" },
  "priority": { "type": "integer", "default": 0 },
  "end_time_offset_minutes": { "type": "integer", "default": 20 },
  "required": ["target_id", "sensor_name", "data_mode", "classification_marking"]
}
"""

SO_data = {
  "title": "SearchObjective",
  "type": "object",
  "target_id": { "type": "integer" },
  "sensor_name": { "type": "string" },
  "data_mode": { "type": "string" },
  "classification_marking": { "type": "string", "default": "U" },
  "initial_offset": { "type": "integer", "default": 30 },
  "final_offset": { "type": "integer", "default": 30 },
  "objective_name": { "type": "string", "default": "Search Objective" },
  "frame_overlap_percentage": { "type": "number", "default": 0.5 },
  "objective_start_time": { "type": "string", "format": "date-time" },
  "objective_end_time": { "type": "string", "format": "date-time" },
  "number_of_frames": { "type": "integer" },
  "integration_time": { "type": "integer" },
  "priority": { "type": "integer", "default": 0 },
  "end_time_offset_minutes": { "type": "integer", "default": 20 },
  "required": ["target_id", "sensor_name", "data_mode", "classification_marking"]
}

SO_required = "target_id, sensor_name, data_mode, classification_marking"

SO_default = """{
  initial_offset: 30,
  final_offset: 30,
  objective_name: "Search Objective",
  frame_overlap_percentage: 0.5,
  objective_start_time: "",
  objective_end_time: "",
  number_of_frames: None,
  integration_time: None,
  priority: 0,
  end_time_offset_minutes: 20,
}
"""

SO_description_prev = '''The SearchObjective class is  used for orchestrating a search operation 
involving satellite sensors. It encapsulates  details of a search pattern along the 
satellite's orbit path, including target ID, sensor name, initial and final offsets, 
frame overlap percentage, objective start and end times, and other related attributes. 
The class constructor checks the validity of specific parameters such as offset limits 
and frame overlap percentages, and sets the objective end time accordingly. It is likely 
to be useful in satellite-based observation systems where precise control and scheduling of 
sensor operations are required, coordinating searches for specific targets along orbital paths.
'''

SO_description = '''The SearchObjective class is used for orchestrating a search operation involving satellite 
sensors. Search encapsulates details of a search pattern along the satellite's orbit path, 
including parameters like target ID, sensor name, initial and final offsets, frame overlap percentage, objective start and end times, and other related fields. The SearchObjective constructor checks the validity of specific parameters such as offset limits and frame overlap percentages, and sets the objective end time accordingly. Useful in satellite-based observation systems where precise control and scheduling of sensor operations are required, coordinating searches for specific targets along orbital paths.
'''

SO_example_1 = '''{
  "objective_def_name": "SearchObjective",
  "objective_name": "Search Objective",
  "target_id": 28884,
  "sensor_name": "RME15",
  "initial_offset": 60,
  "final_offset": 60,
  "objective_start_time": "2023-08-21T18:47:19.059212",
  "objective_end_time": "2023-08-21T18:57:19.059284",
  "data_mode": "TEST",
  "classification_marking": "U"
  }
'''

SO_examples = [SO_example_1]

## Schedule Filler Objective

SFO_description_prev = """The ScheduleFillerObjective class is designed to 
define an objective for scheduling, particularly regarding a sensor's activity. It takes 
various parameters such as the sensor name, data mode, scheduling density, and others, 
allowing the scheduling of blocks with a specific duration and priority within a 24-hour 
time frame. The objective end time can be explicitly set or calculated as 24 hours from 
the current time. Though part of the functionality is inferred due to the missing parent 
class Objective, this class is likely to be used in a broader system that requires detailed 
scheduling of tasks or events, perhaps for astronomical or satellite operations.
"""

SFO_description = """The ScheduleFillerObjective class is used to define an objective for scheduling, particularly 
regarding a sensor's activity. Schedule Filler takes parameters such as the sensor name, data mode, scheduling 
density, and others, allowing the scheduling of blocks with a specific duration and priority within 
a 24-hour time frame. The Schedule Filler's end time can be explicitly set or calculated as 24 hours from 
the current time. ScheduleFillerObjective is useful for detailed scheduling of tasks for astronomical or satellite operations.
"""

SFO_schema = '''{
  "title": "ScheduleFillerObjective",
  "type": "object",
  "sensor_name": { "type": "string" },
  "data_mode": { "type": "string" },
  "classification_marking": { "type": "string", "default": "U" },
  "scheduling_density": { "type": "number", "default": 15.0 },
  "hours_to_plan": { "type": "integer", "default": 24 },
  "objective_name": { "type": "string", "default": "Schedule Filler Objective" },
  "objective_start_time": { "type": "string", "format": "date-time" },
  "objective_end_time": { "type": "string", "format": "date-time" },
  "priority": { "type": "integer", "default": 10 },
  "required": ["sensor_name", "data_mode", "classification_marking"]
}
'''

SFO_data = {
  "title": "ScheduleFillerObjective",
  "type": "object",
  "sensor_name": { "type": "string" },
  "data_mode": { "type": "string" },
  "classification_marking": { "type": "string", "default": "U" },
  "scheduling_density": { "type": "number", "default": 15.0 },
  "hours_to_plan": { "type": "integer", "default": 24 },
  "objective_name": { "type": "string", "default": "Schedule Filler Objective" },
  "objective_start_time": { "type": "string", "format": "date-time" },
  "objective_end_time": { "type": "string", "format": "date-time" },
  "priority": { "type": "integer", "default": 10 },
  "required": ["sensor_name", "data_mode", "classification_marking"]
}

SFO_required = "sensor_name, data_mode, classification_marking"

SFO_default = """{
  scheduling_density: 15.0,
  hours_to_plan: 24,
  objective_name: "New Schedule Filler Objective",
  objective_start_time: "",
  objective_end_time: "",
  priority: 10,
}
"""

SFO_example_1 = '''{
  "objective_def_name": "ScheduleFillerObjective",
  "objective_name": "Schedule Filler Objective",
  "sensor_name": "RME95",
  "objective_start_time": "2023-08-21T18:47:19.059212",
  "scheduling_density": 30.0,
  "data_mode": "TEST",
  "classification_marking": "U"
  }
'''

SFO_examples = [SFO_example_1]

## Quality Window Objective

QWO_description_prev = """The QualityWindowObjective class is central to modeling and 
working with quality objectives in a satellite or space object tracking system. 
The QualityObjectiveObject class encompasses the parameters and mechanisms (using 
an Unscented Kalman Filter) for a particular quality objective, likely aimed at 
non-linear state estimation in observing space objects. On the other hand, the 
QualityWindowObjective class is geared towards orchestrating these objectives, 
handling the specifics of sensors, payloads, scheduling, and logging, and could be 
used as a part of a larger scheduling or mission planning system.
"""

QWO_description = """The QualityWindowObjective class is useful for modeling and working with quality objectives in a 
satellite or space object tracking system. The QualityObjectiveObject class encompasses the parameters and mechanisms (using an Unscented Kalman Filter) for a particular quality objective, aimed at non-linear state estimation in observing space objects. Quality window is geared towards orchestrating these objectives, handling the specifics of sensors, payloads, scheduling, and logging. Window is useful for more complex scheduling or mission planning systems.
"""

QWO_schema = '''{
  "title": "QualityWindowObjective",
  "type": "object",
  "sensor_name": { "type": "string" },
  "payload_list": { "type": "string" },
  "data_mode": { "type": "string", "default": "REAL" },
  "classification_marking": { "type": "string", "default": "U" },
  "scheduling_density": { "type": "number", "default": 5 },
  "hours_to_plan": { "type": "integer", "default": 24 },
  "objective_name": { "type": "string", "default": "Quality Window Objective" },
  "objective_start_time": { "type": "string", "format": "date-time" },
  "objective_end_time": { "type": "string", "format": "date-time" },
  "priority": { "type": "integer", "default": 1 },
  "required": ["sensor_name", "payload_list", "data_mode", "classification_marking"]
}
'''

QWO_data = {
  "title": "QualityWindowObjective",
  "type": "object",
  "sensor_name": { "type": "string" },
  "payload_list": { "type": "string" },
  "data_mode": { "type": "string", "default": "REAL" },
  "classification_marking": { "type": "string", "default": "U" },
  "scheduling_density": { "type": "number", "default": 5 },
  "hours_to_plan": { "type": "integer", "default": 24 },
  "objective_name": { "type": "string", "default": "Quality Window Objective" },
  "objective_start_time": { "type": "string", "format": "date-time" },
  "objective_end_time": { "type": "string", "format": "date-time" },
  "priority": { "type": "integer", "default": 1 },
  "required": ["sensor_name", "payload_list", "data_mode", "classification_marking"]
}

QWO_required = "sensor_name, payload_list, data_mode, classification_marking"

QWO_default = """{
  data_mode: "REAL",
  classification_marking: "U",
  scheduling_density: 5.0,
  hours_to_plan: 24,
  objective_name: "Quality Window Objective",
  objective_start_time: "",
  objective_end_time: "",
  priority: 1,
}
"""

QWO_example_1 = '''{
        "sensor_name": "RME37",
        "objective_start_time": "2023-07-04T00:00:00.000Z",
        "payload_list": [
            {
                "satNo": 28884,
                "priority": 2,
                "state_vector": {
                    "timestamp": "2023-07-04T00:00:00.000Z",
                    "x_kilometers": 3.43988467e04,
                    "y_kilometers": -2.51038896e04,
                    "z_kilometers": -5.14207398e02,
                    "x_dot_kilometers_per_second": 1.8,
                    "y_dot_kilometers_per_second": 2.46858629,
                    "z_dot_kilometers_per_second": -2.07930829e-02
                    },
                "window_start": "2023-07-04T22:00:00.000Z",
                "window_end": "2023-07-04T23:00:00.000Z",
                "position_accuracy": 1.0,
                "velocity_accuracy": 5
            }
        ],
        "data_mode": "TEST",
        "classification_marking": "U",
        "scheduling_density": 5.0,
        "hours_to_plan": 24,
        "objective_name": "Quality Window Objective",
        "objective_start_time": "2023-07-04T00:00:00.000Z",
        "objective_end_time": "2023-07-04T00:00:00.000Z",
        "priority": 1
}'''

QWO_examples = [QWO_example_1]
