# -*- coding: utf-8 -*-

import requests
import pandas as pd
from requests.auth import HTTPBasicAuth
from typing import Union
from langchain_core.messages import AIMessage
from langchain_core.tools import tool
from typing import Literal
from dotenv import load_dotenv, find_dotenv

from langgraph.graph import StateGraph, MessagesState, START, END
from langgraph.prebuilt import ToolNode
from typing import Literal

from langgraph.prebuilt import ToolNode
import gradio as gr

import os
from langchain_openai import ChatOpenAI


_ = load_dotenv(find_dotenv())

global_question = ""

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
    # if name == "西日本営業部":
    #     return "2200"
    # if name == "マーケティング部":
    #     return "2300"
    return "0000"


def getAcount(name):
    if name == "売上":
        return "811100"
    if name == "原価":
        return "825100"
    return "000000"


def get_data_from_erp(oracle_url):
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

    #:param to_this_month_flag:「今月まで」を言ったらTrueを設定する、「今月まで」を言わなかったらFalseを設定する。
    #:param to_last_month_flag:「先月まで」を言ったらTrueを設定する、「先月まで」を言わなかったらFalseを設定する。

    # :param flag:フラグ　例えば：0,1,2 設定方法：「今月まで」を含んだら1を設定する、「先月まで」を含んだら2を設定する,以外の場合は0を設定する。


@tool
def get_ledger_balances(accounting_period: Union[str, None] = None,
                        account: Union[str, None] = None,
                        cost_center: Union[str, None] = None):
    """
    残高を取得する。売り上げを取得する。原価を取得する。

    :param accounting_period:会計期間 例えば：02-25,01-25
    :param account:勘定科目 例えば：売上、原価
    :param cost_center:西日本営業部,マーケティング部
    :return:
    """
    print("*" * 50)
    print("accounting_period:", accounting_period, "account:", account, "cost_center:", cost_center)
    print("*" * 50)
    if "今月まで" in global_question:
        flag = 1
    elif "先月まで" in global_question:
        flag = 2
    else:
        flag = 0

    print("flag:", flag)
    if accounting_period is None:
        return "会計期間を入力してください。"
    if account is None:
        return "勘定科目を入力してください。"
    if cost_center is None:
        return "組織を入力してください。"

    accountCombination = "403-40-" + getCostCenter(cost_center) + "-" + getAcount(account) + "-0000-000-00000-000"
    print("*" * 50)

    url_balance = url_domain + url_balance_head + "accountCombination=" + accountCombination + ",accountingPeriod=" + accounting_period
    print(url_balance)

    result = get_data_from_erp(url_balance)
    print("*" * 50)

    print(result)
    print("*" * 50)
    result1 = int(result[0]["EndingBalance"])
    result2 = int(result[0]["BeginningBalance"])
    result3 = int(result[0]["PeriodActivity"])
    print("*" * 50)
    print("result1:", result1, "result2:", result2, "result3:", result3)
    if flag == 1:
        return abs(result1)
    elif flag == 2:
        return abs(result2)

    else:
        return abs(result3)


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
        po_data = get_data_from_erp(url_po + p)
    else:
        po_data = get_data_from_erp(url_po)
    return po_data


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

tools = [get_purchase_orders, get_ledger_balances]
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
    system_prompt = """
    あなたは、ERPシステムのデータを検索するためのエージェントです。
    ERPシステムのデータは、会計期間、勘定科目、組織、仕入先、購入者、ステータスなどを検索できます。
    会計期間は、例えば「02-25,01-25」です。
    勘定科目は、例えば「売上」または「原価」です。
    組織は、例えば「西日本営業部」または「マーケティング部」です。
    """

    return app.invoke(
        {"messages": [("system", system_prompt), ("human", my_question)]})


from datetime import datetime


def bot(history):
    print("B" * 50)
    print(history)
    my_question = history[-1]["content"]
    # my_question = my_question + "今月は" + datetime.now().strftime("%Y年%m月")
    my_question = my_question + "今月は2025年3月"
    global global_question
    global_question = my_question
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
    str_question1 = "取消済購買オーダーを教えてください。"
    str_question2 = "西日本営業部の１月の売り上げを教えてください。"
    str_question3 = "西日本営業部の先月までの売り上げを出して。"
    str_question4 = "西日本営業部の今月までの売り上げを出して。"

    chat_input = gr.MultimodalTextbox(interactive=True,
                                      file_count="multiple",
                                      placeholder="Enter message or upload file...", show_label=False)
    # 给chat_input添加example
    examples = gr.Examples(
        examples=[str_question1, str_question2, str_question3, str_question4],
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
