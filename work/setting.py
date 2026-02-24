import pandas as pd
import gradio as gr

# 共通函数
from common.LLM import MyLLM
from common.my_config import MyConfig
from common.vanna_calls import setup_vanna
from common.LLM_call import test_llm
from common.LLM_Oracle import LLM_Oracle

config = MyConfig()
vn = setup_vanna()

# 取得Dao信息
from dao.llm_dao import LLMDao, LLM
llm_dao = LLMDao()


####################### 大模型设定 #######################

def select_llm(evt: gr.SelectData, df: pd.DataFrame):
    selected_index = evt.index[0]  # 获取选中行的索引
    selected_row = df.iloc[selected_index]  # 获取选中行的所有数据
    return selected_row['llm_id']


def get_selected_llm_id():
    result = llm_dao.get_selected_llm_id()
    result = result if result is not None else ""
    return result


def use_llm(llm_id):
    llm_dao.set_selected_llm_id(llm_id)
    return "Setting successful!"


def load_llm():
    objects = llm_dao.get_all_llms()
    # print("*" * 50)
    # print(data)
    # print("*" * 50)
    if len(objects) == 0:
        return None
    df = pd.DataFrame.from_records([obj.__dict__ for obj in objects])

    # df = pd.DataFrame(data, columns=["llm_id", "model_name", "api_key", "base_url", "selected"])
    df2 = df[["llm_id", "model_name", "api_key", "base_url"]]
    return df2


def get_all_models():
    objects = llm_dao.get_all_llms()
    return [(obj.model_name, obj.llm_id) for obj in objects]


def delete_llm(llm_id):
    print(llm_id)


def save_model(model_name, api_key, base_url, llm_type):
    llm = LLM()
    llm.model_name = model_name
    llm.api_key = api_key
    llm.base_url = base_url
    llm.llm_type = llm_type
    llm_dao.insert_llm(llm)
    return "Save successful!"


def test_model(model_name, api_key, base_url, question, llm_type):
    # llm = LLM()
    # llm.model_name = model_name
    # llm.api_key = api_key
    # llm.base_url = base_url
    if llm_type == config.llm_type[0]:
        my_llm = MyLLM()
        model = my_llm.get_openai_llm(model_name, api_key, base_url)
    else:
        oracle_llm = LLM_Oracle()
        model = oracle_llm.get_LLM_Model(model_name, api_key, base_url)

    result = test_llm(model, question)

    return result
