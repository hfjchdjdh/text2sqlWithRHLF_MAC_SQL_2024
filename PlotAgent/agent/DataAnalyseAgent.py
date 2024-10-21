from metagpt.actions import ExecuteNbCode
from metagpt.roles import Role
from metagpt.schema import Message
from metagpt.actions.di.write_analysis_code import *
from metagpt.roles.di.data_interpreter import DataInterpreter
from metagpt.schema import logger

from tool.DataAction import ReportGenerator
from tool.DataAction import Executor
from tool.DataAction import DataPreview

from pydantic import Field

class ReportAgent(Role):

    name:str = "Zhang"
    profile:str = "ReportAgent"


    def __init__(self, /, **data):
        super().__init__(**data)
        self.set_actions([DataPreview, Executor, ReportGenerator])
        self._set_react_mode(react_mode="by_order")

    async def _act(self) -> Message:
        logger.info(f"{self._setting}: to do {self.rc.todo}({self.rc.todo.name})")
        todo = self.rc.todo  # todo will be SimpleWriteCode()

        msg = self.get_memories(k=1)[-1]  # find the most recent messages
        code_text = await todo.run(msg.content)

        msg = Message(content=code_text, role=self.profile, cause_by=type(todo))
        self.rc.memory.add(msg)

        return msg





