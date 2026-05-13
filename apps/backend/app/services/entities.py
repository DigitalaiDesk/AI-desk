from collections import Counter

import spacy
from gliner import GLiNER
from neo4j import GraphDatabase

from app.core.config import settings


class EntityService:
    labels = ["organization", "person", "product", "service", "location", "technology", "concept", "brand"]

    def __init__(self):
        self.nlp = spacy.load("en_core_web_sm")
        self.gliner = GLiNER.from_pretrained("urchade/gliner_multi-v2.1")
        self.driver = GraphDatabase.driver(settings.neo4j_uri, auth=(settings.neo4j_user, settings.neo4j_password))

    def extract(self, text: str):
        doc = self.nlp(text)
        spacy_entities = [(e.text.strip().lower(), e.label_, 0.75) for e in doc.ents]
        gliner_entities = [(e["text"].strip().lower(), e["label"], float(e["score"])) for e in self.gliner.predict_entities(text, self.labels)]
        merged = {}
        for name, label, score in spacy_entities + gliner_entities:
            if name not in merged or merged[name][1] < score:
                merged[name] = (label, score)
        pairs = Counter()
        names = list(merged.keys())
        for i in range(len(names)):
            for j in range(i + 1, len(names)):
                pairs[(names[i], names[j])] += 1
        return merged, pairs

    def persist(self, text_id: str, text: str):
        entities, rels = self.extract(text)
        with self.driver.session() as s:
            for name, (label, score) in entities.items():
                s.run("MERGE (e:Entity {name:$name}) SET e.label=$label, e.confidence=$score", name=name, label=label, score=score)
            for (a, b), weight in rels.items():
                s.run(
                    "MATCH (a:Entity {name:$a}),(b:Entity {name:$b}) MERGE (a)-[r:CO_OCCURS_WITH]->(b) SET r.weight=coalesce(r.weight,0)+$w",
                    a=a,
                    b=b,
                    w=weight,
                )
        return {"text_id": text_id, "entities": len(entities), "relationships": len(rels)}
