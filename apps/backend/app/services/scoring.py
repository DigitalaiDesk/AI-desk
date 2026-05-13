def clamp(n: float) -> float:
    return max(0.0, min(100.0, n))


def seo_score(page: dict) -> dict:
    score = 100.0
    issues = []
    if not page.get("title"):
        score -= 15; issues.append(("missing_title", "high"))
    if len(page.get("headings", [])) < 2:
        score -= 8; issues.append(("thin_heading_structure", "medium"))
    if page.get("metadata", {}).get("duplicate"):
        score -= 20; issues.append(("duplicate_content", "high"))
    if not page.get("canonical"):
        score -= 10; issues.append(("missing_canonical", "medium"))
    return {"score": clamp(score), "issues": issues}


def aeo_score(text: str, chunk_count: int) -> dict:
    words = len(text.split())
    direct_answer = 20 if "?" in text and ":" in text else 10
    retrieval = min(40, chunk_count * 2)
    clarity = min(40, 4000 / max(words, 100))
    total = clamp(direct_answer + retrieval + clarity)
    return {"score": total, "retrieval_readiness": retrieval, "citation_probability": min(100, total * 0.9)}


def geo_score(entity_count: int, rel_count: int, brand_mentions: int) -> dict:
    authority = min(40, entity_count * 1.2)
    trust = min(30, rel_count * 0.8)
    consistency = min(30, brand_mentions * 2)
    score = clamp(authority + trust + consistency)
    return {"score": score, "ai_recommendation_probability": min(100, score * 0.88), "ai_memory_score": min(100, score * 0.81)}


def visibility_simulation(query: str, target: dict, competitor: dict) -> dict:
    gaps = []
    if competitor["semantic_match"] > target["semantic_match"]:
        gaps.append("semantic_match_quality")
    if competitor["entities"] > target["entities"]:
        gaps.append("missing_entities")
    if competitor["trust"] > target["trust"]:
        gaps.append("missing_trust_signals")
    return {"query": query, "why_competitors_rank": gaps, "why_target_fails": gaps, "action_items": [f"Improve {g}" for g in gaps]}
