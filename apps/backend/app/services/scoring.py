from __future__ import annotations

import re
from statistics import mean
from typing import Any


def clamp(n: float, low: float = 0.0, high: float = 100.0) -> float:
    return max(low, min(high, n))


def _flesch_reading_ease(text: str) -> float:
    sentences = [s for s in re.split(r"[.!?]+", text) if s.strip()]
    words = re.findall(r"\b\w+\b", text)
    if not sentences or not words:
        return 0.0

    def syllables(word: str) -> int:
        word = re.sub(r"[^a-z]", "", word.lower())
        if not word:
            return 1
        groups = re.findall(r"[aeiouy]+", word)
        count = len(groups)
        if word.endswith("e") and count > 1:
            count -= 1
        return max(1, count)

    total_syllables = sum(syllables(w) for w in words)
    asl = len(words) / len(sentences)
    asw = total_syllables / len(words)
    return clamp(206.835 - 1.015 * asl - 84.6 * asw)


def seo_score(page: dict[str, Any]) -> dict[str, Any]:
    title = (page.get("title") or "").strip()
    meta = page.get("metadata", {}) or {}
    description = (meta.get("description") or meta.get("og:description") or "").strip()
    headings = page.get("headings", []) or []
    content = page.get("content", "") or ""
    internal_links = page.get("internal_links", []) or []
    images = page.get("images", []) or []

    score = 100.0
    issues: list[tuple[str, str]] = []

    if not (50 <= len(title) <= 60):
        score -= 10
        issues.append(("title_length_outside_optimal", "medium"))
    if not (70 <= len(description) <= 160):
        score -= 10
        issues.append(("meta_description_length_outside_optimal", "medium"))
    if not page.get("canonical"):
        score -= 8
        issues.append(("missing_canonical", "high"))
    if not meta.get("robots"):
        score -= 4
        issues.append(("missing_robots_meta", "low"))

    h1_count = sum(1 for h in headings if isinstance(h, str) and h.lower().startswith("h1:"))
    h2_count = sum(1 for h in headings if isinstance(h, str) and h.lower().startswith("h2:"))
    if h1_count != 1:
        score -= 10
        issues.append(("heading_h1_count_invalid", "high"))
    if h2_count < 1:
        score -= 6
        issues.append(("missing_h2_subsections", "medium"))

    if images:
        covered = sum(1 for img in images if img.get("alt")) / max(len(images), 1)
        if covered < 0.8:
            score -= 8
            issues.append(("low_image_alt_coverage", "medium"))

    if len(internal_links) < 2:
        score -= 6
        issues.append(("weak_internal_linking", "medium"))

    readability = _flesch_reading_ease(content)
    if readability < 50:
        score -= 10
        issues.append(("low_readability", "medium"))

    if "viewport" not in meta:
        score -= 6
        issues.append(("missing_viewport_meta", "high"))
    if not str(page.get("url", "")).startswith("https://"):
        score -= 8
        issues.append(("non_https_url", "high"))

    return {
        "score": clamp(score),
        "issues": issues,
        "readability": readability,
    }


def aeo_score(text: str, chunk_count: int) -> dict[str, Any]:
    paragraphs = [p.strip() for p in re.split(r"\n\s*\n", text) if p.strip()]
    if not paragraphs:
        return {"score": 0.0, "direct_answer_score": 0.0, "retrieval_readiness": 0.0}

    sent_re = re.compile(r"[^.!?]+[.!?]")
    qualifying = 0
    for p in paragraphs:
        sentences = [s.strip() for s in sent_re.findall(p)]
        if 2 <= len(sentences) <= 3 and all(5 <= len(s.split()) <= 28 for s in sentences):
            qualifying += 1

    direct_answer = clamp((qualifying / len(paragraphs)) * 100)
    retrieval = clamp(min(100.0, chunk_count * 8.5))
    score = clamp(0.6 * direct_answer + 0.4 * retrieval)
    return {
        "score": score,
        "direct_answer_score": direct_answer,
        "retrieval_readiness": retrieval,
    }


def geo_score(entity_count: int, rel_count: int, brand_mentions: int) -> dict[str, float]:
    retrieval = clamp(entity_count * 2.2)
    answer = clamp((brand_mentions * 6) + (rel_count * 1.5))
    citation = clamp((entity_count / max(1, brand_mentions)) * 12)
    score = clamp(0.35 * retrieval + 0.35 * answer + 0.30 * citation)
    return {
        "score": score,
        "retrieval_readiness": retrieval,
        "answer_extraction": answer,
        "citation_density": citation,
    }


def visibility_simulation(query: str, target: dict[str, float], competitor: dict[str, float]) -> dict[str, Any]:
    factors = ["semantic_match", "entities", "trust"]
    gaps = [f for f in factors if competitor.get(f, 0.0) > target.get(f, 0.0)]
    loss = mean([competitor.get(g, 0.0) - target.get(g, 0.0) for g in gaps]) if gaps else 0.0
    return {
        "query": query,
        "why_competitors_rank": gaps,
        "why_target_fails": gaps,
        "action_items": [f"Improve {g}" for g in gaps],
        "estimated_gap": round(loss, 3),
    }
