# Chatbot: LLM-UI

LLM-UI is a comprehensive user interface for interacting with large language models (LLMs). It uses 🦜️ Langchain for vector database retrieval and incorporates memory mechanisms for handling both local and non-local LLM interactions.

## Installation

Clone the repo to your local machine.

## Setup

1. After cloning the repository, install the necessary requirements.
2. You'll need to add your own API keys to apikeys.py
   * `open_ai_key` (to use both flask_app and agent_app)
   * `hf_key` (for agent_app)
   * `serpapi_key` (for agent_app)

## Setup Notes

Note: If you're running this on conda, there may be issues with hnswlib. Try the following on the command line:
* `export HNSWLIB_NO_NATIVE=1`
* `conda install -c conda-forge hnswlib`

## Structure

The project is structured as follows:
* config.py: Contains HuggingFace model names for `--local` usage and LLM temperature settings.
* prompts.py & code_prompts.py: Contains the prompts used by the chatbot. Customize behavior by modifying these.
* flask_app.py: Contains the main server code for running the LLM chatbot application. Start by running this file.
* llm_logic.py: Logic functions specific to the LLM user interface.
* templates: Contains HTML templates for the chatbot's UI. Modify for custom appearance.
* docs: Contains vector database files for retrieval.

Agent LLM specific:
* agent_app.py: Contains the main server code for Agent LLM.
* agent_logic.py: Core logic functions for Agent LLM.
* agent_utils.py: Utility functions for Agent LLM.
* agent_dir: Directory where Agent LLM stores outputs.
* test_files & tests: Contains test data/scripts and unit/integration tests for Agent LLM.

## General Usage
* Update the config.py file with your desired local LLM (if using a non-OpenAI model).
* Run the `python flask_app.py` to start the server (or `python flask_app.py --local`).
* Navigate to the server's URL (`http://127.0.0.1:5000`) in your web browser to interact with the chatbot.

## Agent LLM Usage
* To use the Agent LLM, run `python agent_app.py`. For testing, in the UI, copy-paste the following coding task:
  * `Write a python function that takes in a list of integers as input and sorts it using the Quick Sort algorithm and then prints the sorted list before returning it`
* This should output a functional code snippet in the `agent_dir` directory under an `agent_code.py` file.
* Navigate to the server's URL (`http://127.0.0.1:5000`) in your web browser to interact with the chatbot.

## Contributing

Contributions to the project are welcome.

This project is licensed under the terms of the MIT License.
