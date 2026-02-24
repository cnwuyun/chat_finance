from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
import pandas as pd

# 共通函数
from common.LLM import MyLLM
from common.LLM_Oracle import LLM_Oracle
from common.my_config import MyConfig
from common.vanna_calls import setup_vanna

config = MyConfig()
vn = setup_vanna()
my_llm = MyLLM()
llm_oracle = LLM_Oracle()

# 取得Dao信息
from dao.llm_dao import LLMDao, LLM

llm_dao = LLMDao()


def get_selected_llm():
    selected_llm = llm_dao.get_llm_by_id(llm_dao.get_selected_llm_id())
    if selected_llm.llm_type == config.llm_type[0]:
        model = my_llm.get_openai_llm(selected_llm.model_name, selected_llm.api_key, selected_llm.base_url)
    else:
        model = llm_oracle.get_LLM_Model(selected_llm.model_name, selected_llm.api_key, selected_llm.base_url)
    return model


def test_llm(model, question):
    prompt_str = question
    prompt = ChatPromptTemplate.from_template(prompt_str)
    output_parser = StrOutputParser()

    chain = prompt | model | output_parser

    result = chain.invoke({})
    return result


def generate_sql_question(prompt_str):
    prompt = ChatPromptTemplate.from_template(
        template=prompt_str,

    )
    output_parser = StrOutputParser()

    model = get_selected_llm()
    chain = prompt | model | output_parser
    prompt_return = prompt.invoke({})
    result1 = chain.invoke({})

    return result1


def generate_question_sql_by_table(count=10, table_name="", ddl=""):
    prompt_str = f"""
    テーブル名とテーブル構造に基づき、{count}個の質問とそれに応じたSQL文を生成してください。JSON形式でのデータ出力をご確認ください。
    JSONファイルには2つのフィールドが含まれます：`question`と`sql`。

    ### テーブル名：{table_name}
    ### テーブル構造：{ddl}
    """

    return prompt_str


def generate_question_sql_by_data(count=10, table_name="", df=None):
    if df is not None:
        try:
            # data = df.to_json(orient="records", force_ascii=False)
            data = df.to_csv(index=False, encoding='utf-8')
        except Exception as e:
            raise ValueError("Data conversion to JSON failed") from e
    else:
        raise ValueError("DataFrame is None")
    print("*" * 50)
    print(data)
    print("*" * 50)
    prompt_str = f"""
    テーブル名とテーブル内のデータに基づき、{count}個の質問とそれに応じたSQL文を生成してください。JSON形式でのデータ出力をご確認ください。
    JSONファイルには2つのフィールドが含まれます：`question`と`sql`。
    
    ### テーブル名：{table_name}
    ### テーブル内のデータ：
{data}
    """
    print(prompt_str)
    return prompt_str

#
# def generate_question_sql(count=10, dll="", df=None):
#     # Define your desired data structure.
#
#     # Set up a parser + inject instructions into the prompt template.
#     # parser = PydanticOutputParser(pydantic_object=question_sql)
#     prompt_str = """
#     请参照sqlite DDL,生成{count}个问题和相应的sql语句。请输出json格式数据。json文件有两个字段：question和sql。
#
#     ### sqlite DDL
#     {ddl}
#     """
#
#     prompt = ChatPromptTemplate.from_template(
#         template=prompt_str,
#         # input_variables=["count"],
#         # partial_variables={"format_instructions": parser.get_format_instructions()},
#     )
#     output_parser = StrOutputParser()
#     print("*" * 50)
#     print("prompt", prompt)
#     model = get_selected_llm()
#     chain = prompt | model | output_parser
#     # DDL_str = get_ddl()
#     prompt_return = prompt.invoke({"count": count, "ddl": dll})
#     result1 = chain.invoke({"count": count, "ddl": dll})
#     print("*" * 50)
#     print("result1", result1)
#     # result2 = parser.invoke(result1)
#
#     return result1, prompt_return
