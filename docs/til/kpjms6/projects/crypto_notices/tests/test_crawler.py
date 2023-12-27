from bithumbcrawler.crawler import get_market_notices


def test_get_market_notices():
    actual = get_market_notices()

    assert len(actual) == 4
    assert any(["빅타임" in each for each in actual])
    assert any(["모스코인" in each for each in actual])
    assert any(["홋스퍼" in each for each in actual])
    assert any(["하이파이" in each for each in actual])
