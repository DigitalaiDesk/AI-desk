from app.services.scoring import aeo_score, geo_score, seo_score, visibility_simulation


def test_seo_score_missing_fields():
    result = seo_score({"headings": [], "url": "http://example.com"})
    assert result["score"] < 100
    assert any(code == "non_https_url" for code, _ in result["issues"])


def test_aeo_score():
    text = "AI is a field that builds smart systems. It helps teams automate work.\n\nMachine learning means models improve with data. It is used in search and forecasting."
    result = aeo_score(text, 10)
    assert result["score"] > 0
    assert result["direct_answer_score"] > 0


def test_geo_score():
    result = geo_score(20, 10, 5)
    assert result["score"] > 0
    assert 0 <= result["citation_density"] <= 100


def test_visibility_simulation_no_gap():
    target = {"semantic_match": 0.8, "entities": 20, "trust": 0.7}
    comp = {"semantic_match": 0.7, "entities": 10, "trust": 0.6}
    result = visibility_simulation("what is ai", target, comp)
    assert result["why_target_fails"] == []
