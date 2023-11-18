from blogcrawler.blogcrawler import get_sympathy_users


def test_get_sympathy_users():
    assert isinstance(get_sympathy_users("qjmoney", "223268359372"), list)
    assert len(get_sympathy_users("qjmoney", "223268359372")) > 40


def test_get_sympathy_users_more_than_itemcount():
    assert isinstance(get_sympathy_users("qjmoney", "223184189607"), list)
    assert len(get_sympathy_users("qjmoney", "223184189607")) > 60
