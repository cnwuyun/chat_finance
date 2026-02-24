import gradio as gr
from common import vanna_calls as calls
import os


class cache_data:
    def __init__(self):
        self.sql = ""
        self.df = None
        self.question = ""
        self.fig = None
        self.summary = ""


my_cache = cache_data()


def add_message(history, message):
    print("1" * 50)
    print(message)

    for x in message["files"]:
        history.append({"role": "user", "content": {"path": x}})
    if message["text"] is not None:
        history.append({"role": "user", "content": message["text"]})
    return history, gr.MultimodalTextbox(value=None, interactive=False)


def append_example_message(x: gr.SelectData, history):
    print(x.value)
    msg = x.value["text"]
    print(x.value["text"])
    history.append({"role": "user", "content": msg})

    print("H" * 50)
    print(history)
    return history


def dataframe_to_html(df):
    return df.to_html(index=False, classes="dataframe-table", border=0)


str_question1 = "2023会計年度、東京のすべての勘定科目の1月実績残高を表示してください。"
str_question2 = "2023会計年度で、東京の資金収益の1月実績残高はいくらですか？"

str_bar_graph1 = "このデータを横棒グラフにしてみて"
str_bar_graph2 = "このデータを縦棒グラフにして"

str_pie_graph = "このデータを円グラフにしてみて"
str_ppt = "このグラフをパワーポイントファイルにして"

# str_none = "非表示"

str_input_question = "質問を入力してください。"

str_order_asc = "、データは１件以上の場合、昇順表示"
str_order_desc = "、データは１件以上の場合、降順表示"

str_asc = "昇順"


# def download_pptx(fig, summary):
#      =


# def check_intent(question):
#     if question.startswith(str_bargraph1):
#         return str_bargraph1


def show_chart(my_question, sql, df, graph_type=None):
    # if calls.should_generate_chart_cached(question=my_question, sql=sql, df=df):
    str_color = ". plot background color is white, paper background color is gray, graph is blue."
    if graph_type == str_bar_graph1:
        my_question = my_question + "、" + str_bar_graph1 + str_color
    elif graph_type == str_bar_graph2:
        my_question = my_question + "、" + str_bar_graph2 + str_color
    elif graph_type == str_pie_graph:
        my_question = my_question + "、" + str_pie_graph + "、plot background color is gray, paper background color is gray"
    else:
        return
    print("#" * 50)
    print("final question: ", my_question)
    code = calls.generate_plotly_code_cached(question=my_question, sql=sql, df=df)
    print("#" * 50)
    print("code: ", code)

    if code is not None and code != "":

        fig = calls.generate_plot_cached(code=code, df=df)
        # fig.update_layout(title=dict(text="組織ごとの収益"))
        # if graph_type == str_bar_graph2:
        #     fig.update_layout(
        #         xaxis=dict(title=dict(text="組織")),
        #         yaxis=dict(tickvals=[0, 200000000, 400000000, 600000000, 800000000, 1000000000, 1200000000],
        #                    ticktext=["0", "2億", "4億", "6億", "8億", "10億", "12億"],
        #                    title=dict(text="収益")))
        #
        # elif graph_type == str_bar_graph1:
        #     fig.update_layout(
        #         yaxis=dict(title=dict(text="組織")),
        #         xaxis=dict(tickvals=[0, 200000000, 400000000, 600000000, 800000000, 1000000000, 1200000000],
        #                    ticktext=["0", "2億", "4億", "6億", "8億", "10億", "12億"],
        #                    title=dict(text="収益")))
        # else:
        #     pass

        print("#" * 50)
        print("fig: ", fig)
        # if fig is not None:
        #     assistant_message_chart.plotly_chart(fig)
        # else:
        #     assistant_message_chart.error("I couldn't generate a chart")

        return fig

def check_intent(question):
    if question.startswith(str_bar_graph1):
        return str_bar_graph1
    elif question.startswith(str_bar_graph2):
        return str_bar_graph2
    elif question.startswith(str_pie_graph):
        return str_pie_graph
    elif question.startswith(str_ppt):
        return str_ppt
    else:
        return None
def bot(history):
    print("2" * 50)
    print(history)
    my_question = history[-1]["content"]
    # intent check
    intent = check_intent(question=my_question)

    if intent == str_bar_graph1 or intent == str_bar_graph2 or intent == str_pie_graph:
        graph_type = intent
        fig = show_chart(my_cache.question, my_cache.sql, my_cache.df, graph_type)
        my_cache.fig = fig
        content = gr.Plot(fig)
        #
        # print(my_question, sql, df)
        # fig = show_chart(my_question, sql, df)
        msg_fig = {"role": "assistant", "content": ""}
        msg_fig["content"] = content  # type: ignore
        history.append(msg_fig)
        return history

    if intent == str_ppt:
        path = os.path.join("ppt", "output_ppt.pptx")
        calls.save_ppt_cached(my_cache.fig, my_cache.summary)

        html_ppt = f"""<div style="display: flex; gap: 5px;">
                        <a href="{path}" download="財務レポート.pptx">PPTダウンロード</a>
                    </div>
                    """

        # content = {"path": os.path.join("ppt", "output_ppt.pptx"), "alt_text": "description"}
        content = gr.HTML(html_ppt)

        msg_ppt = {"role": "assistant", "content": ""}
        msg_ppt["content"] = content  # type: ignore
        history.append(msg_ppt)
        return history

    # generate sql
    my_cache.question = my_question

    order_str = str_order_asc  # str_order_desc

    my_question = my_question + order_str
    print("13" * 50)
    print("final question: ", my_question)
    print("13" * 50)
    sql_generated = calls.generate_sql_cached(question=my_question)
    sql=sql_generated[0]
    print("13" * 50)

    my_cache.sql = sql
    if sql:
        if calls.is_sql_valid_cached(sql=sql):
            df = calls.run_sql_cached(sql=sql)
            my_cache.df = df
            print("*" * 50)

            content = gr.HTML(dataframe_to_html(df))
            #
            # print(my_question, sql, df)
            # fig = show_chart(my_question, sql, df)
            msg_df = {"role": "assistant", "content": ""}
            msg_df["content"] = content  # type: ignore
            history.append(msg_df)

            msg_summary = {"role": "assistant", "content": ""}

            if df is not None:
                if intent == str_question1:
                    my_question = my_question + ""
                msg_summary["content"] = calls.generate_summary_cached(question=my_question, df=df)
                my_cache.summary = msg_summary["content"]
            else:
                msg_summary["content"] = "There is no data in the database"
            history.append(msg_summary)
            return history

    msg_no_data = {"role": "assistant", "content": ""}
    msg_no_data["content"] = "can't answer"  # type: ignore
    history.append(msg_no_data)
    return history


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
        examples=[str_question1, str_question2, str_bar_graph1, str_bar_graph2, str_pie_graph, str_ppt],
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
