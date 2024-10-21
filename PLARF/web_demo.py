import gradio as gr
from main import main
import asyncio

def create_html_table(query):
    # 假设我们根据查询生成一个简单的表格
    # 这里只是一个示例，你可以根据实际需求调整表格内容
    html_table = f"""
    {asyncio.run(main(query))}
    """

    print(html_table)
    return html_table

iface = gr.Interface(
    fn=create_html_table,
    inputs="text",
    outputs="html",
)

iface.launch()