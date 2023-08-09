import unittest

from agent_logic import AgentServer
from agent_utils import code_equivalence, extract_code_from_response
from test_files.responses import responses_1, responses_2, code_1, code_2, code_3, code_4

class AgentTestCase(unittest.TestCase):
    def setUp(self):
        self.agent_server = AgentServer(llm_mode='davinci', agent_mode='text-code', template="")

    def convo_setUp(self):
        self.agent_server = AgentServer(llm_mode='davinci', agent_mode='convo-code', template="")
        
    def test_agent_responses(self):
        responses_3 = self.agent_server.get_response_list("agent_responses/responses-16036891.txt")
        responses_4 = self.agent_server.get_response_list("agent_responses/responses-14552350.txt")
        responses = [responses_1, responses_2, responses_3, responses_4]
        codes = [code_1, code_2, code_3, code_4]
        self.assertEqual(len(responses), len(codes))
        num_tests = len(responses)
        for i in range(num_tests):
            print(f"Running test: {i+1}")
            response = responses[i]
            code = codes[i]
            code_block = extract_code_from_response(response)
            if not code_equivalence(code_block, code):
                print(f"Got following code: {code_block}")
                print(f"But, expected code: {code}")
                print(f"Expected {len(code)} chars but got {len(code_block)} instead.")
                return False
            self.assertTrue(code_equivalence(code_block, code))

if __name__ == '__main__':
    unittest.main()