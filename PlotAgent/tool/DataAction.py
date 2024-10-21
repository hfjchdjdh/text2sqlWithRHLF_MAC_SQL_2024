import json
import re

from metagpt.actions import Action
from metagpt.roles.di.data_interpreter import *
import pdfkit
import time


REPORT_PATH = "D:/text2sql/Report"

class ReportGenerator(Action):

    PROMPT_TEMPLATE:str = """
    Please convert the corresponding information into an HTML table format, with the requirements:

    1.Organized and logical arrangement
    2.Consistent with the corresponding relationships 
    3.
    The relevant information is as follows (in JSON format): 
    {content}
    """
    # name:str = "Alice"
    PATH:str = r"G:\python_project\RapStarAgent\data_preview\summary.csv"
    async def run(self, content):
        content = self.PATH
        content = self.dataframe2html(content)
        content_path = self._parse_pdf(content)
        return content_path

    @staticmethod
    def _parse_root(content):
        pattern = r"```path\((.*?)\)```"
        match = re.search(pattern, content, re.DOTALL)
        code_text = match.group(1) if match else content
        return code_text

    @staticmethod
    def dataframe2html(path):
        import pandas as pd

        df = pd.read_csv(path)

        html_table = df.to_html(escape=False, index=False)
        return html_table

    @staticmethod
    def _parse_pdf(html_code):

        pdf_path = REPORT_PATH+f"/{time.time()}.pdf"
        with open(pdf_path,"w"):
            pass
        pdfkit.from_string(html_code, pdf_path)
        return pdf_path

    @staticmethod
    def _parse_doc(html_code):
        pass

    @staticmethod
    def _parse_html(content):
        pattern = r"```html(.*)```"
        match = re.search(pattern, content, re.DOTALL)
        code_text = match.group(1) if match else content
        return code_text

class DataPreview(Action):
    PROMPT_TEMPLATE: str = """
        Please write Python code to analyze the data file “{content_file}” based on the provided data dictionary 
        from the following perspectives: 
        1. Data distribution of each feature (pie chart or bar chart, save the figure to the “{plt_path}” path) 
        2. Mean of each feature (fill in “N/A” if it cannot be solved) 
        3. Mode of each feature (fill in “N/A” if it cannot be solved)
        4. Median of each feature (fill in “N/A” if it cannot be solved)
        5. Variance of each feature (fill in “N/A” if it cannot be solved)
        6. Standard deviation of each feature (fill in “N/A” if it cannot be solved) 
        7. Number of missing values of each feature
        8. satisfying the custom requirement:{requirement}
        #########################################################zzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzz
        data dictionary： 
        {content_dict}
        #########################################################
        The final output of the code will be saved in the "{data_preview_path}" path in the following format(using CSV format):
        feature,graph,mean,mode,median,variance,SD,missing values,custom requirement
        feature1,{plt_path}/feature1.svg,Mean of feature1,Mode of feature1,Median of feature1,Variance of feature1,Standard deviation of feature1,Number of missing values of feature1,custom requirement of feature1
        ......
        featureN,{plt_path}/featureN.svg,Mean of featureN,Mode of featureN,Median of featureN,Variance of featureN,Standard deviation of featureN,Number of missing values of featureN,custom requirement of featureN
        ########################################################
        Remember, the python code should eventually give out the final CSV file's path in following format:
        "```path({{file_path}})```"
        example:"```path(G:/python_project/RapStarAgent/data_preview/summary.csv)```"
        """
    # name: str = "Bob"

    async def run(self, json_query):
        json_query = self._parse_data(json_query)
        print(json_query)
        json_query = json.loads(json_query)
        query = self.PROMPT_TEMPLATE.format(
            content_file=json_query["content_file"],
            plt_path=json_query["plt_path"],
            requirement=json_query["requirement"],
            content_dict=json_query["content_dict"],
            data_preview_path=json_query["data_preview_path"],
                                            )
        response = await self._aask(query)
        code_text = self._parse_code(response)
        return code_text

    @staticmethod
    def _parse_code(content):
        pattern = r"```python(.*)```"
        match = re.search(pattern, content, re.DOTALL)
        code_text = match.group(1) if match else content
        return code_text

    @staticmethod
    def _parse_data(content):
        pattern = r"```json(.*)```"
        match = re.search(pattern, content, re.DOTALL)
        code_text = match.group(1) if match else content
        return code_text


class Executor(Action):
    execute_code: ExecuteNbCode = Field(default_factory=ExecuteNbCode, exclude=True)
    async def run(self, code):
        result, success = await self.execute_code.run(code)
        return result





