from tool.SQLTool import *
from config.Config import db_info


# exec_sql(db_info["path"], "PRAGMA table_info(AdmissionTable);")

generate_db_schema(db_info["path"])












