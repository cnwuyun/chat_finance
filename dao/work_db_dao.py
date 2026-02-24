import sqlite3
from common.my_config import MyConfig

config = MyConfig()


class Work_DB:
    def __init__(self, db_id=None, db_path=None, selected=None):
        self.db_id = db_id,
        self.db_path = db_path,
        self.selected = selected


class Work_DB_Dao:
    def __init__(self):
        """Initialize the DAO with the database path."""
        self.db_path = config.app_db_path
        # self._create_table()

    # def _create_table(self):
    #     """Ensure the llm table exists."""
    #     query = """
    #     CREATE TABLE IF NOT EXISTS llm (
    #         llm_id INTEGER NOT NULL PRIMARY KEY,
    #         model_name TEXT,
    #         api_key TEXT,
    #         base_url TEXT,
    #         selected REAL DEFAULT (False)
    #     );
    #     """
    #     with sqlite3.connect(self.db_path) as conn:
    #         conn.execute(query)

    def insert_db(self, llm):
        """Insert a new LLM record."""
        query = """
        INSERT INTO work_db (db_path, selected) 
        VALUES (?, ?);
        """
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute(query, (llm.model_name, llm.api_key, llm.base_url, llm.selected, llm.llm_type))
            llm.llm_id = cursor.lastrowid

    def get_all_dbs(self):
        """Retrieve all LLM records."""
        query = "SELECT * FROM work_db;"
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute(query)
            return [Work_DB(*row) for row in cursor.fetchall()]

    def get_db_by_id(self, db_id):
        """Retrieve an LLM by its ID."""
        query = "SELECT * FROM work_db WHERE db_id = ?;"
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute(query, (db_id,))
            row = cursor.fetchone()
            return Work_DB(*row) if row else None

    # def update_llm(self, llm):
    #     """Update an existing LLM record."""
    #     query = """
    #     UPDATE llm
    #     SET model_name = ?, api_key = ?, base_url = ?, selected = ?, llm_type = ?
    #     WHERE llm_id = ?;
    #     """
    #     with sqlite3.connect(self.db_path) as conn:
    #         conn.execute(query, (llm.model_name, llm.api_key, llm.base_url, llm.selected, llm.llm_type, llm.llm_id))

    def delete_db(self, llm_id):
        """Delete an LLM record by its ID."""
        query = "DELETE FROM work_db WHERE db_id = ?;"
        with sqlite3.connect(self.db_path) as conn:
            conn.execute(query, (llm_id,))

    def get_selected_db_id(self):
        """Retrieve an LLM by its ID."""
        query = "SELECT db_id FROM work_db WHERE selected = 1;"
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute(query)
            row = cursor.fetchone()
            return Work_DB(*row).db_id if row else None

    def set_selected_db_id(self, selected_db_id):
        """Update an existing LLM record."""
        query1 = """
        UPDATE work_db
        SET  selected = 0;
        """
        with sqlite3.connect(self.db_path) as conn:
            conn.execute(query1)

        query2 = """
        UPDATE work_db
        SET  selected = 1
        WHERE db_id = ?;
        """
        with sqlite3.connect(self.db_path) as conn:
            conn.execute(query2, (selected_db_id,))
