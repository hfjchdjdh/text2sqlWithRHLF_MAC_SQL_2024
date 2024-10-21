db_info = {
    "path": r"D:\text2sql\PLARF\PLARF.db"
}

RouterTemplate = """
你是一个路由管理员，现在给你一个用户的请求，请你根据用户的请求，判断这是一个“查询任务”还是一个“分析任务”。
######################例子##########################
query:我是山东人，我想看看2023年指挥类分数线多高
answer:
```json
{{
    "type":"SQLAgent"
}}
```
query:我是北京人，我想看看2021年到2023年指挥类男生最低分数线的变化
answer:
```json
{{
    "type":"PlotAgent"
}}
```
####################################################
现在请回答：
query:{query}
answer:
"""

PLARF_Template = """
【DB_ID】 PLARF.db
【Schema】
# Table: AdmissionTable
[
  (province, 招生省份, Value examples: ['北京', '北京', '河北', '河北', '山西'].),
  (isCommand, 是否是指挥类, Value examples: ['非指', '指挥'].),
  (plannedMaleNum, 计划招收男学生数量, Value examples: ['4', '5', '6', '55', '7'].),
  (plannedFemaleNum, 计划招收女学生数量, Value examples: ['1', '0', '1', '2', '1'].),
  (admissionMaleNum, 录取男学生数量, Value examples: ['4', '3', '6', '55', '7'].),
  (admissionFemaleNum, 录取女学生数量, Value examples: ['1', '0', '1', '2', '1'].),
  (firstBatchScore, 一本线分数（这不是学校的分数线）, Value examples: ['513', '513', '498', '498', '505'].),
  (maleHighestScore, 录取男学生最高分（本校男生最高分数线）, Value examples: ['587', '543', '612', '604', '585'].),
  (maleLowestScore, 录取男学生最低分（本校男生最低分数线）, Value examples: ['516', '523', '590', '570', '552'].),
  (lowestRank, 最低排名, Value examples: ['21457', '20286', '17509', '28819', '15177'].),
  (averageAdmissionScore, 平均录取分数, Value examples: ['551', '531', '599', '583', '569'].),
  (femaleLowestScore, 录取女学生最低分, Value examples: ['516', 'None', '612', '597', '556'].),
  (year, 招生年份, Value examples: ['2021', '2022', '2023', '2020'].)
]
【Foreign keys】
None
"""

SQLSelectActionTemplate = """
作为经验丰富的专业数据库管理员，您的任务是分析用户的问题和数据库模式，以提供相关信息。

[指示]：
丢弃任何与用户问题及证据无关的表格模式。
对每个相关表格中的列按相关性降序排序，并保留前6列。
确保最终输出的JSON中至少包含3个表格。
输出格式应为JSON。


[要求]：
如果一个表格的列数小于或等于10列，标记为“keep_all”。
如果一个表格与用户问题及证据完全无关，标记为“drop_all”。
根据列的相关性对每个相关表格中的列进行优先排序。

这里给出一个例子example.csv:

==========
【DB_ID】 banking_system
【Schema】
# Table: account
[
  (account_id, the id of the account. Value examples: [11382, 11362, 2, 1, 2367].),
  (district_id, location of branch. Value examples: [77, 76, 2, 1, 39].),
  (frequency, frequency of the acount. Value examples: ['POPLATEK MESICNE', 'POPLATEK TYDNE', 'POPLATEK PO OBRATU'].),
  (date, the creation date of the account. Value examples: ['1997-12-29', '1997-12-28'].)
]
# Table: client
[
  (client_id, the unique number. Value examples: [13998, 13971, 2, 1, 2839].),
  (gender, gender. Value examples: ['M', 'F']. And F：female . M：male ),
  (birth_date, birth date. Value examples: ['1987-09-27', '1986-08-13'].),
  (district_id, location of branch. Value examples: [77, 76, 2, 1, 39].)
]
# Table: loan
[
  (loan_id, the id number identifying the loan data. Value examples: [4959, 4960, 4961].),
  (account_id, the id number identifying the account. Value examples: [10, 80, 55, 43].),
  (date, the date when the loan is approved. Value examples: ['1998-07-12', '1998-04-19'].),
  (amount, the id number identifying the loan data. Value examples: [1567, 7877, 9988].),
  (duration, the id number identifying the loan data. Value examples: [60, 48, 24, 12, 36].),
  (payments, the id number identifying the loan data. Value examples: [3456, 8972, 9845].),
  (status, the id number identifying the loan data. Value examples: ['C', 'A', 'D', 'B'].)
]
# Table: district
[
  (district_id, location of branch. Value examples: [77, 76].),
  (A2, area in square kilometers. Value examples: [50.5, 48.9].),
  (A4, number of inhabitants. Value examples: [95907, 95616].),
  (A5, number of households. Value examples: [35678, 34892].),
  (A6, literacy rate. Value examples: [95.6, 92.3, 89.7].),
  (A7, number of entrepreneurs. Value examples: [1234, 1456].),
  (A8, number of cities. Value examples: [5, 4].),
  (A9, number of schools. Value examples: [15, 12, 10].),
  (A10, number of hospitals. Value examples: [8, 6, 4].),
  (A11, average salary. Value examples: [12541, 11277].),
  (A12, poverty rate. Value examples: [12.4, 9.8].),
  (A13, unemployment rate. Value examples: [8.2, 7.9].),
  (A15, number of crimes. Value examples: [256, 189].)
]
【Foreign keys】
client.`district_id` = district.`district_id`
【Question】
在平均工资最低的分支机构中开户的最年轻客户的性别是什么？
【Answer】
```json
{{
  "account": "keep_all",
  "client": "keep_all",
  "loan": "drop_all",
  "district": ["district_id", "A11", "A2", "A4", "A6", "A7"]
}}
```
Question Solved.
==========

这里有一个新的 example.csv, 请开始回答:

{SchemaTemplate}
【Question】
{query}
【Answer】
"""

SQLDecomposeActionTemplate = """
给定一个【数据库模式】描述，一个知识【证据】以及一个【问题】，你需要使用有效的SQLite，并理解数据库和知识，然后将问题分解为子问题以进行文本到SQL的生成。 在生成SQL时，我们应始终考虑以下约束：
 【约束】
在 SELECT <列> 中，只选择【问题】中需要的列，不要包含任何不必要的列或值
在 FROM <表> 或 JOIN <表> 中，不要包含不必要的表
如果使用 max 或 min 函数，应先 JOIN <表>，然后使用 SELECT MAX(<列>) 或 SELECT MIN(<列>)
如果 <列> 的【值示例】中有 ‘None’ 或 None，使用 JOIN <表> 或 WHERE <列> is NOT NULL 会更好
如果使用 ORDER BY <列> ASC|DESC，在此之前添加 GROUP BY <列> 以选择不同的值

务必按照所给范例的格式严格书写
==========[范例]==========

【Database schema】 california_schools.db
# Table: frpm
[
  (CDSCode, CDSCode. Value examples: ['01100170109835', '01100170112607'].),
  (Charter School (Y/N), Charter School (Y/N). Value examples: [1, 0, None]. And 0: N;. 1: Y),
  (Enrollment (Ages 5-17), Enrollment (Ages 5-17). Value examples: [5271.0, 4734.0].),
  (Free Meal Count (Ages 5-17), Free Meal Count (Ages 5-17). Value examples: [3864.0, 2637.0]. And eligible free rate = Free Meal Count / Enrollment)
]
# Table: satscores
[
  (cds, California Department Schools. Value examples: ['10101080000000', '10101080109991'].),
  (sname, school name. Value examples: ['None', 'Middle College High', 'John F. Kennedy High', 'Independence High', 'Foothill High'].),
  (NumTstTakr, Number of Test Takers in this school. Value examples: [24305, 4942, 1, 0, 280]. And number of test takers in each school),
  (AvgScrMath, average scores in Math. Value examples: [699, 698, 289, None, 492]. And average scores in Math),
  (NumGE1500, Number of Test Takers Whose Total SAT Scores Are Greater or Equal to 1500. Value examples: [5837, 2125, 0, None, 191]. And Number of Test Takers Whose Total SAT Scores Are Greater or Equal to 1500. . commonsense evidence:. . Excellence Rate = NumGE1500 / NumTstTakr)
]

【Foreign keys】
frpm.`CDSCode` = satscores.`cds`

【Question】
列出那些SAT优秀率超过平均水平的特许学校的校名。


将上述问题拆分为子问题，同时考虑到【约束】，经过逐步思考后编写SQL语句:

Sub question 1: 获取特许学校SAT优秀率的平均值。
SQL
```sql
SELECT AVG(CAST(T2.`NumGE1500` AS REAL) / T2.`NumTstTakr`)
    FROM frpm AS T1
    INNER JOIN satscores AS T2
    ON T1.`CDSCode` = T2.`cds`
    WHERE T1.`Charter School (Y/N)` = 1
```

Sub question 2: 列出那些SAT优秀率超过平均水平的特许学校的校名。
SQL
```sql
SELECT T2.`sname`
  FROM frpm AS T1
  INNER JOIN satscores AS T2
  ON T1.`CDSCode` = T2.`cds`
  WHERE T2.`sname` IS NOT NULL
  AND T1.`Charter School (Y/N)` = 1
  AND CAST(T2.`NumGE1500` AS REAL) / T2.`NumTstTakr` > (
    SELECT AVG(CAST(T4.`NumGE1500` AS REAL) / T4.`NumTstTakr`)
    FROM frpm AS T3
    INNER JOIN satscores AS T4
    ON T3.`CDSCode` = T4.`cds`
    WHERE T3.`Charter School (Y/N)` = 1
  )
```

Combined:将上面的所有查询合并成为一个查询。
```sql
SELECT T2.`sname`
FROM frpm AS T1
INNER JOIN satscores AS T2
ON T1.`CDSCode` = T2.`cds`
WHERE T2.`sname` IS NOT NULL
AND T1.`Charter School (Y/N)` = 1
AND CAST(T2.`NumGE1500` AS REAL) / T2.`NumTstTakr` > (
    SELECT AVG(CAST(T4.`NumGE1500` AS REAL) / T4.`NumTstTakr`)
    FROM frpm AS T3
    INNER JOIN satscores AS T4
    ON T3.`CDSCode` = T4.`cds`
    WHERE T3.`Charter School (Y/N)` = 1
)
```


Question Solved.

==========
【Database schema】
{desc_str}
【Question】
{query}

"""

SQLRefineActionTemplate = """
【指令】 执行下面的SQL时发生了一些错误，请根据查询和数据库信息修复SQL。如果需要，请逐步解决任务。在代码块中使用SQL格式，并在代码块中指明脚本类型。 找到答案后，请仔细验证答案。如果可能，请在回复中包含可验证的证据。 【约束】

在 SELECT <列> 中，只选择【问题】中需要的列，不要包含任何不必要的列或值
在 FROM <表> 或 JOIN <表> 中，不要包含不必要的表
如果使用最大值或最小值函数，请先 JOIN <表>，然后使用 SELECT MAX(<列>) 或 SELECT MIN(<列>)
如果 <列> 的【值示例】中有 ‘None’ 或 None，使用 JOIN <表> 或 WHERE <列> is NOT NULL 会更好
如果使用 ORDER BY <列> ASC|DESC，在此之前添加 GROUP BY <列> 以选择不同的值
【请求】
-- {query}
【数据库信息】
{desc_str}
【出错的SQL】
```sql
{sql}
```
【SQLite error】 
{sqlite_error}

【Exception class】
{exception_class}

现在请修改出错的SQL，并重新产生一个有效SQL
【correct SQL】

"""

PlotActionTemplate = """

"""

DataActionTemplate = """

"""

attr_dict = {
    "province": "省份",
    "isCommand": "类型",
    "plannedMaleNum": "计划招收男性数",
    "plannedFemaleNum": "计划招收女性数",
    "admissionMaleNum": "录取男性数量",
    "admissionFemaleNum": "录取女性数量",
    "firstBatchScore": "一本线",
    "maleHighestScore": "男性最高分",
    "maleLowestScore": "男性最低分",
    "lowestRank": "男性最低排名",
    "averageAdmissionScore": "平均高考分数",
    "femaleLowestScore": "女性最低分",
    "year": "招生年份"
}
