from vanna.qdrant import Qdrant_VectorStore
from qdrant_client import QdrantClient
from vanna.google import GoogleGeminiChat
import sqlalchemy as sa
from ..database_connector import DatabaseManager


class MyVanna(Qdrant_VectorStore, GoogleGeminiChat):

    def __init__(
        self,
        organization: str,
        db: DatabaseManager,
        client: QdrantClient,
        gemini_api_key: str,
        gemini_model: str = "gemini-1.5-flash",
    ):

        Qdrant_VectorStore.__init__(
            self,
            config={
                "client": client,
                "documentation_collection_name": f"{organization}_documentation",
                "ddl_collection_name": f"{organization}_ddl",
                "sql_collection_name": f"{organization}_sql",
            },
        )
        GoogleGeminiChat.__init__(
            self, config={"api_key": gemini_api_key, "model_name": gemini_model}
        )
        self.db = db
        self.engine = self.db.engine
        self.dialect = self.engine.dialect.name

    def log(self, message: str, title: str = "Vanna"):
        return

    def generic_connection(self):

        if self.dialect == "postgresql":
            self.connect_to_postgres(
                host=self.engine.url.host,
                dbname=self.engine.url.database,
                user=self.engine.url.username,
                password=self.engine.url.password,
                port=self.engine.url.port,
            )

    def generate_ddl(self):
        if self.dialect in (
            "PostgreSQL",
            "MySQL",
            "MariaDB",
            "SQLite",
            "Oracle",
            "SQLServer",
        ):
            from sqlalchemy.schema import CreateTable

            metadata = sa.MetaData()
            metadata.reflect(bind=self.engine, schema=self.db.schema)
            ddls = [
                str(CreateTable(table).compile(dialect=self.engine.dialect))
                for table in metadata.tables.values()
            ]
            for ddl in ddls:
                self.add_ddl(ddl)

    def start_documentation(self):
        information_schema = self.run_sql(
            f"SELECT * FROM INFORMATION_SCHEMA.COLUMNS WHERE table_schema = '{self.db.schema}'"
        )

        plan = self.get_training_plan_generic(information_schema)

        self.train(plan=plan)
        self.generate_ddl()
