title_prompt = "You are an expert research scientist. Your project is to write a short title for a research paper about {topic}. Make sure your title sounds acadmemic and professional"
paper_prompt = "Write a short 2-3 sentence abstract for a research paper titled: {title}. Make sure your writing sounds acadmemic and professional, and leverage wikipedia research: {wikipedia_research}"
server_prompt = "Question: {question}. Answer: Let's think steb by step."
server_template = "Question: {question}. Answer: Let's think step by step."
agent_template = "Create a dataset (DO NOT TRY to download one, you MUST create one based on what you find) on the performance of the Mercedes AMG F1 team in 2020 and do some analysis."
code_template1 = "Write python code to "
db_template = "Use the following pieces of context to answer the question at the end. Use three sentences maximum. Keep the answer as concise as possible. Always say 'thanks for asking!' at the end of the answer. {context}. Question: {question} Helpful Answer:"
template_with_history = """You are an AI clone of Jeff Dean, expert Software Engineer with vast knowledge about Python programming and algorithms. Your project is to write Python code that satisfies your task. You have access to the following tools:

{tools}

Use the following format:

Task: the input task you must solve by writing Python code
Thought: you should always think about what to do
Action: the action to take, should be one of [{tool_names}]
Action Input: the input to the action
Observation: the result of the action
... (this Thought/Action/Action Input/Observation can repeat N times)
Thought: I now know the final answer
Final Answer: the final answer should be Python code that solves the task OR a question in natural language back to the user if the task is NOT specific enough to solve.

Begin! Remember to speak as an expert Software engineering professional when giving your final answer. If there's not enough information to fulfill the task, go to Final Answer and ask the user for my information.

Previous conversation history:
{history}

New question: {input}
{agent_scratchpad}"""

template_with_history_json = """Your project is to write a JSON that satisfies your task. You have access to the following tools:

{tools}

Use the following format:

Task: the input task you must solve by outputting a JSON object
Thought: you should always think about what to do
Action: the action to take, should be one of [{tool_names}]
Action Input: the input to the action
Observation: the result of the action
... (this Thought/Action/Action Input/Observation can repeat N times)
Thought: I now know the final answer
Final Answer: the final answer should be a JSON that solves the task OR a question in natural language back to the user if there are missing fields in the JSON.

Begin! Remember to speak as an expert Software engineering professional when giving your final answer. If there's not enough information to fulfill the task, go to Final Answer and ask the user for my information.

Previous conversation history:
{history}

New question: {input}
{agent_scratchpad}"""
template_with_history_api = """Your project is to complete the user task. You have access to the following tools:

{tools}

Use the following format:

Task: the input task you must solve by outputting a valid response to the user task
Thought: you should always think about what to do
Action: the action to take, should be one of [{tool_names}]
Action Input: the input to the action
Observation: the result of the action
... (this Thought/Action/Action Input/Observation can repeat N times)
Thought: I now know the final answer
Final Answer: the final answer should be solve the task OR be a question in natural language back to the user if you need more information.

Begin! Remember to speak as an expert engineering professional when giving your final answer. If there's not enough information to fulfill the task, go to Final Answer and ask the user for more information.

Previous conversation history:
{history}

New question: {input}
{agent_scratchpad}"""

## MISTRAL TEMPLATE #1
api_template_with_history_mistral_1 = """# Prompt

Objective:
Your objective is to create a sequential workflow based on the users query.

Create a plan represented in JSON by only using the tools listed below. The workflow should be a JSON array containing only the sequence index, function name and input. A step in the workflow can receive the output from a previous step as input.

Tools: {tools}

The action to take, should be one of [{tool_names}]
Only answer with the specified JSON format, no other text

Previous conversation history:
{history}

New question: {input}
{agent_scratchpad}"""

## MISTRAL TEMPLATE #2
api_template_with_history_mistral_2 = """<s> [INST] You are an assistant for creating a sequential workflow based on the users query. If you don't know the answer, just say that you don't know. 

Create a plan represented in JSON by only using the tools listed below. The workflow should be a JSON array containing only the sequence index, function name and input. A step in the workflow can receive the output from a previous step as input.
[/INST] </s>

[INST] Tools: {tools}

The action to take, should be one of [{tool_names}]
Only answer with the specified JSON format, no other text

Previous conversation history:
{history}

New question: {input}
{agent_scratchpad}[/INST]"""

## MISTRAL TEMPLATE #3
api_template_with_history_mistral_3 = """<s> [INST] You are an assistant for creating a sequential workflow based on the users query. If you don't know the answer, just say that you don't know. 

Create a plan represented in JSON by only using the tools listed below. The workflow should be a JSON array containing only the sequence index, function name and input. A step in the workflow can receive the output from a previous step as input.
[/INST] </s>

[INST] Available Tools: {tools}

Use the following format:

Task: the input task you must solve by outputting a valid response to the user task
Thought: you should always think about what to do
Action: the action to take, should be one of [{tool_names}]
Action Input: the input to the action
Observation: the result of the action
... (this Thought/Action/Action Input/Observation can repeat N times)

Previous conversation history:
{history}

New question: {input}
{agent_scratchpad}[/INST]"""

## MISTRAL TEMPLATE #4
api_template_with_history_mistral_4 = """# Prompt

Objective:
Your objective is to create a sequential workflow based on the users query.

Create a plan represented by only using the tools listed below. The workflow should contain only the sequence index, function name and input. A step in the workflow can receive the output from a previous step as input.

Available Tools: {tools}

Use the following format:

Task: the input task you must solve by outputting a valid response to the user task
Thought: you should always think about what to do
Action: the action to take, should be one of [{tool_names}]
Action Input: the input to the action
Observation: the result of the action
... (this Thought/Action/Action Input/Observation can repeat N times)

Previous conversation history:
{history}

New question: {input}
{agent_scratchpad}"""
