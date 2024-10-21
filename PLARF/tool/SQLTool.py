import sqlite3
import pandas as pd
import time
from config.Config import attr_dict

query_path = r"G:\python_project\PLARF\tmp\query"

# 数据库文件路径
def exec_sql(database_path, query_sql):


    conn = sqlite3.connect(database_path)

    cursor = conn.cursor()
    cursor.execute(query_sql)
    # 获取列名
    column_names = [description[0] for description in cursor.description]

    # 获取查询结果，并使用列名创建字典
    rows = cursor.fetchall()
    rows_with_names = [dict(zip(column_names, row)) for row in rows]
    for row in rows_with_names:
        print(row)
    translated_data = [{attr_dict[key]: value for key, value in item.items()} for item in rows_with_names]

    data = pd.DataFrame(translated_data)

    print(data.to_html())

    data.to_html(query_path+r"\{}.html".format(time.time()))

    cursor.close()
    conn.close()
    return data.to_html()

def generate_db_schema(database_path):
    conn = sqlite3.connect(database_path)
    cursor = conn.cursor()

    # 查询数据库中的所有表结构
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    db_id = database_path.split("\\")[-1]
    # 输出结果初始化
    output = f"【DB_ID】 {db_id}\n【Schema】\n"

    # 遍历每个表
    for (table_name,) in tables:
        # 查询表结构
        cursor.execute(f"PRAGMA table_info({table_name});")
        table_info = cursor.fetchall()

        # 获取表中的数据样本
        cursor.execute(f"SELECT * FROM {table_name} LIMIT 5;")
        data_samples = cursor.fetchall()

        # 输出表信息
        output += f"# Table: {table_name}\n["

        # 输出列信息
        for idx, (cid, name, type, notnull, dflt_value, pk) in enumerate(table_info):
            # 提取数据样本
            sample_values = [str(row[idx]) for row in data_samples]
            # 输出列描述
            output += f"\n  ({name}, {type.lower()} column. Value examples: {sample_values}.),"

        # 去除最后一个逗号并添加换行
        output = output.rstrip(',') + "\n]\n"

    # 添加外键信息
    output += "【Foreign keys】\nNone\n"

    # 关闭游标和连接
    cursor.close()
    conn.close()
    print(output)






