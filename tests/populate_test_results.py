import json
import pandas as pd
from sqlalchemy import create_engine


def main():
    input_path = "/home/etopocart/Desktop/Text2SQL-core/tests/postgres_test_cases.json"
    output_path = input_path.replace(".json", "_with_results.json")

    connection_string = "postgresql://postgres:123@localhost:5432/chinook"
    engine = create_engine(connection_string)

    with open(input_path, "r", encoding="utf-8") as f:
        cases = json.load(f)

    for case in cases:
        sql = case.get("expected_sql", "").strip()
        if not sql:
            print(f"Ignorado (sem SQL): {case['prompt']}")
            continue

        df = pd.read_sql(sql, engine)

        case["expected_result"] = df.to_dict(orient="records")

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(cases, f, indent=2, ensure_ascii=False, default=str)

    print(f"JSON atualizado com respostas em: {output_path}")


if __name__ == "__main__":
    main()
