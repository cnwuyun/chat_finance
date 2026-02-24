import os
from dotenv import load_dotenv, find_dotenv

# LLM
from langchain_openai import ChatOpenAI
from langchain_openai import AzureChatOpenAI

# Embedding
from langchain_community.embeddings import OllamaEmbeddings
from langchain_openai import AzureOpenAIEmbeddings
from langchain_community.embeddings import DashScopeEmbeddings

class MyLLM:

    def __init__(self):
        pass

    def get_openai_llm(self, model_name, api_key, base_url):
        llm = ChatOpenAI(
            api_key=api_key,  # 如果您没有配置环境变量，请在此处用您的API Key进行替换
            base_url=base_url,  # 填写DashScope base_url
            model=model_name
        )
        return llm

    def get_azure_model(self):
        llm = AzureChatOpenAI(
            azure_endpoint=os.environ["AZURE_OPENAI_ENDPOINT"],
            azure_deployment=os.environ["AZURE_OPENAI_DEPLOYMENT_NAME"],
            openai_api_version=os.environ["AZURE_OPENAI_API_VERSION"],
        )
        return llm

    def get_zhipu_model(self, model_name="glm-4"):
        api_key = os.environ.get("ZHIPU_API_KEY")
        llm = ChatOpenAI(
            api_key=api_key,  # 如果您没有配置环境变量，请在此处用您的API Key进行替换
            base_url="https://open.bigmodel.cn/api/paas/v4/",  # 填写DashScope base_url
            model=model_name
        )
        return llm

    # def get_qwen_model_72b(self, model_name="qwen2-72b-instruct"):
    #     api_key = os.environ.get("DASHSCOPE_API_KEY")
    #     llm = ChatOpenAI(
    #         api_key=api_key,  # 如果您没有配置环境变量，请在此处用您的API Key进行替换
    #
    #         base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",  # 填写DashScope base_url
    #         model=model_name, temperature=0
    #     )
    #     return llm
#https://python.langchain.com/docs/integrations/chat/tongyi/
    def get_qwen_model(self, model_name="qwen-plus"):
        api_key = os.environ.get("DASHSCOPE_API_KEY")
        llm = ChatOpenAI(
            api_key=api_key,  # 如果您没有配置环境变量，请在此处用您的API Key进行替换

            base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",  # 填写DashScope base_url
            model=model_name, temperature=0
        )
        return llm

    def get_deepseek_model(self, model_name="deepseek-chat"):
        api_key = os.environ.get("DEEPSEEK_API_KEY")
        base_url = "https://api.deepseek.com"
        model_openai = ChatOpenAI(model=model_name, api_key=api_key, base_url=base_url)
        return model_openai

        ######################################################################################################
    def get_DashScope_embeddings_model(self,model_name="text-embedding-v3"):
        embeddings = DashScopeEmbeddings(
            model=model_name, dashscope_api_key=os.environ.get("DASHSCOPE_API_KEY")
        )
        return embeddings