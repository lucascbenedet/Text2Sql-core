import pandas as pd
import json
from components.database_connector import DatabaseManager
import sqlglot
from components.vanna.vanna_manager import MyVanna
from pandas.testing import assert_frame_equal


class TestManager:
    def __init__(self, test_cases_path: str, database: DatabaseManager, model_client):
        self.test_cases_path = test_cases_path
        self.cases = self.load_test_cases()
        self.database = database
        self.model_client = model_client
        self.prompt_complement = " If necessary, use the appropriate SQL window function, as well as the WITH clause for the main query."

    def load_test_cases(self):
        with open(self.test_cases_path, "r", encoding="utf-8") as f:
            cases = json.load(f)

        return cases

    def get_case_prompt(self, case):
        prompt = case["prompt"]
        prompt = prompt.strip()
        prompt += self.prompt_complement
        return prompt

    def get_case_expected_sql(self, case):
        expected_sql = case["expected_sql"]
        return expected_sql

    def get_case_expected_result(self, case):
        expected_result = pd.DataFrame(case["expected_result"])
        return expected_result

    def compare_results(self, df_gen, df_exp):

        try:
            assert_frame_equal(df_gen, df_exp, check_names=True)
            return True
        except AssertionError as e:
            return str(e)

    def format_sql(self, sql: str):
        return sqlglot.transpile(sql, pretty=False)[0]

    def compare_sql(self, expected_sql: str, generated_sql: str):
        expected_sql_formated = self.format_sql(expected_sql)
        generated_sql_formated = self.format_sql(generated_sql)

        comparison = expected_sql_formated == generated_sql_formated
        if not comparison:
            return f"SQLs are not equal:\n\nExpected:\n{expected_sql_formated}\n\nGenerated:\n{generated_sql_formated}"
        return comparison

    def start_model(self):
        if isinstance(self.model_client, MyVanna):
            self.model_client.generic_connection()
            # self.model_client.start_documentation()
