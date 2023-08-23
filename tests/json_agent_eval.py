import argparse
import sys

sys.path.append('/Users/edealba/Documents/GitHub/llm-ui')
from agent_logic import AgentServer

SFO_list = [
    ("Create a new schedule filler for sensor RME50 with a scheduling density of 15 minutes, "
     "'U' markings, and priority of 5"
    ),
]

QWO_list = [
    ("Start a quality window for sensor RME23 in TEST mode for the next 12 hours, with a priority "
     "of 2, and a scheduling density of 5.0"
    ),
]

SO_list = [
    ("Create a search objective for target ID 56789 using sensor RME01, with an initial offset of "
     "100 seconds, 35 percent frame overlap, and ending in 20 mins"
    ),
]

CMO_list = [
    ("I want to make a new catalog maintenance for sensor RME01 with default priority, 'U' marking, "
     "and TEST data mode"
    ),
]

PRO_list = [
    "Track object 12345 with sensor RME08, revisiting twice per hour for the next 16 hours, starting now",
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
    server = AgentServer(llm_mode=args.llm, agent_mode='json-agent', template="")
    ## JSON-agent testing
    score = 0
    total = 0
    logger = {"Correct": [],
            "Incorrect": []}
    for obj, task_list in JSON_EVALS.items():
        for task in task_list:
            response, valid = server.test_json(task)
            if valid:
                logger["Correct"].append(f"{obj}: {task} -- Agent response: {response}")
                score += 1
            else:
                logger["Incorrect"].append(f"{obj}: {task} -- Agent response: {response}")
            total += 1
    print("="*40)
    print(f"JSON AGENT EVAL: {score} / {total}")
    print(logger)
