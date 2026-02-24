import gradio as gr
import json
import pandas as pd
# import Common_Chroma as ccc


# 共通函数

from common.Work_DB_call import run_sql
from common.my_config import MyConfig
from common.vanna_calls import setup_vanna
from common.LLM import MyLLM

config = MyConfig()
vn = setup_vanna()
my_llm = MyLLM()

# Dao
from dao.llm_dao import LLMDao, LLM

llm_dao = LLMDao()


def save_sql_question(text):
    # 把text保存到文本中
    with open("temp_sql_question.txt", "a", encoding="utf-8") as f:
        f.write(text + "\n")


def load_sql_question():
    # 读取文本中的数据
    with open("temp_sql_question.txt", "r", encoding="utf-8") as f:
        data = f.read()
        return data


def select_json_data(evt: gr.SelectData, df: pd.DataFrame):
    selected_index = evt.index[0]  # 获取选中行的索引
    selected_row = df.iloc[selected_index]  # 获取选中行的所有数据
    return selected_row['question'], selected_row['sql']


def run_this_sql(sql):
    return run_sql(sql)


def get_prompt(count):
    return "str1"


def filter_train_use_data(table_name, filter_data):
    sql = f"select * from {table_name} where 1=1 "
    if filter_data:
        sql += f" and {filter_data}"

    # if organization != "全て":
    #     sql += f" and 組織='{organization}'"
    # if code != "全て":
    #     sql += f" and 勘定科目='{code}'"

    sql += f" LIMIT 20"

    print("sql:", sql)
    df_results = run_sql(sql)
    return df_results
    # Create a DataFrame
    #
    # # columns = [
    # #     "会計年度", "財務諸表区分", "勘定科目区分", "集計勘定科目", "勘定科目細目", "会社区分",
    # #     "事業部門", "所管部", "課・グループ"
    # # ]
    # columns = [
    #     "会計年度", "勘定科目", "組織"
    # ]
    # # 生成 实績_1月 到 予測_12月 的列名
    # for month in range(1, 13):
    #     columns.append(f"実績_{month}月")
    #     columns.append(f"予測_{month}月")
    #
    # # 创建 DataFrame
    # df = pd.DataFrame(results, columns=columns)
    # return df


def get_selected_llm():
    selected_llm = llm_dao.get_llm_by_id(llm_dao.get_selected_llm_id())
    model = my_llm.get_openai_llm(selected_llm.model_name, selected_llm.api_key, selected_llm.base_url)
    return model


def select_dll_list(evt: gr.SelectData, df: pd.DataFrame):
    selected_index = evt.index[0]  # 获取选中行的索引
    selected_row = df.iloc[selected_index]  # 获取选中行的所有数据
    return selected_row['DDL'], selected_row['Name']


def show_table(json_data):
    # df = pd.DataFrame(json_data)
    # data = json.loads(json_data)
    print("1" * 50)
    print(json_data)

    # 获取字符串中的JSON部分
    start_index = json_data.find('[')
    end_index = json_data.rfind(']') + 1

    # Extract only the JSON part
    json_data = json_data[start_index:end_index]

    # 将字符串中的单引号替换为双引号
    # json_data = json_data.replace("'", '"')
    data = json.loads(json_data)
    print("2" * 50)
    print(data)
    # 使用pd.json_normalize将字典转换为DataFrame
    df = pd.DataFrame(data)
    return df


def load_json():
    # 读取本地txt文件
    with open('question_sql.json', 'r', encoding='utf-8') as f:
        data = f.read()
        # change data to json
        return json.loads(data)


def train_sql_data(data):
    # 将数据保存到DataFrame
    df = show_table(data)

    # 将DataFrame中的数据逐条插入到数据库
    for index, row in df.iterrows():
        print("row index insert:", index)
        vn.add_question_sql(question=row['question'], sql=row['sql'])

    return "Data train successful!"


def train_dll_data(df):
    # 将DataFrame中的数据逐条插入到数据库
    for index, row in df.iterrows():
        print("row index insert:", index)
        vn.add_ddl(ddl=row['DDL'])
    gr.Info("Data train successful!")
    return "Data train successful!"
