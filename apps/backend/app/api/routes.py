import asyncio
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.session import SessionLocal
from app.models.crawl import CrawlRun, CrawledPage
from app.schemas.crawl import CrawlCreate
from app.services.crawler import CrawlService
from app.services.embeddings import EmbeddingService
from app.services.entities import EntityService
from app.services.scoring import aeo_score, geo_score, seo_score, visibility_simulation

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post('/crawls')
def create_crawl(payload: CrawlCreate, db: Session = Depends(get_db)):
    crawl = CrawlRun(base_url=str(payload.base_url), max_pages=payload.max_pages)
    db.add(crawl); db.commit(); db.refresh(crawl)
    asyncio.create_task(CrawlService(db).run_crawl(crawl.id))
    return {"id": crawl.id, "status": crawl.status}

@router.get('/crawls/{crawl_id}')
def crawl_status(crawl_id: int, db: Session = Depends(get_db)):
    crawl = db.get(CrawlRun, crawl_id)
    if not crawl: raise HTTPException(404, 'crawl not found')
    return crawl

@router.get('/crawls/{crawl_id}/results')
def crawl_results(crawl_id: int, page: int = 1, size: int = 20, db: Session = Depends(get_db)):
    q = db.query(CrawledPage).filter_by(crawl_id=crawl_id)
    return {"items": q.offset((page-1)*size).limit(size).all(), "total": q.count()}

@router.post('/embeddings/index')
def embeddings_index(doc_id: str, text: str):
    svc = EmbeddingService(); svc.ensure_collection(); return svc.index(doc_id, text)

@router.post('/entities/extract')
def entities_extract(text_id: str, text: str):
    return EntityService().persist(text_id, text)

@router.post('/scores/seo')
def score_seo(page: dict): return seo_score(page)

@router.post('/scores/aeo')
def score_aeo(text: str, chunk_count: int): return aeo_score(text, chunk_count)

@router.post('/scores/geo')
def score_geo(entity_count: int, rel_count: int, brand_mentions: int): return geo_score(entity_count, rel_count, brand_mentions)

@router.post('/visibility/simulate')
def simulate(query: str, target: dict, competitor: dict): return visibility_simulation(query, target, competitor)
