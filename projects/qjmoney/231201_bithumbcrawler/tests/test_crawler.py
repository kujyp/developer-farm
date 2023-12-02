from bithumbcrawler.crawler import get_notices


def test_get_notices():
    actual = get_notices()

    assert len(actual) > 0
