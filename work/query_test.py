import pandas as pd
import gradio as gr

from common.my_config import MyConfig
from common.vanna_calls import setup_vanna

config = MyConfig()

vn = setup_vanna()


def generate_sql(question):
    # _admin
    try:

        sql, prompt, question_sql_list, ddl_list = vn.generate_sql(question=question, allow_llm_to_see_data=True)
        is_sql_valid = vn.is_sql_valid(sql=sql)
        print("1" * 50)
        print(sql)
        print("2" * 50)
        print(prompt)
        print("3" * 50)
        print(ddl_list)
        print("4" * 50)
        print(question_sql_list)
        print("5" * 50)
        print(is_sql_valid)

        df_result = vn.run_sql(sql=sql)
        return pd.DataFrame(prompt), pd.DataFrame(question_sql_list), pd.DataFrame(
            {"DDL": ddl_list}), sql, df_result, is_sql_valid
    # print(df)
    except ValueError:
        print("出现错误啦！")
        gr.Error("出现错误啦！")
        return None, None, None, "", "", ""
