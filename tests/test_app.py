from credit_limit.app import app

def test_credit_limit_app_initialization() -> None:
    assert app.title == "Credit Limit Core API"