import requests
import pandas as pd
from requests.auth import HTTPBasicAuth
from typing import Union
from langchain_core.messages import AIMessage
from langchain_core.tools import tool
from typing import Literal
from dotenv import load_dotenv, find_dotenv

from langgraph.graph import StateGraph, MessagesState, START, END

from typing import Literal

from langgraph.graph import StateGraph, MessagesState
from langgraph.prebuilt import ToolNode
import gradio as gr

import os
from langchain_openai import ChatOpenAI
from langgraph.prebuilt import ToolNode

_ = load_dotenv(find_dotenv())

# API的URL
url_domain = "https://fa-eqje-dev12-saasfademo1.ds-fa.oraclepdemos.com/fscmRestApi/resources/11.13.18.05/"
url_po_head = "purchaseOrders?onlyData=True&limit=10&"
# url_fields = "fields=OrderNumber,SoldToLegalEntity,StatusCode,Status,ProcurementBU,RequisitioningBU,BillToBU,Revision,Buyer,Supplier,SupplierSite,SupplierContact,BillToLocation,Ordered,OrderedAmountBeforeAdjustments,CreditAmount,DiscountAmount,CurrencyCode,Currency,TotalTax,Total,Description,RequiredAcknowledgmentCode,RequiredAcknowledgment,PaymentTerms,Carrier,ShippingMethod,FreightTermsCode,FreightTerms,FOBCode,FOB,RequiresSignatureFlag,BuyerManagedTransportFlag,PayOnReceiptFlag,ConfirmingOrderFlag,CreationDate,CreatedBy,LastUpdateDate,LastUpdatedBy,ImportSourceCode,SupplierCommunicationMethodCode,OverrideB2BCommunicationFlag,SupplierCommunicationMethod,SupplierContactDisplayName,DocumentStyleId,ProgressPaymentFlag,PurchaseBasis,DocumentStyle,ConsignmentTermsFlag,OrderDate,DefaultTaxationCountryCode,DefaultTaxationCountry"
url_po_fields = "fields=OrderNumber,SoldToLegalEntity,Status,ProcurementBU,RequisitioningBU,BillToBU,Buyer,Supplier,SupplierSite,SupplierContact,BillToLocation"
url_po = url_domain + url_po_head + url_po_fields

url_balance_head = "ledgerBalances?fields=BeginningBalance,PeriodActivity,EndingBalance&onlyData=True&totalResults=true&finder=AccountBalanceFinder;currency=JPY,ledgerName=Japan Primary Ledger,mode=Summary,"

accountCombination = "403-40-0000-811100-0000-000-00000-000"
accountingPeriod = "02-25"

# 用户名和密码 casey.brown
username = "fin_impl"
password = "R2T9H%p*"

# 请求头部
headers = {
    "Accept": "application/json",
    "Content-Type": "application/json"
}


def getCostCenter(name):
    if name == "西日本営業部":
        return "2200"
    if name == "マーケティング部":
        return "2300"
    return "0000"


def getAcount(name):
    if name == "売上":
        return "811100"
    if name == "原価":
        return "825100"
    return "000000"


# # 发起GET请求并进行身份验证
# response = requests.get(url, headers=headers, auth=HTTPBasicAuth(username, password))

# # 检查请求是否成功
# if response.status_code == 200:
#     # 解析响应内容
#     data = response.json()

#     # 假设返回的数据是列表格式，提取其中的"items"字段（如果实际数据结构不同，需要调整）
#     if "items" in data:
#         items = data["items"]

#         # 将数据转换为DataFrame
#         df = pd.DataFrame(items)

#         # 将DataFrame保存到Excel文件
#         df.to_excel("purchaseOrders.xlsx", index=False)
#         print("数据已成功保存到 purchaseOrders.xlsx")
#     else:
#         print("没有找到'items'字段，响应结构可能不同")
# else:
#     print(f"请求失败，状态码: {response.status_code}")


def get_po(oracle_url):
    # 发起GET请求并进行身份验证
    response = requests.get(oracle_url, headers=headers, auth=HTTPBasicAuth(username, password))

    # 检查请求是否成功
    if response.status_code == 200:
        # 解析响应内容
        data = response.json()

        # 假设返回的数据是列表格式，提取其中的"items"字段（如果实际数据结构不同，需要调整）
        if "items" in data:
            items = data["items"]

            # 将数据转换为DataFrame
            # df = pd.DataFrame(items)
            return items
            # 将DataFrame保存到Excel文件
    else:
        return f"请求失败，状态码: {response.status_code}"


@tool
def get_ledger_balances(accounting_period: Union[str, None] = None, account: Union[str, None] = None,
                        cost_center: Union[str, None] = None):
    """
    残高を取得する

    :param accounting_period:会計期間 例えば：02-25,01-25
    :param account:勘定科目 例えば：売上、原価
    :param cost_center:西日本営業部,マーケティング部
    :return:
    """


@tool
def get_purchase_orders(buyer: Union[str, None] = None, supplier: Union[str, None] = None,
                        status: Union[str, None] = None):
    """
    購買オーダーを取得する

    :param buyer:
    :param supplier:
    :param status:取消済、未完了、承認待ち
    :return:
    """
    have_p = False
    p = "&q="
    print("*" * 50)
    print("buyer:", buyer, "supplier:", supplier, "status:", status)
    if buyer:
        have_p = True
        p += "Buyer=" + buyer
    if supplier:
        if have_p:
            p += ";"
        p += "Supplier=" + supplier
        have_p = True
    if status:
        if have_p:
            p += ";"
        p += "Status=" + status
        have_p = True
    if have_p:
        po_data = get_po(url_po + p)
    else:
        po_data = get_po(url_po)
    return po_data


# Status="取消済";Buyer="Miller, Saville";Supplier="Howell Engineering Inc."
# message_with_single_tool_call = AIMessage(
#     content="",
#     tool_calls=[
#         {
#             "name": "get_purchase_orders",
#             "args": {"buyer": "Miller, Saville", "supplier": "Howell Engineering Inc.", "status": "取消済"},
#             "id": "tool_call_id",
#             "type": "tool_call",
#         }
#     ],
# )
#
# result = tool_node.invoke({"messages": [message_with_single_tool_call]})

# print(result)
#         Status="取消済";Buyer="Miller, Saville";Supplier="Howell Engineering Inc."
#         &q=Status="取消済";Buyer="Miller, Saville";Supplier="Howell Engineering Inc."
# fastapi dev 04_PO.py

def should_continue(state: MessagesState):
    messages = state["messages"]
    last_message = messages[-1]
    if last_message.tool_calls:
        return "tools"
    return END


model_name = "qwen2.5-72b-instruct"
api_key = os.environ.get("DASHSCOPE_API_KEY")
llm = ChatOpenAI(
    api_key=api_key,  # 如果您没有配置环境变量，请在此处用您的API Key进行替换

    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",  # 填写DashScope base_url
    model=model_name, temperature=0
)

tools = [get_purchase_orders]
tool_node = ToolNode(tools)

model_with_tools = llm.bind_tools(tools)


def call_model(state: MessagesState):
    messages = state["messages"]
    response = model_with_tools.invoke(messages)
    return {"messages": [response]}


def get_response(my_question):
    workflow = StateGraph(MessagesState)

    # Define the two nodes we will cycle between
    workflow.add_node("agent", call_model)
    workflow.add_node("tools", tool_node)

    workflow.add_edge(START, "agent")
    workflow.add_conditional_edges("agent", should_continue, ["tools", END])
    workflow.add_edge("tools", "agent")

    app = workflow.compile()
    return app.invoke({"messages": [("human", my_question)]})


# from IPython.display import Image, display
#
# try:
#     display(Image(graph.get_graph().draw_mermaid_png()))
# except Exception:
#     # This requires some extra dependencies and is optional
#     pass
# https://langchain-ai.github.io/langgraph/how-tos/tool-calling/#setup

# example with a single tool call
#         &q=Status="取消済";Buyer="Miller, Saville";Supplier="Howell Engineering Inc."

# for chunk in app.stream(
#         {"messages": [("human", "取消済購買オーダーを教えてください。")]}, stream_mode="values"
# ):
#     chunk["messages"][-1].pretty_print()


str_question1 = "取消済購買オーダーを教えてください。"
str_question2 = "２月、西日本営業部の売り上げを教えてください。"

import datetime


def bot(history):
    print("B" * 50)
    print(history)
    my_question = history[-1]["content"]
    my_question = my_question + "今月は" + datetime.datetime.now().strftime("%Y年%m月")
    print("问题是：", my_question)

    print("2" * 50)
    content = get_response(my_question)
    print("回答是：", content["messages"][-1].content)
    print("2" * 50)
    # content="已经回答"
    msg_fig = {"role": "assistant", "content": ""}
    msg_fig["content"] = content["messages"][-1].content  # type: ignore
    history.append(msg_fig)
    return history


def add_message(history, message):
    # print("A" * 50)
    print(message)

    for x in message["files"]:
        history.append({"role": "user", "content": {"path": x}})
    if message["text"] is not None:
        history.append({"role": "user", "content": message["text"]})
    return history, gr.MultimodalTextbox(value=None, interactive=False)


with gr.Blocks(fill_height=True, title="Chat Finance") as demo:
    gr.Markdown("""# Chat Finance""")
    chatbot = gr.Chatbot(
        elem_id="chatbot",
        type="messages",
        bubble_full_width=False,
        scale=1,
        # examples=[{"text": "現在の収益は、どんな状況"},
        #           {"text": "組織ごとの収益を教えて"}],
        show_copy_button=True,
        avatar_images=(
            os.path.join("pic", "manager.svg"),  # os.path.join("files", "avatar.png"),
            os.path.join("pic", "assistant.svg"),
        ),
    )

    chat_input = gr.MultimodalTextbox(interactive=True,
                                      file_count="multiple",
                                      placeholder="Enter message or upload file...", show_label=False)
    # 给chat_input添加example
    examples = gr.Examples(
        examples=[str_question1],
        inputs=[chat_input],
    )
    response_type = "txt_file"
    chat_msg = chat_input.submit(
        add_message, [chatbot, chat_input], [chatbot, chat_input]
    )
    bot_msg = chat_msg.then(
        bot, chatbot, chatbot, api_name="bot_response"
    )
    bot_msg.then(lambda: gr.MultimodalTextbox(interactive=True), None, [chat_input])

if __name__ == "__main__":
    demo.launch()
