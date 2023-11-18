

def test_get_sympathy_users():
    assert isinstance(get_sympathy_users("qjmoney", "223268359372"), list)
    assert len(get_sympathy_users("qjmoney", "223268359372")) > 40
