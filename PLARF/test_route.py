import asyncio
import json
import re


from agent.RouterAgent import *
from config.Config import PLARF_Template
from config.Config import *
from tool.SQLTool import exec_sql



async def main(query):
    # query = "我是北京人，我想了解本地2021年和2023年的招生的详情信息"
    msg = query
    role1 = RouterAgent()
    result = await role1.run(msg)
    print(result)

    return

asyncio.run(main("我是东北人，21年到23年的非指的最低分数线咋变的啊？"))




