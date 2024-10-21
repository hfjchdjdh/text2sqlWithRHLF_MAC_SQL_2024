import json

from metagpt.actions import Action
import re

from config.Config import RouterTemplate

class RouterAction(Action):

    name:str = "Router"

    async def run(self, query):
        prompt = RouterTemplate.format(query=query)
        result = await self._aask(prompt)
        type = self._parse_json(result)
        type = json.loads(type)
        return type["type"]


    @staticmethod
    def _parse_json(content):
        pattern = r"```json(.*)```"
        match = re.search(pattern, content, re.DOTALL)
        code_text = match.group(1) if match else content
        return code_text