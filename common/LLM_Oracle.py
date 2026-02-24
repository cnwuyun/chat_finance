import os
from dotenv import load_dotenv, find_dotenv


# Oracle
from langchain_community.chat_models.oci_generative_ai import ChatOCIGenAI
from langchain_community.embeddings import OCIGenAIEmbeddings


class LLM_Oracle:
    def __init__(self):
        _ = load_dotenv(find_dotenv())
        pass

    # cohere.command-r-plus-08-2024
    # cohere.command-r-08-2024
    # cohere.command-r-16k
    # cohere.command-r-plus
    # https://docs.oracle.com/en-us/iaas/Content/generative-ai/chat-models.htm
    def get_LLM_Model(self, model_id, api_key, base_url):
        chat = ChatOCIGenAI(
            model_id=model_id,
            service_endpoint=base_url,
            compartment_id=api_key,
            model_kwargs={"temperature": 0, "max_tokens": 2000},
        )
        return chat

    def get_embeddings_model(self, model_name="cohere.embed-multilingual-light-v3.0"):
        # use default authN method API-key
        embeddings = OCIGenAIEmbeddings(
            model_id=model_name,
            service_endpoint="https://inference.generativeai.us-chicago-1.oci.oraclecloud.com",
            compartment_id=os.environ["MY_COMPARTMENT_OCID"],
        )
        return embeddings
