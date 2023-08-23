import argparse
import sys

sys.path.append('/Users/edealba/Documents/GitHub/llm-ui')
from objective_utils import get_objective, get_embedding_fn

SFO_list = [
    ("Create a new schedule filler for sensor RME50 with a scheduling density of 15 minutes, "
     "'U' markings, and priority of 5"
    ),
    "I want a schedule filler for the next 48 hours for sensor RME70, with data mode 'TEST' and priority of 8",
    "Generate a Schedule Filler for sensor RME56, with a scheduling density of 30 minutes, priority of 7, and  name it 'Critical Test'",
    ("Create an objective for sensor RME98, with data mode 'TEST', classification marking 'U', scheduling "
     "density of 20 mins and plan for the next 36 hours"
    ),
    "Design a Schedule Filler for the next 72 hours for sensor RME12, using 'TEST' data mode, 'U' markings, and priority of 4"
]

QWO_list = [
    ("Start a quality window for sensor RME23 in TEST mode for the next 12 hours, with a priority "
     "of 2, and a scheduling density of 5.0"
    ),
    "Schedule a 36-hour quality window using sensor RME89, operating in TEST mode, with a high priority of 5 and classification marking of 'U'",
    "Initiate a Quality Window Objective with sensor RME56, planning for 48 hours, using TEST mode, and commencing 8 hours later",
    "Configure a new quality window for sensor RME21 in TEST mode, lasting 24 hours, incorporating specific payloads, and ending 8 hours later",
    "Prepare a quality window with sensor RME54, scheduling density of 3.0, objective to begin in 15 hours from now, in TEST mode, with classification marking 'U'"
]

SO_list = [
    ("Create a search objective for target ID 56789 using sensor RME01, with an initial offset of "
     "100 seconds, 35 percent frame overlap, and ending in 20 mins"
    ),
    "I want a new search for target 76117 with sensor RME07 with 30 percent frame overlap",
    "Schedule a search for target 32101 with sensor RME02 with 70 percent frame overlap, and a classification marking of 'U'",
    "Make a new search for target 87654 using sensor RME03 with data mode 'TEST' and a priority of 2, ending in 15 minutes",
    "Set up a search objective for target 11223 using sensor RME04 that starts at a specific time, with integration time of 100 seconds, and .60 frame overlap"
]

CMO_list = [
    ("I want to make a new catalog maintenance for sensor RME01 with default priority, 'U' marking, "
     "and TEST data mode"
    ),
    "Set up catalog maintenance using sensor RME02 with a priority level of 5 and a 'U' classification marking, utilizing TEST data mode"
    "Schedule catalog maintenance on sensor RME12, with a 60-minute patience window, starting now",
    "Create a new catalog maintenance objective for sensor RME01 with an end time offset of 15 minutes and priority 8, using 'U' marking and TEST data mode",
    "Make a catalog maintenance task for sensor RME03 with a start time now, an end time in 5 hrs, and a 'U' classification marking."
]

PRO_list = [
    "Track object 12345 with sensor RME08, revisiting twice per hour for the next 16 hours, starting now",
    "Observe satellite 67890 using sensor RME01, once per hour for a total of 12 hours, with priority 3",
    "Monitor target 54321 through sensor RME52, visiting three times per hour, starting at 2023-12-01 12:00:00 and ending 8 hours later, with a priority of 1",
    "Observe target 33333 using sensor RME72, once per hour, for a 6-hour plan, starting at 2023-12-20 00:08:00, with a classification marking of 'U'"
]

JSON_EVALS = {
    "ScheduleFillerObjective": SFO_list,
    "QualityWindowObjective": QWO_list,
    "SearchObjective": SO_list,
    "CatalogMaintenanceObjective": CMO_list,
    "PeriodicRevisitObjective": PRO_list,
}

def create_parser() -> argparse.ArgumentParser:
    """Creates a command-line argument parser."""
    parser = argparse.ArgumentParser(description="Run json-agent evals")
	# Usage: `--llm local` or `--llm davinci` etc
    parser.add_argument('--llm', choices=['local', 'chatgpt', 'davinci'], help='Choose an LLM for json-agent evals')
    return parser

if __name__ == "__main__":
    parser = create_parser()
    args = parser.parse_args()
    """
    RESULTS:
    thenlper/gte-small: 19 / 23 -- 0.83%
    thenlper/gte-base: 16 / 23 -- 0.70%
    BAAI/bge-base-en: 14 / 23 -- 0.61%
    BAAI/bge-small-en: 17 / 23 -- 0.74%
    intfloat/e5-small-v2: 17 / 23 -- 0.74%
    sentence-transformers/all-MiniLM-L6-v2: 19 / 23 -- 0.83%
    """
    model_name = 'sentence-transformers/all-MiniLM-L6-v2'
    embedding_fn = get_embedding_fn(model_name=model_name)
    ## JSON-agent testing
    score = 0
    total = 0
    cumulative_confidence = 0.0
    logger = {"Correct": [],
            "Incorrect": []}
    for obj, task_list in JSON_EVALS.items():
        for task in task_list:
            objective, confidence = get_objective(task, embedding_fn=embedding_fn)
            cumulative_confidence += confidence
            valid = bool(str(objective.name) == str(obj))
            if valid:
                logger["Correct"].append(f"{obj}: {task} -- Extracted: {objective.name}")
                score += 1
            else:
                logger["Incorrect"].append(f"{obj}: {task} -- Extracted: {objective.name}")
            total += 1
    print("="*40)
    print(f"OBJ DEF EXTRACTION EVAL: {model_name}: {score} / {total} -- {float(score/total):.2f}%")
    print(f"CUMULATIVE CONFIDENCE: {cumulative_confidence}")
    print(logger)
