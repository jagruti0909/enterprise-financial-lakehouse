def calculate_risk_score(
    is_suspicious_flag: bool,
    amount_usd: float,
    txns_last_1hr: int,
    is_impossible_travel: bool,
    country_code: str
) -> tuple[int, str]:
    """Deterministic business logic for transaction fraud scoring."""
    score = 0
    if is_suspicious_flag:
        score += 40
    if amount_usd > 10000:
        score += 25
    elif amount_usd > 5000:
        score += 10
    if txns_last_1hr >= 4:
        score += 20
    if is_impossible_travel:
        score += 35
    if country_code in {"KY", "PA", "VG"}:
        score += 15

    score = min(100, score)

    if score >= 70:
        tier = "CRITICAL"
    elif score >= 40:
        tier = "HIGH"
    elif score >= 20:
        tier = "MEDIUM"
    else:
        tier = "LOW"

    return score, tier