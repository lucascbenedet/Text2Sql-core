import sqlalchemy as sa
import pandas as pd


class DatabaseManager:

    _metadata = sa.MetaData()

    def __init__(self) -> None:
        from settings import DATABASE

        self.connection_data = DATABASE
        self.schema = DATABASE.get("schema")
        self.cursor = None

    def _build_connection_url(self):
        if self.connection_data:
            return sa.URL.create(
                self.connection_data.get("dialect"),
                username=self.connection_data.get("user"),
                password=self.connection_data.get("password"),
                host=self.connection_data.get("host"),
                port=self.connection_data.get("port"),
                database=self.connection_data.get("database"),
            )

    def _get_engine(self):
        url = self._build_connection_url()

        try:
            engine = sa.create_engine(
                url,
                pool_size=10,
                max_overflow=20,
                pool_pre_ping=True,
                pool_recycle=1800,
            )
        except Exception as error:
            raise Exception(
                f"Conexão não suportada, verifique as configurações da conexão {error}"
            )
        return engine

    def __enter__(self):
        self.engine = self._get_engine()
        try:
            self.cursor = self.engine.connect()
        except Exception as error:
            raise Exception("Connection error: ", str(error))
        self.inspector = sa.inspect(self.engine)

        return self

    def __exit__(self, exc_type, exc_value, traceback):
        if not exc_type:
            self.cursor.commit()
        else:
            self.cursor.rollback()

        self.cursor.close()

    def run_query(self, query: str) -> pd.DataFrame:
        df = pd.read_sql(query, self.engine)
        return df
