import hashlib

class VectorIndexingEngine:
    async def index_pages(self, pages):
        # placeholder deterministic embeddings; swap with sentence-transformers
        return [{"id": hashlib.sha1(p["url"].encode()).hexdigest(), "embedding": [0.1, 0.2, 0.3]} for p in pages]
