import logging
import argparse

from prompts import server_template
from flask import Flask, request, jsonify, render_template
from agent_logic import AgentServer

app = Flask(__name__)
logging.basicConfig(level=logging.DEBUG)

@app.route('/', methods=['GET', 'POST'])
def home() -> str:
    """Renders home page for LLM agent."""
    return render_template('agent-index.html')

@app.route('/chat', methods=['POST'])
def chat() -> jsonify:
    """Handles chat requests via LLM agent."""
    
    try:
        prompt = request.json['prompt']

        return server.task_agent(prompt)
    except Exception as e:
        return server.error_handler(e)

def get_parser():
	parser = argparse.ArgumentParser(description="Run the Flask server")
	parser.add_argument('--local', action='store_true', help='Use local server settings')
	parser.add_argument('--mode', choices=['non-vectordb', 'vectordb', 'vectordb-memory'],
                     default='vectordb-memory', help='Choose the server mode')
	return parser

## TODO: add options for task-code AND convo-code as server modes
## TODO: add multi-chat multi-message functionality
def create_parser() -> argparse.ArgumentParser:
    """Creates a command-line argument parser."""
    parser = argparse.ArgumentParser(description="Run the Flask server")
    parser.add_argument('--local', action='store_true', help='Use local server settings')
    return parser

if __name__ == "__main__":
    parser = create_parser()
    args = parser.parse_args()
    server = AgentServer(use_local=args.local, template=server_template)
    app.run()