# Chatbot: Large Language Model UI (LLM-UI)

LLM-UI is a comprehensive user interface for interacting with large language models (LLMs). It uses 🦜️ Langchain for vector database retrieval and incorporates memory mechanisms for handling both local and non-local LLM interactions.

## Installation

Clone the repo to your local machine.

## Setup

1. After cloning the repository, install the necessary requirements.
2. You'll need to add your own API keys to apikeys.py
   * open_ai_key (to use both flask_app and agent_server)
   * hf_key (for agent_server)
   * serpapi_key (for agent_server)
3. 


## Setup Notes

Note: If you're running this on conda, there may be issues with hnswlib. Try the following on the command line:
* export HNSWLIB_NO_NATIVE=1
* conda install -c conda-forge hnswlib 

## Structure

The project is structured as follows:
* cli.py: Entry point of the application if you are using a command-line interface.
* config.py: Contains the configuration parameters for the project. Modify this file to suit your needs.
* prompts.py: Contains the prompts used by the chatbot. Feel free to modify or extend this file to customize the chatbot's behavior.
* server2.py: Contains the main server code for running the chatbot application. Start the application by running this file.
* templates: Contains HTML templates for the chatbot's web interface. You can customize the look and feel of the chatbot by modifying these templates.
* docs: Contains vector database files for retrieval

## Usage
* Update the config.py file with your desired configuration.
* Run the server2.py file to start the server.
* Navigate to the server's URL (http://127.0.0.1:5000) in your web browser to interact with the chatbot.

## Contributing

Contributions to the project are welcome.

This project is licensed under the terms of the MIT License.
