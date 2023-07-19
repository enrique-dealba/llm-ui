import logging
import argparse

from prompts import server_template
from flask import Flask, request, jsonify, render_template
from llm_logic import LLMServer

app = Flask(__name__)
logging.basicConfig(level=logging.DEBUG)

@app.route('/', methods=['GET', 'POST'])
def home() -> str:
  """Renders home page for LLM."""
  return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat() -> jsonify:
  """Handles chat prompts via LLM."""

  try:
    prompt = request.json['prompt']
    # server = LLMServer(use_local=True, mode='vectordb-memory', template="")
    if server.mode == "non-vectordb":
      return server.chat_with_model(prompt)
    elif server.mode == "vectordb":
      return server.chat_with_db(prompt)
    elif server.mode == "vectordb-memory":
      return server.chat_with_memory(prompt)
    else:
      raise ValueError(f"Invalid mode: {server.mode}")
  except Exception as e:
      return server.error_handler(e)

def get_parser():
  parser = argparse.ArgumentParser(description="Run the Flask server")
  parser.add_argument('--local', action='store_true', help='Use local server settings')
  parser.add_argument('--mode', choices=['non-vectordb', 'vectordb', 'vectordb-memory'],
                      default='vectordb-memory', help='Choose the server mode')
  return parser

if __name__ == "__main__":
  parser = get_parser()
  args = parser.parse_args()
  server = LLMServer(use_local=args.local, mode=args.mode, template=server_template)
  app.run()