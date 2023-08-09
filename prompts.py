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
