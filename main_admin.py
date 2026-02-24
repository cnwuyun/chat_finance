# 系统
import gradio as gr

# 共通
from common.LLM_call import generate_question_sql_by_data, generate_question_sql_by_table, generate_sql_question
# from common.Finance_DB_call import get_ddl, get_all_codes, get_all_organizations
from common.Work_DB_call import get_table_ddl, get_view_ddl

from common.my_config import MyConfig
from common.vanna_calls import setup_vanna

config = MyConfig()
vn = setup_vanna()

# 工作
from work.query_test import generate_sql
from work.add_vanna_data import show_table, train_sql_data, train_dll_data, select_dll_list, filter_train_use_data, \
    run_this_sql, select_json_data, save_sql_question, load_sql_question
from work.setting import load_llm, select_llm, delete_llm, save_model, test_model, use_llm, \
    get_selected_llm_id, get_all_models
from work.view_vanna import select_rag_list

with gr.Blocks(title="ChatFinanceTraining") as demo:
    gr.Markdown("""# ChatFinance Training""")

    with gr.Tab("ADD RAG Data"):
        with gr.Tab("Create RAG Data"):
            with gr.Row():
                with gr.Column():
                    with gr.Row():
                        btn_get_all_table_dll = gr.Button("Get DLL of tables")
                        btn_get_all_view_dll = gr.Button("Get DLL of views")
                    with gr.Row():
                        df_dll = gr.DataFrame(headers=["Name", "DDL"])
                with gr.Column():
                    txt_select_table_name = gr.Textbox(label="Selected Table", lines=1, value="")
                    txt_select_dll = gr.Textbox(label="Selected DLL", lines=3)
                    btn_train_dll = gr.Button("Train this DLL Data")
                    txt_work_result = gr.Textbox(label="Train Result")
            with gr.Row():
                txt_filter = gr.Textbox(label="Filter Condition", lines=1, interactive=True,
                                        value="")
                # value = "勘定科目='外注費' and 組織='東京'")

                # dropdown_code = gr.Dropdown(label="勘定科目", choices=get_all_codes(), value="外注費")
                # dropdown_organization = gr.Dropdown(label="组织", choices=get_all_organizations(), value="東京")
                btn_filter = gr.Button("Show data by this filter")
            with gr.Row():
                df_train_use_data = gr.DataFrame(show_copy_button=True)
            with gr.Row():
                txt_count = gr.Textbox(label="Count of generate", value="3")
                dropdown_llm = gr.Dropdown(label="LLM", choices=get_all_models(), value=get_selected_llm_id())
                btn_generate_by_data = gr.Button("The prompt of using table data to generate")
                btn_generate_by_table = gr.Button("The prompt of using table structure fo generate")
                btn_generate_sql_question = gr.Button("Generate question and sql by prompt")
            with gr.Row():
                txt_prompt = gr.Textbox(label="Prompt to generate", lines=3, interactive=True)
            with gr.Row():
                txt_json_result = gr.Textbox(label="Generated Json data", lines=20, interactive=True)
            with gr.Row():
                btn_show_table = gr.Button("Show to table")
                btn_temp_save = gr.Button("Temp save this Jason data")
                bnt_temp_read = gr.Button("Temp read last saved Jason data")
            with gr.Row():
                with gr.Column():
                    df_json_data = gr.DataFrame()
                with gr.Column():
                    txt_select_question = gr.Textbox(label="Selected question", lines=1, interactive=True)
                    txt_select_sql = gr.Textbox(label="Selected SQL", lines=1)
                    btn_run_sql = gr.Button("Execute SQL")
                    btn_save = gr.Button("Train this data")
                    btn_add_to_evaluate = gr.Button("Add to evaluate")
                    txt_run_result = gr.Textbox(label="Work Result")
            with gr.Row():
                df_sql_run_result = gr.DataFrame(label="Run SQL result")

            dropdown_llm.change(use_llm, inputs=[dropdown_llm], outputs=[])
            btn_temp_save.click(save_sql_question, inputs=[txt_json_result], outputs=[txt_run_result])
            bnt_temp_read.click(load_sql_question, inputs=[], outputs=[txt_json_result])
            df_json_data.select(fn=select_json_data, inputs=[df_json_data],
                                outputs=[txt_select_question, txt_select_sql])
            btn_run_sql.click(run_this_sql, inputs=[txt_select_sql], outputs=[df_sql_run_result])
            btn_filter.click(filter_train_use_data,
                             inputs=[txt_select_table_name, txt_filter],
                             outputs=[df_train_use_data])
            df_dll.select(fn=select_dll_list, inputs=[df_dll], outputs=[txt_select_dll, txt_select_table_name])
            btn_get_all_table_dll.click(get_table_ddl, inputs=[], outputs=[df_dll])
            btn_get_all_view_dll.click(get_view_ddl, inputs=[], outputs=[df_dll])
            btn_train_dll.click(vn.add_ddl, inputs=[txt_select_dll], outputs=[txt_work_result])
            btn_generate_by_data.click(generate_question_sql_by_data,
                                       inputs=[txt_count, txt_select_table_name, df_train_use_data],
                                       outputs=[txt_prompt])
            btn_generate_by_table.click(generate_question_sql_by_table,
                                        inputs=[txt_count, txt_select_table_name, txt_select_dll],
                                        outputs=[txt_prompt])
            btn_generate_sql_question.click(generate_sql_question,
                                            inputs=[txt_prompt], outputs=[txt_json_result])

            btn_show_table.click(show_table, inputs=[txt_json_result], outputs=[df_json_data])
            btn_save.click(train_sql_data, inputs=[txt_json_result], outputs=[txt_run_result])
            # btn_get_prompt.click(get_prompt, inputs=[txt_count], outputs=[txt_prompt])
            # btn_json_load.click(load_json, inputs=[], outputs=[txt_json_result])

        with gr.Tab("Add one train data"):
            with gr.Blocks():
                with gr.Row():
                    one_question = gr.Textbox(label="Question")
                with gr.Row():
                    one_sql = gr.Textbox(label="SQL", lines=5)
                with gr.Row():
                    btn_sql = gr.Button("Add SQL")

                with gr.Row():
                    one_ddl = gr.Textbox(label="DDL", lines=5)
                with gr.Row():
                    btn_ddl = gr.Button("Add DLL")
                with gr.Row():
                    one_doc = gr.Textbox(label="Document", lines=5)
                with gr.Row():
                    btn_doc = gr.Button("Add Doc")
                with gr.Row():
                    one_result = gr.Textbox(label="Work Result")

                btn_sql.click(vn.add_question_sql, inputs=[one_question, one_sql], outputs=[one_result])
                btn_ddl.click(vn.add_ddl, inputs=[one_ddl], outputs=[one_result])
                btn_doc.click(vn.add_documentation, inputs=[one_doc], outputs=[one_result])

    with gr.Tab("RAG Data List"):
        with gr.Row():
            load_rag_data_btn = gr.Button("Load data")
            export_to_excel_btn = gr.Button("Export to Excel")

        with gr.Row():
            df_rag_list = gr.Dataframe(label="Data in database",
                                       headers=["id", "question", "content", "training_data_type"],
                                       column_widths=["10%", "20%", "60%", "10%"], wrap=True)
        with gr.Row():
            delete_content_id = gr.Textbox(label="id")
            delete_btn = gr.Button("Delete this record")
        with gr.Row():
            delete_output = gr.Textbox(label="Work Result")

        delete_btn.click(vn.remove_training_data, inputs=delete_content_id, outputs=[delete_output])
        export_to_excel_btn.click(

        )
        load_rag_data_btn.click(vn.get_training_data, inputs=[], outputs=[df_rag_list])
        df_rag_list.select(fn=select_rag_list, inputs=[df_rag_list], outputs=[delete_content_id])

    with gr.Tab("Question Test"):
        with gr.Blocks():
            with gr.Row():
                # str_question1 = "４月の収益はどんな状況"
                # str_question2 = "４月の組織ごとの収益を教えて"
                test_question = gr.Textbox(label="Question", value="")
            with gr.Row():
                btn_execute = gr.Button("Execute")
            with gr.Row():
                # prompt = gr.Textbox(label="prompt")
                df_prompt = gr.DataFrame(label="prompt", interactive=True, headers=["role", "content"],
                                         column_widths=["20%", "80%"], wrap=True)
            with gr.Row():
                df_sql_prompt = gr.DataFrame(label="sql prompt")
            with gr.Row():
                df_ddl_prompt = gr.DataFrame(label="ddl prompt")
            with gr.Row():
                test_sql = gr.Textbox(label="SQL")
                is_valid = gr.Textbox(label="Correct SQL?")
                btn_train_this_question = gr.Button("Train this data")
                txt_train_data_add_result = gr.Textbox(label="Work result")
            with gr.Row():
                df_test_result = gr.DataFrame(label="Execute SQL result")
            btn_execute.click(generate_sql, inputs=[test_question],
                              outputs=[df_prompt, df_sql_prompt, df_ddl_prompt, test_sql, df_test_result, is_valid])
            btn_train_this_question.click(vn.add_question_sql, inputs=[test_question, test_sql],
                                          outputs=[txt_train_data_add_result])

    with gr.Tab("Evaluate System"):

        pass

    with gr.Tab("Setting"):
        with gr.Tab("LLM Setting"):
            with gr.Tab("LLM List"):
                with gr.Blocks():
                    with gr.Row():
                        df_llm = gr.DataFrame(label="LLM List",
                                              headers=["llm_id", "model_name", "api_key", "base_url"])

                    with gr.Row():
                        btn_update_llm = gr.Button("Load LLMs")
                        btn_use_llm = gr.Button("Use this LLM")
                        btn_delete_llm = gr.Button("Delete this LLM")

                    with gr.Row():
                        txt_selected_llm = gr.Textbox(label="Selected LLM ID", visible=True)
                        txt_list_result = gr.Textbox(label="Work Result")
                    btn_use_llm.click(fn=use_llm, inputs=txt_selected_llm, outputs=txt_list_result)
                    df_llm.select(
                        fn=select_llm, inputs=df_llm, outputs=txt_selected_llm)
                    btn_update_llm.click(fn=load_llm, inputs=None, outputs=df_llm)
                    btn_delete_llm.click(fn=delete_llm, inputs=txt_selected_llm, outputs=txt_list_result)
                    # btn_select_llm.click(fn=None, inputs=None, outputs=None)

            with gr.Tab("Add LLM"):
                with gr.Blocks():
                    with gr.Row():
                        model_name = gr.Textbox(label="Model Name")
                        api_key = gr.Textbox(label="API Key")
                        base_url = gr.Textbox(label="Base URL")
                        llm_type = gr.Radio(choices=config.llm_type, value=config.llm_type[0], label="LLM Type")
                    with gr.Row():
                        txt_question = gr.Textbox(label="Test Question")
                        gr.Examples(
                            examples=["你好，你是谁？", "今天是2023年10月6日，星期五，4天前是星期几，仅返回数字。"],
                            inputs=txt_question)
                    with gr.Row():
                        btn_test = gr.Button("Test")
                        btn_save = gr.Button("Save")
                    with gr.Row():
                        txt_add_result = gr.Textbox(label="Work result")

                    btn_save.click(fn=save_model, inputs=[model_name, api_key, base_url, llm_type],
                                   outputs=txt_add_result)
                    btn_test.click(fn=test_model, inputs=[model_name, api_key, base_url, llm_type, txt_question],
                                   outputs=txt_add_result)

demo.queue()
if __name__ == "__main__":
    demo.launch(server_port=8080, inbrowser=False, show_api=False)
    # demo.launch(server_name="0.0.0.0", server_port=8080, inbrowser=False, show_api=False)
