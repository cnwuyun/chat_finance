import configparser
import configparser
import yaml
import os

# 加载环境变量
from dotenv import load_dotenv, find_dotenv

_ = load_dotenv(find_dotenv())


# 常量定义
# SR_COLUMN =
# SR_COLUMN_UI =

# KNOWLEDGE_COLUMN =
# # KNOWLEDGE_COLUMN_UI=["id", "product", "catalog1", "catalog2", "question"]
# # KNOWLEDGE_COLUMN_UI =
# # KNOWLEDGE_COLUMN_UI_distance =
# # KNOWLEDGE_COLUMN_UI_distance_score =


class MyConfig:
    def __init__(self):
        # self.work_db_path = './work_db/finance_db.db'
        # self.vanna_db_path = "./vanna_db/finance"
        self.work_db_path = './work_db/score_db.db'
        self.vanna_db_path = "./vanna_db/score"

        self.app_db_path = './app_db/app_db.db'

        self.export_dir = "./export/"
        self.backup_dir = "./backup/"
        self.config_file = "config.yaml"
        self.temp_save_dir = "./doc/"

        self.embedding_api_base = "https://dashscope.aliyuncs.com/compatible-mode/v1"
        self.embedding_api_key = os.environ["DASHSCOPE_API_KEY"]
        self.embedding_model_name = "text-embedding-v3"
        self.llm_type = ["OpenAI适配模型", "Oracle模型"]

        self.load_config()

    def to_dict(self):
        return {
            'embedding_threshold': self.embedding_threshold,
            'embedding_top_k': self.embedding_top_k,
            'rerank_threshold': self.rerank_threshold,
            'rerank_top_k': self.rerank_top_k
        }

    def save_config(self):
        with open(self.config_file, 'w') as file:
            yaml.dump(self.to_dict(), file)

    def load_config(self):
        if os.path.exists(self.config_file):
            with open(self.config_file, 'r') as file:
                config_data = yaml.safe_load(file)
                if config_data:
                    self.embedding_threshold = float(config_data.get('embedding_threshold', self.embedding_threshold))
                    self.embedding_top_k = int(config_data.get('embedding_top_k', self.embedding_top_k))
                    self.rerank_threshold = float(config_data.get('rerank_threshold', self.rerank_threshold))
                    self.rerank_top_k = int(config_data.get('rerank_top_k', self.rerank_top_k))
