def position_size(capital, risk_percent, entry_price, stop_loss):
    """
    Calculate recommended position size.
    """

    max_risk = capital * (risk_percent / 100)

    risk_per_share = abs(entry_price - stop_loss)

    if risk_per_share == 0:
        return 0, 0, max_risk, risk_per_share

    quantity = int(max_risk // risk_per_share)

    investment = quantity * entry_price

    return quantity, investment, max_risk, risk_per_share