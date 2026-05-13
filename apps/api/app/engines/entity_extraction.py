import re

class EntityExtractionEngine:
    def extract_entities_batch(self, pages):
        entities = []
        for p in pages:
            tokens = re.findall(r"[A-Z][a-zA-Z]{2,}", p.get("content", ""))
            entities.extend({"entity": t, "type": "unknown", "source": p["url"]} for t in tokens)
        return entities[:200]
