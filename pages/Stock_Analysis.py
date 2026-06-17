import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# ====================================
# PAGE CONFIG
# ====================================

st.set_page_config(
    page_title="Stock Analysis Pro",
    page_icon="📈",
    layout="wide"
)

# ====================================
# CUSTOM HEADER
# ====================================

st.markdown("""
# 📈 Stock Analysis Pro
### Real-Time Market Intelligence Dashboard
""")

st.markdown("---")

# ====================================
# SIDEBAR
# ====================================

st.sidebar.title("📊 Stock Controls")

ticker = st.sidebar.text_input(
    "Stock Symbol",
    "TCS.NS"
)

period = st.sidebar.selectbox(
    "Historical Data",
    ["1mo", "3mo", "6mo", "1y", "2y", "5y"]
)

# ====================================
# ANALYZE BUTTON
# ====================================

if st.sidebar.button("🚀 Analyze Stock"):

    try:

        stock = yf.Ticker(ticker)

        info = stock.info

        hist = stock.history(period=period)

        if hist.empty:
            st.error("No stock data found.")
            st.stop()

        # ====================================
        # COMPANY HEADER
        # ====================================

        company_name = info.get(
            "longName",
            ticker
        )

        st.subheader(company_name)

        st.caption(
            info.get(
                "sector",
                "Sector Not Available"
            )
        )

        # ====================================
        # LIVE METRICS
        # ====================================

        current_price = info.get(
            "currentPrice",
            0
        )

        previous_close = info.get(
            "previousClose",
            0
        )

        day_high = info.get(
            "dayHigh",
            0
        )

        day_low = info.get(
            "dayLow",
            0
        )

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.metric(
                "💰 Current Price",
                f"₹{current_price}"
            )

        with col2:
            st.metric(
                "📊 Previous Close",
                f"₹{previous_close}"
            )

        with col3:
            st.metric(
                "📈 Day High",
                f"₹{day_high}"
            )

        with col4:
            st.metric(
                "📉 Day Low",
                f"₹{day_low}"
            )

        st.markdown("---")

        # ====================================
        # FUNDAMENTALS
        # ====================================

        st.subheader("📑 Fundamentals")

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.metric(
                "Market Cap",
                f"{info.get('marketCap',0):,}"
            )

        with col2:
            st.metric(
                "PE Ratio",
                info.get("trailingPE", "N/A")
            )

        with col3:
            st.metric(
                "Dividend Yield",
                info.get("dividendYield", "N/A")
            )

        with col4:
            st.metric(
                "Volume",
                f"{info.get('volume',0):,}"
            )

        st.markdown("---")

        # ====================================
        # 52 WEEK STATS
        # ====================================

        st.subheader("📅 52 Week Statistics")

        col1, col2 = st.columns(2)

        with col1:
            st.metric(
                "52 Week High",
                info.get(
                    "fiftyTwoWeekHigh",
                    "N/A"
                )
            )

        with col2:
            st.metric(
                "52 Week Low",
                info.get(
                    "fiftyTwoWeekLow",
                    "N/A"
                )
            )

        st.markdown("---")

        # ====================================
        # CANDLESTICK CHART
        # ====================================

        st.subheader("🕯 Candlestick Chart")

        candle = go.Figure(
            data=[
                go.Candlestick(
                    x=hist.index,
                    open=hist["Open"],
                    high=hist["High"],
                    low=hist["Low"],
                    close=hist["Close"]
                )
            ]
        )

        candle.update_layout(
            height=600
        )

        st.plotly_chart(
            candle,
            use_container_width=True
        )

        st.markdown("---")

        # ====================================
        # MOVING AVERAGES
        # ====================================

        st.subheader(
            "📈 Moving Average Analysis"
        )

        hist["MA20"] = (
            hist["Close"]
            .rolling(20)
            .mean()
        )

        hist["MA50"] = (
            hist["Close"]
            .rolling(50)
            .mean()
        )

        ma_chart = px.line(
            hist,
            y=[
                "Close",
                "MA20",
                "MA50"
            ],
            title="Closing Price vs Moving Averages"
        )

        st.plotly_chart(
            ma_chart,
            use_container_width=True
        )

        st.markdown("---")

        # ====================================
        # VOLUME ANALYSIS
        # ====================================

        st.subheader(
            "📊 Trading Volume"
        )

        volume_chart = px.bar(
            hist,
            x=hist.index,
            y="Volume"
        )

        st.plotly_chart(
            volume_chart,
            use_container_width=True
        )

        st.markdown("---")

        # ====================================
        # RETURNS ANALYSIS
        # ====================================

        st.subheader(
            "💹 Performance Analysis"
        )

        total_return = (
            (
                hist["Close"].iloc[-1]
                -
                hist["Close"].iloc[0]
            )
            /
            hist["Close"].iloc[0]
        ) * 100

        st.metric(
            "Total Return",
            f"{total_return:.2f}%"
        )

        st.markdown("---")

        # ====================================
        # RISK ANALYSIS
        # ====================================

        st.subheader(
            "⚠ Risk Analysis"
        )

        volatility = (
            hist["Close"]
            .pct_change()
            .std()
            * 100
        )

        if volatility < 2:

            st.success(
                f"Low Risk ({volatility:.2f}%)"
            )

        elif volatility < 4:

            st.warning(
                f"Medium Risk ({volatility:.2f}%)"
            )

        else:

            st.error(
                f"High Risk ({volatility:.2f}%)"
            )

        st.markdown("---")

        # ====================================
        # COMPANY OVERVIEW
        # ====================================

        st.subheader(
            "🏢 Company Overview"
        )

        st.write(
            info.get(
                "longBusinessSummary",
                "No summary available."
            )
        )

        st.markdown("---")

        # ====================================
        # HISTORICAL DATA
        # ====================================

        st.subheader(
            "📋 Historical Data"
        )

        st.dataframe(
            hist.tail(50),
            use_container_width=True
        )

        csv = hist.to_csv()

        st.download_button(
            "⬇ Download Historical Data",
            csv,
            file_name=f"{ticker}.csv",
            mime="text/csv"
        )

    except Exception as e:

        st.error(
            f"Error: {str(e)}"
        )

else:

    st.info(
        "Enter a stock symbol and click Analyze Stock."
    )

    st.markdown("""
### Popular Indian Stocks

- TCS.NS
- INFY.NS
- RELIANCE.NS
- HDFCBANK.NS
- ICICIBANK.NS
- SBIN.NS
- LT.NS
- ITC.NS
""")