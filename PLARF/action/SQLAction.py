import json
import re

from metagpt.actions import Action
from config.Config import SQLSelectActionTemplate,SQLDecomposeActionTemplate,SQLRefineActionTemplate
from tool.SQLTool import exec_sql
from config.Config import db_info

class SelectorAction(Action):

    name:str = "Select"

    async def run(self, prompt):
        result = await self._aask(prompt)
        return result


    @staticmethod
    def _parse_sql(content):
        pattern = r"```sql(.*)```"
        match = re.search(pattern, content, re.DOTALL)
        code_text = match.group(1) if match else content
        return code_text

class DecomposerAction(Action):

    name:str = "Decompose"

    async def run(self, prompt):
        result = await self._aask(prompt)
        return result


    @staticmethod
    def _parse_sql(content):
        pattern = r"```sql(.*)```"
        match = re.search(pattern, content, re.DOTALL)
        code_text = match.group(1) if match else content
        return code_text


class RefinerAction(Action):

    name:str = "Refine"

    MAX_ITER:int = 4

    async def run(self, prompt):
        prompt = await self._aask(prompt)
        sql = self._parse_sql(prompt)
        for i in range(self.MAX_ITER):
            try:
                table = exec_sql(db_info["path"], sql)
                return table
            except Exception as e:
                prompt = await self._aask(prompt)
                sql = self._parse_sql(prompt)

        return "Failure"


    @staticmethod
    def _parse_sql(content):
        pattern = r"```sql(.*)```"
        match = re.search(pattern, content, re.DOTALL)
        code_text = match.group(1) if match else content
        return code_text









