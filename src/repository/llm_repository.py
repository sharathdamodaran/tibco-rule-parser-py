import json
import requests
from util.prompt_util import PromptEngineeringUtil
from model.LLMResponse import LLMResponse
from model.RuleNode import RuleNode
from typing import List

class LLMRepository:

    def translate_code(self, endpoint_url: str, rule: RuleNode, child_rules: List[RuleNode]) -> str:
        client = requests.Session()
        client.headers.update({'Content-Type': 'application/json; charset=utf-8'})

        prompt_json = PromptEngineeringUtil.get_prompt_json(rule, child_rules)

        try:
            response = client.post(endpoint_url, data=prompt_json, timeout=20)
            response.raise_for_status()
            
            result = []
            for line in response.iter_lines():
                if line:
                    line_json = json.loads(line)
                    if 'done_reason' in line_json:
                        print(line_json)
                    else:
                        llm_response = LLMResponse(**line_json)
                        result.append(llm_response.response)
            
            return ''.join(result)
        except Exception as ex:
            print(ex)
            return str(ex)