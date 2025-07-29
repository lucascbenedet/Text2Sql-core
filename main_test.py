from tests.test_manager import TestManager
import pandas as pd
from components.database_connector import DatabaseManager
from components.vanna.vanna_manager import MyVanna
from qdrant_client import QdrantClient
from settings import VECTOR_STORE_URL, API_KEY, MODEL


def main():
    client = QdrantClient(url=VECTOR_STORE_URL)
    input_path = "tests/cases/postgres_test_cases_with_results.json"

    with DatabaseManager() as db:
        model = MyVanna(
            client=client,
            db=db,
            organization="test",
            gemini_api_key=API_KEY,
            gemini_model=MODEL,
        )

        tester = TestManager(input_path, db, model_client=model)
        tester.start_model()
        for case in tester.cases:

            generated_sql = model.generate_sql(tester.get_case_prompt(case))
            expected_sql = tester.get_case_expected_sql(case)

            print(tester.compare_sql(expected_sql, generated_sql))
            print("\n")
            expected_df = db.run_query(tester.format_sql(expected_sql))
            generated_df = db.run_query(tester.format_sql(generated_sql))

            print(expected_df)
            print(generated_df)

            print("\n")
            diffs = tester.compare_results(generated_df, expected_df)
            print(diffs)
            return


if __name__ == "__main__":
    main()
