import gradio as gr
import pandas as pd

# 共通函数

from common.my_config import MyConfig
from common.vanna_calls import setup_vanna

config = MyConfig()

vn = setup_vanna()


def select_rag_list(evt: gr.SelectData, df: pd.DataFrame):
    selected_index = evt.index[0]  # 获取选中行的索引
    selected_row = df.iloc[selected_index]  # 获取选中行的所有数据
    return selected_row['id']
