import asyncio
import json
import re

from action.SQLAction import SelectorAction
from agent.SQLAgent import *
from config.Config import PLARF_Template
from config.Config import *
from tool.SQLTool import exec_sql


def parse_sql_from_string(input_string):
    sql_pattern = r'```sql(.*?)```'
    all_sqls = []
    # 将所有匹配到的都打印出来
    for match in re.finditer(sql_pattern, input_string, re.DOTALL):
        all_sqls.append(match.group(1).strip())

    if all_sqls:
        return all_sqls
    else:
        return "error: No SQL found in the input string"

async def main(query):
    # query = "我是北京人，我想了解本地2021年和2023年的招生的详情信息"
    msg = SQLSelectActionTemplate.format(SchemaTemplate=PLARF_Template, query=query)
    role1 = SQLSelectorAgent()
    result1 = await role1.run(msg)

    #

    print(result1.content[:])

    role2 = SQLDecomposerAgent()
    msg = SQLDecomposeActionTemplate.format(desc_str=PLARF_Template, query=query+"\n"+str(f"你应当重点考虑的列元素是：{result1.content[:]}"))
    result2 = await role2.run(msg)

    print(result2.content[:])
    sql = parse_sql_from_string(result2.content[:])
    print(sql)
    try:
        result = exec_sql(db_info["path"], sql)
    except Exception as e:
        msg = SQLRefineActionTemplate.format(query=query, desc_str=PLARF_Template, sql=sql,
                                             sqlite_error="", exception_class=str(e))
        role3 = SQLRefinerAgent()
        result = await role3.run(msg)

    return result

# asyncio.run(main("我是北京人，我想了解本地2021年和2023年的招生的详情信息"))




