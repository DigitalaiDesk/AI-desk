from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = "AI Desk Intelligence API"
    database_url: str = "postgresql+psycopg://postgres:postgres@localhost:5432/aidesk"
    qdrant_url: str = "http://localhost:6333"
    neo4j_uri: str = "bolt://localhost:7687"
    neo4j_user: str = "neo4j"
    neo4j_password: str = "neo4j"
    crawl_concurrency: int = 10
    crawl_rate_per_second: float = 2.0


settings = Settings()
