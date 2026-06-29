def risk_management(close, support, resistance):

    entry = close

    stop_loss = support

    risk = entry - stop_loss

    target1 = entry + (risk * 2)

    target2 = entry + (risk * 3)

    rr = round((target1 - entry) / risk, 2) if risk > 0 else 0

    return (
        entry,
        stop_loss,
        target1,
        target2,
        rr
    )