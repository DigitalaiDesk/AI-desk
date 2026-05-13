import asyncio
import hashlib
import json
import time
from collections import deque
from dataclasses import dataclass
from urllib.parse import urljoin, urlparse
from urllib.robotparser import RobotFileParser

import httpx
from bs4 import BeautifulSoup
from langdetect import detect
from sqlalchemy.orm import Session

from app.core.config import settings
from app.models.crawl import CrawledPage, CrawlError, CrawlRun


@dataclass(slots=True)
class QueueItem:
    url: str
    depth: int


class CrawlService:
    def __init__(self, db: Session):
        self.db = db

    async def run_crawl(self, crawl_id: int) -> None:
        crawl = self.db.get(CrawlRun, crawl_id)
        if not crawl:
            return
        crawl.status = "running"
        self.db.commit()

        robots = RobotFileParser()
        robots.set_url(urljoin(crawl.base_url, "/robots.txt"))
        try:
            robots.read()
        except Exception:
            pass

        domain = urlparse(crawl.base_url).netloc
        queue: deque[QueueItem] = deque([QueueItem(str(crawl.base_url), 0)])
        seen: set[str] = set()
        hashes: set[str] = set()
        sem = asyncio.Semaphore(settings.crawl_concurrency)
        client = httpx.AsyncClient(follow_redirects=True, timeout=20)

        async def worker(item: QueueItem):
            if item.url in seen or len(seen) >= crawl.max_pages:
                return
            seen.add(item.url)
            if not robots.can_fetch("*", item.url):
                return
            async with sem:
                await asyncio.sleep(1 / settings.crawl_rate_per_second)
                started = time.perf_counter()
                try:
                    response = await client.get(item.url)
                    elapsed = (time.perf_counter() - started) * 1000
                    soup = BeautifulSoup(response.text, "lxml")
                    text = " ".join(t.strip() for t in soup.stripped_strings)
                    digest = hashlib.sha256(text.encode("utf-8", errors="ignore")).hexdigest()
                    is_dup = digest in hashes
                    hashes.add(digest)
                    links = []
                    for a in soup.select("a[href]"):
                        full = urljoin(str(response.url), a["href"])
                        if urlparse(full).netloc == domain:
                            links.append(full)
                            if item.depth + 1 <= 4:
                                queue.append(QueueItem(full, item.depth + 1))
                    page = CrawledPage(
                        crawl_id=crawl.id,
                        url=item.url,
                        final_url=str(response.url),
                        status_code=response.status_code,
                        depth=item.depth,
                        title=soup.title.string.strip() if soup.title and soup.title.string else None,
                        headings=[h.get_text(strip=True) for h in soup.select("h1,h2,h3")],
                        metadata={
                            m.get("name") or m.get("property"): m.get("content")
                            for m in soup.select("meta[content]")
                        },
                        structured_data=[json.loads(s.string) for s in soup.select("script[type='application/ld+json']") if s.string],
                        content=text,
                        canonical=(soup.select_one("link[rel='canonical']") or {}).get("href") if soup.select_one("link[rel='canonical']") else None,
                        language=soup.html.get("lang") if soup.html else detect(text[:500]) if text else None,
                        duplicate_hash=digest,
                        internal_links=list(set(links)),
                        fetch_ms=elapsed,
                    )
                    if is_dup:
                        page.metadata["duplicate"] = True
                    self.db.add(page)
                    self.db.commit()
                except Exception as exc:
                    self.db.add(CrawlError(crawl_id=crawl.id, url=item.url, error_type=type(exc).__name__, message=str(exc), depth=item.depth))
                    self.db.commit()

        while queue and len(seen) < crawl.max_pages:
            batch = [queue.popleft() for _ in range(min(settings.crawl_concurrency, len(queue)))]
            await asyncio.gather(*(worker(i) for i in batch))

        await client.aclose()
        crawl.status = "completed"
        crawl.stats = {"pages": len(seen), "errors": self.db.query(CrawlError).filter_by(crawl_id=crawl.id).count()}
        self.db.commit()
