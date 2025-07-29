from components.schema_handler import SchemaHandler
from components.query_parser import QueryParser
from components.sql_generator import SQLGenerator
from components.database_executor import DatabaseExecutor
from typing import List, Dict, Any
import pandas as pd

class TextToSQLPipeline:
    def __init__(self, model: str = "gpt-4o-mini"):
        #self.schema_handler = SchemaHandler(json_data)
        self.parser = QueryParser()
        self.generator = SQLGenerator(model)
        #self.conn = self.schema_handler.create_memory_table()
        self.executor = DatabaseExecutor()
        self.executor.verify_database()

    def run(self, question: str, schema_description: str) -> pd.DataFrame:
        parsed_question = self.parser.parse(question)
        sql_query = self.generator.generate(parsed_question, schema_description)
        print(f"Generated SQL:\n{sql_query}")
        return self.executor.run_query(sql_query)