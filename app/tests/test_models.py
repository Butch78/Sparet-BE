from app.models.balance import Balance

from app.utils.config import settings, Settings

# Test Pydantic Models
def test_balance_model(settings: Settings = settings):

    # Test Account Model
    balance = Balance(
        account_id=settings.TEST_ACCOUNT_ID,
        available=None,
        current=None,
        limit=0,
        unofficial_currency_code="USD",
        iso_curreny_code="USD",
    )

    assert balance is not None
    assert balance.account_id == settings.TEST_ACCOUNT_ID
    assert balance.available == 0.0
    assert balance.current == 0.0
    assert balance.limit == 0
    assert balance.unofficial_currency_code == "USD"
    assert balance.iso_curreny_code == "USD"
