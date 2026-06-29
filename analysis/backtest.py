def backtest(data):

    total_trades = 0
    winning_trades = 0
    losing_trades = 0

    for i in range(len(data) - 1):

        signal = data["Signal"].iloc[i]

        buy_price = data["Close"].iloc[i]

        next_price = data["Close"].iloc[i + 1]

        if signal == "🟢 BUY":

            total_trades += 1

            if next_price > buy_price:
                winning_trades += 1
            else:
                losing_trades += 1

    if total_trades == 0:
        win_rate = 0
    else:
        win_rate = round((winning_trades / total_trades) * 100, 2)

    return total_trades, winning_trades, losing_trades, win_rate