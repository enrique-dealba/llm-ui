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

        response, _ = server.task_agent(prompt)
        return response
    except Exception as e:
        return server.error_handler(e)

def create_parser() -> argparse.ArgumentParser:
    """Creates a command-line argument parser."""
    parser = argparse.ArgumentParser(description="Run the Flask server")
	# Usage: `--llm local` or `--llm davinci` etc
    parser.add_argument('--llm', choices=['local', 'chatgpt', 'davinci', 'custom_gpt', 'gpt4'], help='Choose an LLM for Agent')
	# Usage: `--mode text-code`, `--mode convo-code`, etc
    parser.add_argument('--mode', choices=['text-code', 'convo-code', 'json-agent'], help='Choose an Agent mode')
    return parser

if __name__ == "__main__":
    parser = create_parser()
    args = parser.parse_args()
    server = AgentServer(llm_mode=args.llm, agent_mode=args.mode, template=server_template)
    app.run()