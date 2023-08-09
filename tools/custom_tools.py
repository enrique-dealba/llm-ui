from langchain.agents import Tool
from langchain.tools import BaseTool

def ask_user(input: str = ""):
    return "Please provide more information."

ask_user_tool = Tool(
    name="Final Answer",
    func=ask_user,
    description="Useful for when you need to ask the user for more information.",
    )
