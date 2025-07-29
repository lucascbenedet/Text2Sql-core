import sqlite3
from typing import List, Dict, Any

class SchemaHandler:
    def __init__(self, data: List[Dict[str, Any]], table_name: str = "data"):
        self.data = data
        self.table_name = table_name
        self.conn = None

    def create_memory_table(self) -> sqlite3.Connection:
        if not isinstance(self.data, list) or not all(isinstance(item, dict) for item in self.data):
            raise ValueError("Input data must be a list of dictionaries.")

        sample = self.data[0]
        column_definitions = []

        for key, value in sample.items():
            if isinstance(value, int):
                column_type = "INTEGER"
            elif isinstance(value, float):
                column_type = "REAL"
            else:
                column_type = "TEXT"
            column_definitions.append(f'"{key}" {column_type}')

        self.conn = sqlite3.connect(":memory:")
        cursor = self.conn.cursor()

        columns_sql = ", ".join(column_definitions)
        sql_command = f'CREATE TABLE "{self.table_name}" ({columns_sql})'
        cursor.execute(sql_command)

        column_names = list(sample.keys())
        placeholders = ", ".join("?" for _ in column_names)
        insert_sql = f'INSERT INTO "{self.table_name}" ({", ".join(column_names)}) VALUES ({placeholders})'

        for record in self.data:
            values = tuple(record.get(col) for col in column_names)
            cursor.execute(insert_sql, values)

        self.conn.commit()
        return self.conn