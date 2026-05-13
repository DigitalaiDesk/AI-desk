from concurrent.futures import ThreadPoolExecutor
from typing import Iterable

from qdrant_client import QdrantClient
from qdrant_client.models import Distance, PointStruct, VectorParams
from sentence_transformers import SentenceTransformer

from app.core.config import settings


class EmbeddingService:
    def __init__(self):
        self.model = SentenceTransformer("BAAI/bge-small-en-v1.5")
        self.client = QdrantClient(url=settings.qdrant_url)

    def ensure_collection(self, name: str = "chunks"):
        self.client.recreate_collection(name, vectors_config=VectorParams(size=384, distance=Distance.COSINE))

    def chunk(self, text: str, max_tokens: int = 250, overlap: int = 40):
        words = text.split()
        i = 0
        chunks = []
        while i < len(words):
            c = words[i : i + max_tokens]
            chunks.append(" ".join(c))
            i += max_tokens - overlap
        return chunks

    def embed_chunks(self, chunks: Iterable[str]):
        with ThreadPoolExecutor(max_workers=4) as ex:
            return list(ex.map(lambda c: self.model.encode(c, normalize_embeddings=True).tolist(), chunks))

    def index(self, doc_id: str, text: str, collection: str = "chunks"):
        chunks = self.chunk(text)
        vectors = self.embed_chunks(chunks)
        points = [PointStruct(id=abs(hash(f"{doc_id}-{i}")), vector=v, payload={"doc_id": doc_id, "chunk": c, "idx": i}) for i, (c, v) in enumerate(zip(chunks, vectors))]
        self.client.upsert(collection_name=collection, points=points)
        return {"chunks": len(chunks), "status": "indexed"}
