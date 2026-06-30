import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

from indicators.rsi import calculate_rsi
from indicators.ema import calculate_ema
from indicators.macd import calculate_macd
from indicators.atr import calculate_atr 
from indicators.trend import detect_trend
from indicators.candlestick import detect_pattern
from indicators.support_resistance import support_resistance

from analysis.volume import volume_analysis
from analysis.risk import risk_management
from analysis.position_sizing import position_size
from analysis.backtest import backtest

from ai.scorer import calculate_score, confidence
from ai.decision import ai_decision
from ai.weighted_analysis import weighted_analysis
from ai.smart_score import smart_score
from ai.indicator_summary import indicator_summary

from strategies.signal import generate_signal

# -------------------------------------------------
# PAGE CONFIG
# -------------------------------------------------

st.set_page_config(
    page_title="BullEye AI",
    page_icon="📈",
    layout="wide"
)

st.title("📈 BullEye AI")
st.subheader("Professional AI Stock Analysis Platform")

st.markdown("---")

# -------------------------------------------------
# SIDEBAR
# -------------------------------------------------

st.sidebar.title("⚙️ BullEye AI")

stock = st.sidebar.text_input(
    "NSE Stock Symbol",
    value="RELIANCE.NS"
).upper()

capital = st.sidebar.number_input(
    "Capital (₹)",
    min_value=10000,
    value=100000,
    step=10000
)

risk_percent = st.sidebar.slider(
    "Risk Per Trade (%)",
    1,
    10,
    2
)

analyze = st.sidebar.button("📊 Analyze Stock")

# -------------------------------------------------
# MAIN ANALYSIS
# -------------------------------------------------

if analyze:

    with st.spinner("Downloading Market Data..."):

        data = yf.download(
            stock,
            period="1y",
            progress=False
        )

    if hasattr(data.columns, "nlevels") and data.columns.nlevels > 1:
        data.columns = data.columns.get_level_values(0)

    st.success("✅ Market Data Loaded Successfully")
        # -------------------------------------------------
    # INDICATOR CALCULATIONS
    # -------------------------------------------------

    data["RSI"] = calculate_rsi(data)
    data["EMA20"] = calculate_ema(data)
    data["ATR"] = calculate_atr(data)

    data["Trend"] = data.apply(
        lambda row: detect_trend(
            row["Close"],
            row["EMA20"]
        ),
        axis=1
    )

    data["MACD"], data["MACD_Signal"], data["Histogram"] = calculate_macd(data)

    current_volume, avg_volume, volume_status = volume_analysis(data)

    data["Support"], data["Resistance"] = support_resistance(data)

    entry, stop_loss, target1, target2, rr = risk_management(
        data["Close"].iloc[-1],
        data["Support"].iloc[-1],
        data["Resistance"].iloc[-1]
    )

    qty, investment, max_risk, risk_per_share = position_size(
        capital,
        risk_percent,
        entry,
        stop_loss
    )

    pattern = detect_pattern(data)

    scores = data.apply(
        lambda row: calculate_score(
            row["RSI"],
            row["Close"],
            row["EMA20"],
            row["MACD"],
            row["MACD_Signal"],
            volume_status
        ),
        axis=1
    )

    data["Score"] = scores.apply(lambda x: x[0])
    data["Reasons"] = scores.apply(lambda x: ", ".join(x[1]))
    data["AI_Confidence"] = data["Score"].apply(confidence)
    data["Signal"] = data["Score"].apply(generate_signal)

    weighted_score = weighted_analysis(
        data["RSI"].iloc[-1],
        data["Close"].iloc[-1],
        data["EMA20"].iloc[-1],
        data["MACD"].iloc[-1],
        data["MACD_Signal"].iloc[-1],
        data["Trend"].iloc[-1],
        volume_status,
        pattern
    )

    final_ai_score = smart_score(
        data["Score"].iloc[-1],
        weighted_score
    )

    verdict, strength, recommendation = ai_decision(
        final_ai_score,
        data["Trend"].iloc[-1],
        volume_status,
        data["ATR"].iloc[-1]
    )

    summary, bullish, bearish, neutral, bias = indicator_summary(
        data["RSI"].iloc[-1],
        data["Close"].iloc[-1],
        data["EMA20"].iloc[-1],
        data["MACD"].iloc[-1],
        data["MACD_Signal"].iloc[-1],
        data["Trend"].iloc[-1],
        volume_status,
        pattern,
        data["ATR"].iloc[-1]
    )

    total, win, loss, rate = backtest(data)

    latest = data.iloc[-1]
        # -------------------------------------------------
    # AI DASHBOARD
    # -------------------------------------------------

    st.markdown("---")
    st.header("📊 BullEye AI Dashboard")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            "💰 Close Price",
            f"₹{latest['Close']:.2f}"
        )

    with col2:
        st.metric(
            "🤖 AI Score",
            f"{latest['Score']}/100"
        )

    with col3:
        st.metric(
            "⚖️ Weighted Score",
            f"{weighted_score}/100"
        )

    with col4:
        st.metric(
            "⭐ Smart Score",
            f"{final_ai_score}/100"
        )

    st.markdown("---")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.info("### 📈 Trend")
        st.write(latest["Trend"])

    with col2:
        st.info("### 🎯 Signal")
        st.write(latest["Signal"])

    with col3:
        st.info("### 🔒 Confidence")
        st.write(latest["AI_Confidence"])

    st.markdown("---")

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("🤖 AI Decision")

        st.write(f"**Verdict :** {verdict}")
        st.write(f"**Strength :** {strength}")

    with col2:
        st.subheader("📝 Recommendation")

        for line in recommendation.split("\n"):
            st.write("• " + line)
                # -------------------------------------------------
    # INDICATOR SUMMARY
    # -------------------------------------------------

    st.markdown("---")
    st.header("📊 Indicator Summary")

    summary_df = pd.DataFrame(
        {
            "Indicator": list(summary.keys()),
            "Status": list(summary.values())
        }
    )

    st.dataframe(
        summary_df,
        use_container_width=True,
        hide_index=True
    )

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("🟢 Bullish", bullish)
    col2.metric("🔴 Bearish", bearish)
    col3.metric("🟡 Neutral", neutral)
    col4.metric("Market Bias", bias)

    # -------------------------------------------------
    # RISK MANAGEMENT
    # -------------------------------------------------

    st.markdown("---")
    st.header("💰 Trade Plan")

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Entry", f"₹{entry:.2f}")
    col2.metric("Stop Loss", f"₹{stop_loss:.2f}")
    col3.metric("Target 1", f"₹{target1:.2f}")
    col4.metric("Target 2", f"₹{target2:.2f}")

    st.info(f"Risk Reward Ratio : 1 : {rr}")

    # -------------------------------------------------
    # POSITION SIZING
    # -------------------------------------------------

    st.markdown("---")
    st.header("📦 Position Sizing")

    c1, c2, c3 = st.columns(3)

    c1.metric("Capital", f"₹{capital:,.0f}")
    c2.metric("Risk Per Trade", f"{risk_percent}%")
    c3.metric("Maximum Risk", f"₹{max_risk:,.2f}")

    c1, c2, c3 = st.columns(3)

    c1.metric("Risk / Share", f"₹{risk_per_share:.2f}")
    c2.metric("Recommended Qty", qty)
    c3.metric("Investment", f"₹{investment:,.2f}")

    # -------------------------------------------------
    # BACKTEST
    # -------------------------------------------------

    st.markdown("---")
    st.header("📈 Backtest Result")

    b1, b2, b3, b4 = st.columns(4)

    b1.metric("Trades", total)
    b2.metric("Winning", win)
    b3.metric("Losing", loss)
    b4.metric("Win Rate", f"{rate}%")

    # -------------------------------------------------
    # PRICE CHART
    # -------------------------------------------------

    st.markdown("---")
    st.header("📉 Price Chart")

    chart = data[["Close", "EMA20"]]

    st.line_chart(chart)

    # -------------------------------------------------
    # RSI CHART
    # -------------------------------------------------

    st.markdown("---")
    st.header("📊 RSI")

    st.line_chart(data["RSI"])

    # -------------------------------------------------
    # MACD CHART
    # -------------------------------------------------

    st.markdown("---")
    st.header("📈 MACD")

    st.line_chart(
        data[
            [
                "MACD",
                "MACD_Signal"
            ]
        ]
    )

    st.success("✅ Analysis Completed Successfully")