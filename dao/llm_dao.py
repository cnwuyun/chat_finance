import sqlite3
from common.my_config import MyConfig

config = MyConfig()


class LLM:
    def __init__(self, llm_id=None, model_name=None, api_key=None, base_url=None, selected=False, llm_type=None):
        self.llm_id = llm_id
        self.model_name = model_name
        self.api_key = api_key
        self.base_url = base_url
        self.selected = selected
        self.llm_type = llm_type


class LLMDao:
    def __init__(self):
        """Initialize the DAO with the database path."""
        self.db_path = config.app_db_path
        # self._create_table()

    def _create_table(self):
        """Ensure the llm table exists."""
        query = """
        CREATE TABLE IF NOT EXISTS llm (
            llm_id INTEGER NOT NULL PRIMARY KEY,
            model_name TEXT,
            api_key TEXT,
            base_url TEXT,
            selected REAL DEFAULT (False)
        );
        """
        with sqlite3.connect(self.db_path) as conn:
            conn.execute(query)

    def insert_llm(self, llm):
        """Insert a new LLM record."""
        query = """
        INSERT INTO llm (model_name, api_key, base_url, selected,llm_type) 
        VALUES (?, ?, ?, ?);
        """
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute(query, (llm.model_name, llm.api_key, llm.base_url, llm.selected, llm.llm_type))
            llm.llm_id = cursor.lastrowid

    def get_all_llms(self):
        """Retrieve all LLM records."""
        query = "SELECT * FROM llm;"
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute(query)
            return [LLM(*row) for row in cursor.fetchall()]

    def get_llm_by_id(self, llm_id):
        """Retrieve an LLM by its ID."""
        query = "SELECT * FROM llm WHERE llm_id = ?;"
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute(query, (llm_id,))
            row = cursor.fetchone()
            return LLM(*row) if row else None

    def update_llm(self, llm):
        """Update an existing LLM record."""
        query = """
        UPDATE llm
        SET model_name = ?, api_key = ?, base_url = ?, selected = ?, llm_type = ?
        WHERE llm_id = ?;
        """
        with sqlite3.connect(self.db_path) as conn:
            conn.execute(query, (llm.model_name, llm.api_key, llm.base_url, llm.selected, llm.llm_type, llm.llm_id))

    def delete_llm(self, llm_id):
        """Delete an LLM record by its ID."""
        query = "DELETE FROM llm WHERE llm_id = ?;"
        with sqlite3.connect(self.db_path) as conn:
            conn.execute(query, (llm_id,))

    def get_selected_llm_id(self):
        """Retrieve an LLM by its ID."""
        query = "SELECT llm_id FROM llm WHERE selected = 1;"
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute(query)
            row = cursor.fetchone()
            return LLM(*row).llm_id if row else None

    def set_selected_llm_id(self, selected_llm_id):
        """Update an existing LLM record."""
        query1 = """
        UPDATE llm
        SET  selected = 0;
        """
        with sqlite3.connect(self.db_path) as conn:
            conn.execute(query1)

        query2 = """
        UPDATE llm
        SET  selected = 1
        WHERE llm_id = ?;
        """
        with sqlite3.connect(self.db_path) as conn:
            conn.execute(query2, (selected_llm_id,))
