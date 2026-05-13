import asyncio
import re
from urllib.parse import urljoin
import httpx

class CrawlerEngine:
    async def crawl_site(self, payload):
        async with httpx.AsyncClient(timeout=10) as client:
            resp = await client.get(str(payload.url))
            html = resp.text
        links = sorted(set(re.findall(r'href=[\"\'](https?://[^\"\']+|/[^\"\']+)', html)))
        normalized = [urljoin(str(payload.url), link) for link in links[: payload.max_pages]]
        await asyncio.sleep(0)
        return {"root": str(payload.url), "pages": [{"url": u, "content": ""} for u in normalized]}
