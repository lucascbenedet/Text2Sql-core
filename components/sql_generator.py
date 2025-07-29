import os
from openai import OpenAI
from dotenv import load_dotenv

class SQLGenerator:
    def __init__(self, model="gpt-4o-mini"):
        load_dotenv()
        api_key = os.getenv("OPEN_AI_KEY")
        self.client = OpenAI(api_key=api_key)
        self.model = model

    def generate(self, question: str, schema_description: str) -> str:
        prompt = f'''Considering the database schema {schema_description}, 
            write an SQL query to answer the query: "{question}". 
            The generated queries must attribute an alias for 
            each column when is not used the column name. 
            In the answer, present only the SQL query without any formatting or line breaks as a string, 
            without the ";" character at the end and without the "\" character'''
        #prompt = f"Given the schema:\n{schema_description}\nTranslate the following question to SQL:\n{question}"
        completion = self.client.chat.completions.create(
            model=self.model,
            max_tokens=1000,
            temperature=0.0,
            messages=[{"role": "user", "content": prompt}]
        )
        return completion.choices[0].message.content.strip()