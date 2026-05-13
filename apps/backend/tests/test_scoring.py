from app.services.scoring import seo_score, aeo_score, geo_score


def test_seo_score_missing_fields():
    result = seo_score({"headings": []})
    assert result["score"] < 100


def test_aeo_score():
    result = aeo_score("What is AI?: Artificial intelligence", 10)
    assert result["score"] > 0


def test_geo_score():
    result = geo_score(20, 10, 5)
    assert result["score"] > 0
