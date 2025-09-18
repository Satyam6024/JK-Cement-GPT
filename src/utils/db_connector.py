import sqlite3
import pandas as pd
import pyodbc
from typing import Dict, Any

class DatabaseConnector:
    def __init__(self):
        self.connections = {}
    
    def connect_sqlite(self, db_path: str) -> sqlite3.Connection:
        return sqlite3.connect(db_path)
    
    def connect_access(self, db_path: str) -> pyodbc.Connection:
        conn_str = f'DRIVER={{Microsoft Access Driver (*.mdb, *.accdb)}};DBQ={db_path};'
        return pyodbc.connect(conn_str)
    
    def query_database(self, db_path: str, query: str = None) -> pd.DataFrame:
        ext = db_path.split('.')[-1].lower()
        
        if ext in ['sqlite', 'sqlite3', 'db']:
            conn = self.connect_sqlite(db_path)
            if query is None:
                query = "SELECT name FROM sqlite_master WHERE type='table';"
            return pd.read_sql_query(query, conn)
        
        elif ext in ['accdb', 'mdb']:
            conn = self.connect_access(db_path)
            cursor = conn.cursor()
            if query is None:
                cursor.execute("SELECT Name FROM MSysObjects WHERE Type=1 AND Flags=0")
                return pd.DataFrame([row[0] for row in cursor.fetchall()], columns=['table_name'])
            return pd.read_sql(query, conn)