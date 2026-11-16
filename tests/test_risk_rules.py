from src.transformations.risk_rules import calculate_risk_score

def test_low_risk_standard_transaction():
    score, tier = calculate_risk_score(
        is_suspicious_flag=False,
        amount_usd=120.50,
        txns_last_1hr=1,
        is_impossible_travel=False,
        country_code="US"
    )
    assert score == 0
    assert tier == "LOW"

def test_critical_risk_impossible_travel_and_high_amount():
    score, tier = calculate_risk_score(
        is_suspicious_flag=True,
        amount_usd=15000.00,
        txns_last_1hr=5,
        is_impossible_travel=True,
        country_code="KY"
    )
    assert score == 100
    assert tier == "CRITICAL"

def test_medium_risk_velocity_spike():
    score, tier = calculate_risk_score(
        is_suspicious_flag=False,
        amount_usd=250.00,
        txns_last_1hr=4,
        is_impossible_travel=False,
        country_code="GB"
    )
    assert score == 20
    assert tier == "MEDIUM"