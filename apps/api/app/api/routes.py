from fastapi import APIRouter
from app.models.schemas import CrawlRequest, VisibilitySimulationRequest
from app.engines.crawler import CrawlerEngine
from app.engines.vector_indexing import VectorIndexingEngine
from app.engines.entity_extraction import EntityExtractionEngine
from app.engines.ai_visibility import AIVisibilityEngine

router = APIRouter()

@router.get("/health")
async def health() -> dict[str, str]:
    return {"status": "ok"}

@router.post("/crawl")
async def crawl(payload: CrawlRequest):
    return await CrawlerEngine().crawl_site(payload)

@router.post("/index")
async def index(payload: CrawlRequest):
    pages = await CrawlerEngine().crawl_site(payload)
    entities = EntityExtractionEngine().extract_entities_batch(pages["pages"])
    vectors = await VectorIndexingEngine().index_pages(pages["pages"])
    return {"entities": entities, "vectors": vectors}

@router.post("/simulate-visibility")
async def simulate(payload: VisibilitySimulationRequest):
    return await AIVisibilityEngine().simulate(payload)
