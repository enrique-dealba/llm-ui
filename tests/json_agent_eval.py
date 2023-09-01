import argparse
import sys

sys.path.append('/Users/edealba/Documents/GitHub/llm-ui')
from agent_logic import AgentServer

SFO_list = [
    ("Create a new schedule filler for sensor RME50 with a scheduling density of 15 minutes, "
     "'U' markings, and priority of 5"
    ),
    "I want a schedule filler for the next 48 hours for sensor RME70, with data mode 'TEST' and priority of 8",
    "Generate a Schedule Filler for sensor RME56, with a scheduling density of 30 minutes, priority of 7, and name it “CriticalTest”. Also want TEST mode and C markings"
]

# QWO_list = [
#     "Configure a new quality window for sensor RME21 in TEST mode, lasting 24 hours, incorporating specific payloads, and ending 8 hours later",
#     "Set up a quality window objective with sensor RME52, in TEST mode, priority 4 lasting for 30 hours",
# ]

SO_list = [
    "Create a search objective for target ID 56789 using sensor RME01, with an initial offset of 100 seconds, 0.35 frame overlap, and ending in 20 mins",
    "Make a new search for target 87654 using sensor RME03 with data mode 'TEST' and a priority of 2, ending in 15 minutes",
    "Set up a search for target 28884 using sensor RME04 with integration time of 100 seconds, and .60 frame overlap"
]

CMO_list = [
    ("I want to make a new catalog maintenance for sensor RME01 with default priority, 'U' marking, "
     "and TEST data mode"
    ),
    "Create a new catalog maintenance objective for sensor RME01 with an end time offset of 15 minutes and priority 8, using 'U' marking and TEST data mode",
    "Schedule a catalog maintenance on sensor RME12, with a 60 min patience window on REAL mode",
]

PRO_list = [
    "Track object 12345 with sensor RME08, revisiting twice per hour for the next 16 hours, starting now",
    "Observe satellite 67890 using sensor RME01, once per hour for a total of 12 hours, with priority 3",
    "Make a periodic revisit for target 33333 using sensor RME72, once per hour, for a 6-hour plan, starting at 2023-12-20 00:08:00, with a marking of 'TS' and TEST mode"
]

JSON_EVALS = {
    "ScheduleFillerObjective": SFO_list,
    # "QualityWindowObjective": QWO_list,
    "SearchObjective": SO_list,
    "CatalogMaintenanceObjective": CMO_list,
    "PeriodicRevisitObjective": PRO_list,
}

def create_parser() -> argparse.ArgumentParser:
    """Creates a command-line argument parser."""
    parser = argparse.ArgumentParser(description="Run json-agent evals")
	# Usage: `--llm local` or `--llm davinci` etc
    parser.add_argument('--llm', choices=['local', 'chatgpt', 'davinci', 'custom_gpt', 'gpt4'], help='Choose an LLM for json-agent evals')
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
