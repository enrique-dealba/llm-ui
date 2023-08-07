import argparse
import config
import logging
import os
import random

from typing import List, Dict, Any, Optional, Union
from apikeys import open_ai_key, hf_key, serpapi_key
from prompts import server_template, agent_template #, db_template
from agent_utils import get_agent_thoughts, extract_code_from_response
from test_files.responses import responses_1, responses_2, code_1, code_2, code_3, code_4

from agent_utils import save_code_to_file, code_equivalence

from flask import Flask, request, jsonify, render_template
from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline
from langchain import PromptTemplate, LLMChain
from langchain.chains import RetrievalQA, ConversationalRetrievalChain
from langchain.llms import OpenAI, HuggingFacePipeline
from langchain.embeddings import HuggingFaceInstructEmbeddings
from langchain.document_loaders import TextLoader
from langchain.memory import ConversationBufferMemory
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import Chroma
from InstructorEmbedding import INSTRUCTOR

## AGENT IMPORTS ##
from langchain.agents import load_tools, initialize_agent
from langchain.agents import (
    AgentType,
)  # We will be using the type: ZERO_SHOT_REACT_DESCRIPTION which is standard

os.environ['OPENAI_API_KEY'] = open_ai_key
os.environ['HUGGINGFACEHUB_API_TOKEN'] = hf_key
os.environ['SERPAPI_API_KEY'] = serpapi_key

app = Flask(__name__)

logging.basicConfig(level=logging.DEBUG)

class ListHandler(logging.Handler): # Inherits from logging.Handler
    def __init__(self):
        super().__init__()
        self.log = []

    def emit(self, record) -> None:
        """Keeps track of verbose outputs from agent LLM in logs."""
        self.log.append(self.format(record))

handler = ListHandler()
logging.getLogger().addHandler(handler)

class AgentServer:
    """LLM Agent Flask server with Agent operations."""

    def __init__(self, use_local: bool=True, template: str="", init_model: bool=True):
        self.app = app 
        self.tokenizer = None
        self.model = None
        self.llm = None
        self.embedding = None
        self.memory = None
        self.qa_chain = None
        self.tools = None
        self.agent = None
        self.template = template
        self.persist_directory = 'docs/chroma/'
        if init_model:
            self.initialize_model(use_local)

    def set_tools(self, use_default_tools: bool):
        """Setup of tools for agent LLM."""
        assert self.llm is not None

        if use_default_tools:
            self.tools = load_tools(["wikipedia",
                                     "serpapi",
                                     "python_repl",
                                     "terminal"],
                                     llm=self.llm)
            
    def init_agent(self):
        """Initializes LLM agent."""
        if self.tools is None:
            self.set_tools(use_default_tools=True)
        
        self.agent = initialize_agent(
            tools=self.tools,
            llm=self.llm,
            agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
            verbose=True)
        
        if self.tools is None or self.agent is None:
            return jsonify({'error': 'Agent or tools not initialized'}), 400

    def initialize_model(self, use_local: bool=True):
        """Initialize LLM either locally or from OpenAI (text-davinci-003)."""
        if use_local:
            directory_path = config.MODEL_DIRECTORY_PATH
            self.tokenizer = AutoTokenizer.from_pretrained(directory_path)
            self.model = AutoModelForCausalLM.from_pretrained(directory_path)
        else:
            # low temp = less "creative"/random (more strict)
            # TODO: think about this more -- currently at 0.1
            self.llm = OpenAI(temperature=config.TEMPERATURE) # (text-davinci-003)

        if self.model:
            self.llm = self.initialize_local_model()
            logging.debug(f"LLM running on {self.model.device}")
        
    def initialize_local_model(self) -> HuggingFacePipeline:
        """Initialize local LLM."""
        local_pipe = pipeline("text-generation",
                               model=self.model,
                               tokenizer=self.tokenizer,
                               max_length=500)
        return HuggingFacePipeline(pipeline=local_pipe)
    
    def get_response_list(self, filepath):
        try:
            with open(filepath, 'r') as file:
                lines = [line.strip() for line in file]
            return lines
        
        except FileNotFoundError:
            print("File not found. Please check the file path.")
            return []
    
    def test_agent(self, extract_fn):
        ## TODO: Clean this up to be neater.
        responses_3 = self.get_response_list("agent_responses/responses-16036891.txt")
        responses_4 = self.get_response_list("agent_responses/responses-14552350.txt")
        responses = [responses_1, responses_2, responses_3, responses_4]
        codes = [code_1, code_2, code_3, code_4]

        assert len(responses) == len(codes)
        num_tests = len(responses)
        for i in range(num_tests):
            print(f"Running test: {i+1}")
            response = responses[i]
            code = codes[i]
            code_block = extract_fn(response)
            if not code_equivalence(code_block, code):
                print(f"Got following code: {code_block}")
                print(f"But, expected code: {code}")
                print(f"Expected {len(code)} chars but got {len(code_block)} instead.")
                return False
            assert code_equivalence(code_block, code)

        return True
    
    def save_response(self, responses):
        id = random.randint(1e7, 1e8-1)
        directory = "agent_responses"
        filename = "responses-" + str(id) + ".txt"

        if not os.path.exists(directory):
            os.makedirs(directory)
        
        with open(os.path.join(directory, filename), 'w') as f:
            for response in responses:
                f.write("%s\n" % response)

    def run_agent_tests(self):
        if self.test_agent(extract_fn=extract_code_from_response):
            print()
            print("="*50)
            print("SUCCESS: Agent tests passed!")
    
    def task_agent(self, prompt: str) -> Union[tuple, jsonify]:
        """Tasks LLM agent to process a given prompt/task."""
        if not prompt:
            return jsonify({'error': 'No task provided'}), 400
        
        self.init_agent()
        final_answer = self.agent.run(prompt)

        # Agent Logs
        logs = handler.log # gets verbose logs from agent LLM
        cleaned_logs = get_agent_thoughts(logs) # cleans logs
        # self.save_response(cleaned_logs) # UNCOMMENT to save logs for debugging

        response = cleaned_logs + [final_answer]
        if final_answer == "Agent stopped due to iteration limit or time limit.":
            return jsonify({'response': response})
        
        code_block = extract_code_from_response(cleaned_logs)
        response += [f'Extracted code:\n{code_block}']
        if code_block is not None:
            save_code_to_file(code=code_block, filename='agent_code', dir_name='agent_dir')

        return jsonify({'response': response})

    def error_handler(self, e: Exception) -> jsonify:
        """Handle errors during request processing."""
        logging.error(f"Error occurred: {e}")
        return jsonify({'error': 'An error occurred while processing the request.'}), 500