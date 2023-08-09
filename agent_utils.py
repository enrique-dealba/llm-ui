from collections import OrderedDict
import ast
import itertools
import os
import re
import traceback

from typing import List, Dict, Any, Optional, Union

def get_agent_thoughts(input_data):
    """
    Extract the thoughts or actions of an agent from a given text string.

    This function uses regular expressions to find and return all matches 
    of a specific pattern in the text. The pattern is designed to capture 
    sentences that begin with "I need to" or "I now have". It then strips 
    unwanted escape characters (newline and backslashes).

    [Inputs]
        input_data (str): A string from which to extract the agent's thoughts/actions.
        Can also be a List[str]

    [Outputs]
        List[str]: A list of strings, each string being a thought or action 
        expressed by the agent in the input text.

    Example:
        text = "I need to find information on the performance.\\\\nI now have a dataset."
        get_agent_thoughts(text)
        ['I need to find information on the performance.', 'I now have a dataset.']
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

def execute_code(code: str, debug=False):
    """
    Execute Python code in a specific execution environment.
    
    [Inputs]
        Python code to execute

    [Outputs]
        execution environment if code executed successfully, None otherwise
    """
    exec_env = {}
    try:
        exec(code, exec_env)
        return exec_env
    except Exception as e:
        if debug:
            print(f"CODE ERROR - FAILED TO EXECUTE: {code}")
            print(f"An error occurred while executing the Python code:\n{traceback.format_exc()}")
        return None

def save_code_to_file(code: str, filename: str, dir_name: str = 'agent_dir'):
    if not code.strip():
        print("CODE ERROR - EMPTY CODE: No code to save.")
        return
    
    # Tries to execute the entire code. If it fails, it's likely due to a function 
    # call being made before the function is defined.
    exec_env = execute_code(code)
    if exec_env is None:
        # Splits the code into blocks by blank lines
        code_blocks = list(filter(bool, code.split("\n\n")))
        for i, block in enumerate(code_blocks):
            # Attempts to execute each block. If a block fails, it's likely a 
            # function call dependent on a prior definition.
            exec_env = execute_code("\n\n".join(block[:i+1]))
            if exec_env is None:
                return
            
    print("SUCCESS - Saving code!")
    os.makedirs(dir_name, exist_ok=True)
    file_path = os.path.join(dir_name, f"{filename}.py")

    with open(file_path, 'w') as file:
        file.write(code)

def count_and_replace_spaces(code_str: str) -> str:
    def replacer(match):
        return f'[SPACE:{len(match.group())}]'
    if not code_str: return
    processed_str = re.sub(r' {2,}', replacer, code_str)
    return processed_str

def space_to_newlines_map_2(text):
    """
    This function processes a specially formatted string to extract unique 
    numbers associated with specific space placeholders, sorts them, and maps 
    them to specific strings.
    
    [Inputs]
        input_string (str): A string containing space placeholders in the format:
        [SPACE:NUM]
      
    [Outputs]
        dict: A dictionary mapping each number to a specific string. For each 
        number in the sorted list (excluding the last number), it maps to a 
        string consisting of a newline character followed by a number of spaces 
        equal to 4 times its position index in the sorted list. The last number 
        in the list maps to an empty string.
    """
    # Extracts space values
    space_values = re.findall(r'\[SPACE:(\d+)\]', text)
    space_values = [int(value) for value in space_values]

    # Removes duplicates and sort in ascending order
    space_values = sorted(list(set(space_values)))

    # Generates num spaces to newline + indents mapping
    mapping = {}
    NUM_VALUES = len(space_values)
    for i, value in enumerate(space_values):
        if i < NUM_VALUES - 1:
            num_spaces = 4 * i
            mapping[value] = "\n" + " " * num_spaces
        else:
            mapping[value] = ""

    return mapping

def standard_indents(space_list):
    for num_spaces in space_list:
        if num_spaces % 2 != 0:
            return False
    return True

def off_by_one(space_list):
    for num_spaces in space_list:
        if (num_spaces-1) % 2 != 0:
            return False
    return True

def space_to_newlines_map(text):
    """
    This function processes a specially formatted string to extract unique 
    numbers associated with specific space placeholders, sorts them, and maps 
    them to specific strings.
    
    [Inputs]
      input_string (str): A string containing space placeholders in the format:
      [SPACE:NUM]
      
    [Outputs]
      dict: A dictionary mapping each number to a specific string. For each 
      number in the sorted list (excluding the last number), it maps to a 
      string consisting of a newline character followed by a number of spaces 
      equal to 4 times its position index in the sorted list. The last number 
      in the list maps to an empty string.
    """
    # Extracts space values
    space_values = re.findall(r'\[SPACE:(\d+)\]', text)
    space_values = [int(value) for value in space_values]

    # Removes duplicates and sort in ascending order
    space_values = sorted(list(set(space_values)))

    if standard_indents(space_values):
      mapping = {}
      NUM_VALUES = len(space_values)
      for i, value in enumerate(space_values):
          num_spaces = 4 * i
          mapping[value] = "\n" + " " * num_spaces
    elif off_by_one(space_values):
        # Also assumes the starting def line has no spaces!
        mapping = {}
        NUM_VALUES = len(space_values)
        for i, value in enumerate(space_values):
            num_spaces = 4 * (i+1)
            mapping[value] = "\n" + " " * num_spaces
    else:
      # Generates num spaces to newline + indents mapping
      mapping = {}
      NUM_VALUES = len(space_values)
      for i, value in enumerate(space_values):
          if i < NUM_VALUES - 1:
              num_spaces = 4 * i
              mapping[value] = "\n" + " " * num_spaces
          else:
              mapping[value] = ""

    return mapping

def replace_spaces(text, mapping):
    """
    Replaces placeholders with the corresponding strings from the mapping 
    using regex.
    """
    for k, v in mapping.items():
        text = re.sub(f'\[SPACE:{k}\]', v, text)
    return text

def process_code_line(code_txt) -> str:
    space_count_txt = count_and_replace_spaces(code_txt)
    if not space_count_txt: return ""
    # print(f"space_count_txt: {space_count_txt}")
    space_newline_mapping = space_to_newlines_map(space_count_txt)
    new_txt = replace_spaces(space_count_txt, space_newline_mapping)
    return new_txt

def code_equivalence(str1: str, str2: str) -> bool:
    """
    Removes all extra whitespaces to check string equivalence.
    """
    str1 = re.sub(r'\s+', ' ', str1.strip())
    str2 = re.sub(r'\s+', ' ', str2.strip())
    return str1 == str2

def execute_and_test_code(code_blocks: OrderedDict):
    code_block = '\n'.join(code_blocks.keys())
    code_text = process_code_line(code_block)
    exec_env = execute_code(code_text)
    return exec_env is not None

def find_valid_blocks_prev(code_blocks: OrderedDict, debug=False):
    # First, try the original order
    if execute_and_test_code(code_blocks):
        return code_blocks
    
    # If original order doesn't work then check all permutations
    for block in itertools.permutations(code_blocks.keys()):
        new_blocks = OrderedDict((line, None) for line in block)
        if new_blocks == code_blocks:  # Skips original
            continue
        if execute_and_test_code(new_blocks):
            return new_blocks
    if debug:
        print("ERROR - No valid sequence of code blocks found.")
    return None

def get_one_off_blocks(cb: OrderedDict, b_to_remove):
    return OrderedDict((k, v) for k, v in cb.items() if k != b_to_remove)

def one_off_permutations(code_blocks: OrderedDict, debug=False):
    # Trying permutations with one code block removed
    for block_to_remove in code_blocks.keys():
        reduced_blocks = get_one_off_blocks(code_blocks, block_to_remove)
        for block in itertools.permutations(reduced_blocks.keys()):
            new_blocks = OrderedDict((x, reduced_blocks[x]) for x in block)
            if execute_and_test_code(new_blocks):
                if debug:
                    print(f"Found valid permutation w/o block: {block_to_remove}")
                return new_blocks
    return None

def find_valid_blocks(code_blocks: OrderedDict, debug=False):
    # First, try the original order
    if execute_and_test_code(code_blocks):
        return code_blocks
    
    # If original order doesn't work then check all permutations
    for block in itertools.permutations(code_blocks.keys()):
        new_blocks = OrderedDict((line, None) for line in block)
        if new_blocks == code_blocks:  # Skips original
            continue
        if execute_and_test_code(new_blocks):
            return new_blocks
        
    # If full Perms don't work - try Perms with one code block removed
    one_off_blocks = one_off_permutations(code_blocks, debug=debug)
    if one_off_blocks is not None:
        return one_off_blocks
    
    if debug:
        print("ERROR - No valid sequence of code blocks found.")
    return None

def get_valid_code_prev(code_blocks: OrderedDict):
    try:
        blocks = find_valid_blocks_prev(code_blocks)
        code_block = '\n'.join(blocks.keys())
    except AttributeError:
        code_block = '\n'.join(code_blocks.keys())
    return code_block

def get_valid_code(code_blocks: OrderedDict):
    try:
        blocks = find_valid_blocks(code_blocks, debug=True)
        code_block = '\n'.join(blocks.keys())
    except AttributeError:
        code_block = '\n'.join(code_blocks.keys())
    return code_block

def try_agent_outputs(try_output: str, code_block: str, code_blocks: OrderedDict):
    """
    Useful when Agent outputs code in its final answer.
    """
    if try_output is not None:
        code_blocks[try_output] = None
        new_block = get_valid_code(code_blocks)
        if len(new_block) > len(code_block):
            return new_block
    return code_block

def extract_function_name(input_str: str) -> str:
    match = re.search(r'def (\w+)\(', input_str)
    if match:
        return match.group(1)
    else:
        return "No explicit function name found."

def python_to_text(file_path: str) -> str:    
    if os.path.exists(file_path) and os.path.isfile(file_path):
        with open(file_path, 'r') as file:
            content = file.read()
            return str(content)
    elif os.path.exists(file_path):
        raise IsADirectoryError(f"A directory with the same name as the file exists: {file_path}")
    else:
        raise FileNotFoundError(f"The file does not exist: {file_path}")

def extract_code_from_response(response: list, try_output = None) -> str:
    response_str = "\n".join(response)

    code_blocks = OrderedDict()
    inside_code_block = False
    code = ""

    for line in response_str.split("\n"):
        # Check for multi-line code block
        if "Action: Python_REPL" in line or "Action Input:" in line:
            inside_code_block = True
            if "Action Input:" in line:
                code += line.split("Action Input:", 1)[1].strip() + "\n"
        elif "Observation:" in line and inside_code_block:
            inside_code_block = False
            if code:
                code_blocks[code] = None
                code += "\n"  # add newline to the end of each code block
                # print(f'Adding code block (length {len(code)}): {code}')  # debugging print
                code = ""
        elif inside_code_block and line.strip():
            code += line + "\n"

        # Check for single-line code block
        match = re.search(r"Action Input:\s*(.*?)\s*Observation:", line)
        if match:
            code = match.group(1)
            if code:
                code_blocks[code] = None

    code_block = get_valid_code_prev(code_blocks)
    if try_output is not None:
        code_block = try_agent_outputs(try_output, code_block, code_blocks)

    # print(f'Complete code block (length {len(code_block)}): {code_block}')  # debugging print
    # print(f"Total number of code blocks: {len(code_blocks)}")

    code_text = process_code_line(code_block)

    return code_text

def remove_code_markers(code_text: str) -> str:
    code_text = code_text.replace("```python\n", "")
    code_text = code_text.replace("```", "")
    agent_stop_text = "Agent stopped due to iteration limit or time limit."
    code_text = code_text.replace(agent_stop_text, "")
    return code_text

def remove_markers_from_blocks(code_blocks: OrderedDict):
    new_blocks = OrderedDict()
    for k, v in code_blocks.items():
        clean_code = remove_code_markers(k)
        new_blocks[clean_code] = None
    return new_blocks

def extract_code_from_response_convo(response: list, try_output = None) -> str:
    response_str = "\n".join(response)

    code_blocks = OrderedDict()
    inside_code_block = False
    code = ""

    for line in response_str.split("\n"):
        # Check for multi-line code block
        if "Action: Python_REPL" in line or "Action Input:" in line:
            inside_code_block = True
            if "Action Input:" in line:
                code += line.split("Action Input:", 1)[1].strip() + "\n"
        elif "Observation:" in line and inside_code_block:
            inside_code_block = False
            if code:
                code_blocks[code] = None
                code += "\n"  # add newline to the end of each code block
                code = ""
        elif inside_code_block and line.strip():
            code += line + "\n"

        # Check for single-line code block
        match = re.search(r"Action Input:\s*(.*?)\s*Observation:", line)
        if match:
            code = match.group(1)
            if code:
                code_blocks[code] = None
                
    code_blocks = remove_markers_from_blocks(code_blocks)
    code_block = get_valid_code(code_blocks)
    if try_output is not None:
        code_block = try_agent_outputs(try_output, code_block, code_blocks)

    code_text = process_code_line(code_block)
    # code_text = remove_code_markers(code_text)

    return code_text