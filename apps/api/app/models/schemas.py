from pydantic import BaseModel, AnyHttpUrl

class CrawlRequest(BaseModel):
    url: AnyHttpUrl
    max_pages: int = 25

class VisibilitySimulationRequest(BaseModel):
    prompt: str
    target_domain: str
    competitor_domains: list[str]
