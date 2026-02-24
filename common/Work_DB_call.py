import sqlite3
import pandas as pd

from common.my_config import MyConfig

config = MyConfig()

db_name = config.work_db_path


def get_dropdown_list(script):
    # Connect to the SQLite database
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

    cursor.execute(script)
    results = cursor.fetchall()
    list_return = []
    for result in results:
        list_return.append(result[0])
    return list_return

#
# def get_all_organizations():
#     script = """
#         SELECT distinct(組織) from 残高
#     """
#     result = get_dropdown_list(script)
#     result.insert(0, "全て")
#     print("result:", result)
#     return result
#
#
# def get_all_codes():
#     script = """
#         SELECT distinct(勘定科目) from 残高
#     """
#     result = get_dropdown_list(script)
#     result.insert(0, "全て")
#     print("result:", result)
#     return result


def get_view_ddl():
    # Connect to the SQLite database
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

    script = """
        SELECT name, sql 
        FROM sqlite_master 
        WHERE type='view' 
        ORDER BY name;
    """

    cursor.execute(script)
    results = cursor.fetchall()

    # Create a DataFrame
    df = pd.DataFrame(results, columns=['Name', 'DDL'])

    conn.close()

    # Print the DataFrame
    print(df)
    return df

def get_table_ddl():
    # Connect to the SQLite database
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

    script = """
        SELECT name, sql 
        FROM sqlite_master 
        WHERE type='table' 
        ORDER BY name;
    """

    cursor.execute(script)
    results = cursor.fetchall()

    # Create a DataFrame
    df = pd.DataFrame(results, columns=['Name', 'DDL'])

    conn.close()

    # Print the DataFrame
    print(df)
    return df


def run_sql(sql):
    # Connect to the SQLite database
    conn = sqlite3.connect(db_name)
    # cursor = conn.cursor()
    #
    # cursor.execute(sql)
    # results = cursor.fetchall()
    #
    # conn.close()
    #
    # # Print the Da
    # return results
# 3. 执行查询并将结果加载到 DataFrame
    df = pd.read_sql_query(sql, conn)

    # 4. 查看 DataFrame 内容
    print(df.head())
    return df