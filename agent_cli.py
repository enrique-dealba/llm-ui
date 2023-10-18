import argparse
import logging
from agent_logic import AgentServer
from prompts import server_template

def chat_with_agent(server: AgentServer) -> None:
    while True:
        prompt = input("You: ")
        response, _ = server.task_agent(prompt)
        print(f"LLM: {response}")
        cont = input("Continue chatting? (y/n): ")
        if cont.lower() != 'y':
            break

def create_parser() -> argparse.ArgumentParser:
    """Creates a command-line argument parser."""
    parser = argparse.ArgumentParser(description="Run the CLI agent")
    parser.add_argument('--llm', choices=['local', 'vllm', 'chatgpt', 'davinci', 'custom_gpt', 'gpt4'], help='Choose an LLM for Agent')
    parser.add_argument('--mode', choices=['text-code', 'convo-code', 'json-agent'], help='Choose an Agent mode')
    return parser

if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    parser = create_parser()
    args = parser.parse_args()
    server = AgentServer(llm_mode=args.llm, agent_mode=args.mode, template=server_template, is_flask_app=False)
    chat_with_agent(server)
