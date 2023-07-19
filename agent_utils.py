import re

def get_agent_thoughts(input_data):
    """
    Extract the thoughts or actions of an agent from a given text string.

    This function uses regular expressions to find and return all matches 
    of a specific pattern in the text. The pattern is designed to capture 
    sentences that begin with "I need to" or "I now have". It then strips 
    unwanted escape characters (newline and backslashes).

    Inputs:
        input_data (str): A string from which to extract the agent's thoughts/actions.
        Can also be a List[str]

    Outputs:
        List[str]: A list of strings, each string being a thought or action 
        expressed by the agent in the input text.
    """

    text = ""
    
    # Check if the input_data is a list
    if isinstance(input_data, list):
        # If it's a list, join all the strings in the list
        for item in input_data:
            if isinstance(item, str):
                text += item
    elif isinstance(input_data, str):
        # If it's a string, just assign it to the text
        text = input_data
    else:
        raise ValueError("Input must be either a string or a list of strings.")
    
    text = text.replace('\\\\n', ' ').replace('\\\\', '')
    pattern = r"(I need to.*?|I now have.*?)(?=Thought:|$)"
    matches = re.findall(pattern, text, re.DOTALL)
    return [match.strip() for match in matches]