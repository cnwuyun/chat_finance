# vanna
from vanna_main.qianwen import QianWenAI_Chat
from vanna_main.chromadb import ChromaDB_VectorStore

#系统函数
import os
from dotenv import load_dotenv, find_dotenv

import gradio as gr
import json
import pandas as pd
# import Common_Chroma as ccc

# 共通函数
from common.LLM import MyLLM
from common.LLM_call import generate_question_sql
from common.DB_call import get_ddl
from common.my_config import MyConfig

config = MyConfig()
llm = MyLLM()
embeddings = llm.EmbeddingsModel.get_DashScope_embeddings_model()

_ = load_dotenv(find_dotenv())
DASHSCOPE_API_KEY = os.environ["DASHSCOPE_API_KEY"]




class MyVanna(ChromaDB_VectorStore, QianWenAI_Chat):
    def __init__(self, config=None):
        ChromaDB_VectorStore.__init__(self, config=config)
        QianWenAI_Chat.__init__(self, config={'api_key': DASHSCOPE_API_KEY, 'model': 'qwen-plus'})


vn = MyVanna()
vn.connect_to_sqlite(config.finance_db_path)


def train_sql_data(data):
    # 将数据保存到DataFrame
    df = show_table(data)

    # 将DataFrame中的数据逐条插入到数据库
    for index, row in df.iterrows():
        print("row index insert:", index)
        vn.add_question_sql(question=row['question'], sql=row['sql'])

    return "训练数据追加成功"


def train_dll_data(df):
    # 将DataFrame中的数据逐条插入到数据库
    for index, row in df.iterrows():
        print("row index insert:", index)
        vn.add_ddl(ddl=row['DDL'])

    return "训练数据追加成功"


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


def save_model(name):
    return "保存成功"


def generate_sql(question):
    sql, prompt, question_sql_list, ddl_list = vn.generate_sql_admin(question=question, allow_llm_to_see_data=True)
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
    # print(df)

    return pd.DataFrame(prompt), pd.DataFrame(question_sql_list), pd.DataFrame(
        {"DDL": ddl_list}), sql, df_result, is_sql_valid

def get_prompt(count):

    return "str1"

with gr.Blocks() as demo:
    gr.Markdown("""# ChatBI设定页面""")

    with gr.Tab("训练数据追加"):
        with gr.Tab("DDL训练数据生成"):
            with gr.Blocks():
                with gr.Row():
                    df = gr.DataFrame(headers=["Table Name ","DDL"])
                with gr.Row():
                    btn_get_dll = gr.Button("所有DLL取得")
                    btn_save_dll = gr.Button("保存DLL训练数据")
                with gr.Row():
                    txt_save_ddl_result = gr.Textbox("DDL训练数据保存成功")
                btn_get_dll.click(get_ddl, inputs=[], outputs=[df])
                btn_save_dll.click(train_dll_data, inputs=[df], outputs=[txt_save_ddl_result])
        with gr.Tab("SQL训练数据生成"):
            with gr.Blocks():
                with gr.Row():
                    txt_count = gr.Textbox(label="训练数据数量")
                    # btn_get_prompt = gr.Button("显示提示词")
                    btn_generate = gr.Button("训练数据生成")
                with gr.Row():
                    txt_prompt = gr.Textbox(label="Prompt", lines=3, interactive=True)
                with gr.Row():
                    txt_json_result = gr.Textbox(label="Json数据", lines=20, interactive=True)
                with gr.Row():
                    btn_show_table = gr.Button("整理到表里中")
                with gr.Row():
                    df = gr.DataFrame()
                with gr.Row():
                    btn_save = gr.Button("保存训练数据")
                with gr.Row():
                    txt_save_result = gr.Textbox("训练数据保存成功")
                btn_generate.click(generate_question_sql, inputs=[txt_count], outputs=[txt_json_result,txt_prompt])
                btn_show_table.click(show_table, inputs=[txt_json_result], outputs=[df])
                btn_save.click(train_sql_data, inputs=[txt_json_result], outputs=[txt_save_result])
                # btn_get_prompt.click(get_prompt, inputs=[txt_count], outputs=[txt_prompt])
                # btn_json_load.click(load_json, inputs=[], outputs=[txt_json_result])
        with gr.Tab("训练数据单个追加"):
            with gr.Blocks():
                with gr.Row():
                    question = gr.Textbox(label="问题")
                with gr.Row():
                    sql = gr.Textbox(label="SQL")
                with gr.Row():
                    btn_sql = gr.Button("SQL追加")

                with gr.Row():
                    ddl = gr.Textbox(label="DDL")
                with gr.Row():
                    btn_ddl = gr.Button("DDL追加")
                with gr.Row():
                    doc = gr.Textbox(label="文档")
                with gr.Row():
                    btn_doc = gr.Button("Doc追加")
                with gr.Row():
                    result = gr.Textbox(label="处理结果")
                btn_sql.click(vn.add_question_sql, inputs=[question, sql], outputs=[result])
                btn_ddl.click(vn.add_ddl, inputs=[ddl], outputs=[result])
                btn_doc.click(vn.add_documentation, inputs=[doc], outputs=[result])

    with gr.Tab("训练数据列表"):
        with gr.Blocks():
            with gr.Tab("读取数据"):
                read_btn = gr.Button("读取数据")
                read_output = gr.Dataframe(label="数据库内容",
                                           headers=["id", "question", "content", "training_data_type"],
                                           column_widths=["10%", "20%", "60%", "10%"],wrap=True)

            read_btn.click(vn.get_training_data, inputs=[], outputs=[read_output])

            with gr.Tab("删除数据"):
                delete_content_input = gr.Textbox(label="id")
                delete_btn = gr.Button("删除数据")
                delete_output = gr.Textbox(label="删除状态")
                delete_btn.click(vn.remove_training_data, inputs=delete_content_input, outputs=[delete_output])
    with gr.Tab("训练数据验证"):
        with gr.Blocks():
            with gr.Row():
                question = gr.Textbox(label="问题", value="查询所有学生的姓名和对应的班级名称。")
            with gr.Row():
                btn_execute = gr.Button("执行")
            with gr.Row():
                # prompt = gr.Textbox(label="prompt")
                df_prompt = gr.DataFrame(label="prompt", interactive=True, headers=["role", "content"],
                                         column_widths=["20%", "80%"], wrap=True)
            with gr.Row():
                df_sql_prompt = gr.DataFrame(label="sql prompt")
            with gr.Row():
                df_ddl_prompt = gr.DataFrame(label="ddl prompt")
            with gr.Row():
                sql = gr.Textbox(label="SQL")
                is_valid = gr.Textbox(label="是否有效")
            with gr.Row():
                df = gr.DataFrame(label="执行结果")
            btn_execute.click(generate_sql, inputs=[question],
                              outputs=[df_prompt, df_sql_prompt, df_ddl_prompt, sql, df, is_valid])

    with gr.Tab("模型设定"):
        with gr.Blocks():
            with gr.Row():
                model_name = gr.Textbox(label="模型名称")
            with gr.Row():
                btn_save = gr.Button("保存")
            with gr.Row():
                txt_save_result = gr.Textbox("模型保存成功")
            btn_save.click(save_model, inputs=[model_name], outputs=[txt_save_result])
        pass

demo.queue()
if __name__ == "__main__":
    demo.launch(server_port=8080, inbrowser=False, show_api=False)
