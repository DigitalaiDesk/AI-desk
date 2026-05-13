from pydantic import BaseModel, HttpUrl


class CrawlCreate(BaseModel):
    base_url: HttpUrl
    max_pages: int = 300


class CrawlStatus(BaseModel):
    id: int
    base_url: str
    status: str
    max_pages: int
    stats: dict
