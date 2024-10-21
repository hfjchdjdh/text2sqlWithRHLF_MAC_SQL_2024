import asyncio

from metagpt.roles.product_manager import ProductManager
from metagpt.logs import logger
from agent.DataAnalyseAgent import *


async def ReportGen():
    msg = """
        {
          "name": "gaojian",
          "sex": "male",
          "age": 20,
          "school": "NEU"
        }
    
        """
    role = ReportAgent()
    result = await role.run(msg)
    logger.info(result.content[:])

async def data_analysis():
    msg = """
    ```json
            {
              "content_file": "G:/python_project/RapStarAgent/content_file/schools.csv",
              "plt_path": "G:/python_project/RapStarAgent/plt_path",
              "requirement": "For each feature’s data distribution, if the number of unique values is greater than 3, a pie chart should be used when plotting, and only the names of the top three most frequent features should be displayed. The rest should be represented by 'Others'.",
              "content_dict": "None",
              "data_preview_path": "G:/python_project/RapStarAgent/data_preview"
            }
    ```
            """
    role = ReportAgent()
    result = await role.run(msg)
    logger.info(result.content[:])

async def main():
    pass


if __name__ == '__main__':
    asyncio.run(data_analysis())