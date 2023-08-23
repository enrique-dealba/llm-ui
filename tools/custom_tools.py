from langchain.agents import Tool
from langchain.tools import BaseTool

def ask_user(input: str = ""):
    return "Please provide more information."

ask_user_tool = Tool(
    name="Final Answer",
    func=ask_user,
    description="Useful for when you need to ask the user for more information.",
    )

def get_current_time(*args, **kwargs):
    import subprocess

    result = subprocess.run(['date', '-u', '+%Y-%m-%dT%H:%M:%SZ'], stdout=subprocess.PIPE)
    current_time = result.stdout.decode('utf-8').strip()
    print(current_time)
    return current_time

get_current_time_tool = Tool(
    name="get_current_time",
    func=get_current_time,
    description = (
        "Use this tool to get the current time."
        "Useful when you need to fill in JSON fields like:"
        "start_time, objective_start_time."
        ),
    )
