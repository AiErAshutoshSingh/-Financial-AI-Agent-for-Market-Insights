import streamlit as st
import pandas as pd
import plotly.express as px

# ====================================
# PAGE CONFIG
# ====================================

st.set_page_config(
    page_title="Expense Tracker",
    page_icon="💰",
    layout="wide"
)

# ====================================
# HEADER
# ====================================

st.title("💰 Smart Expense Tracker")
st.caption(
    "Track, Analyze and Optimize Your Spending"
)

# ====================================
# FILE UPLOAD
# ====================================

file = st.file_uploader(
    "📂 Upload Expense CSV",
    type=["csv"]
)

if file:

    # ===============================
    # LOAD DATA
    # ===============================

    df = pd.read_csv(file)

    df.columns = (
        df.columns
        .str.strip()
        .str.lower()
    )

    # Date handling
    if "date" in df.columns:

        df["date"] = pd.to_datetime(
            df["date"],
            dayfirst=True,
            errors="coerce"
        )

    # Amount handling
    df["amount"] = pd.to_numeric(
        df["amount"],
        errors="coerce"
    )

    df = df.dropna(
        subset=["amount"]
    )

    # ===============================
    # KPI CARDS
    # ===============================

    total_expense = df["amount"].sum()

    avg_expense = df["amount"].mean()

    total_transactions = len(df)

    top_category = (
        df.groupby("category")["amount"]
        .sum()
        .idxmax()
    )

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            "💸 Total Expense",
            f"₹{total_expense:,.0f}"
        )

    with col2:
        st.metric(
            "📊 Avg Transaction",
            f"₹{avg_expense:,.0f}"
        )

    with col3:
        st.metric(
            "🧾 Transactions",
            total_transactions
        )

    with col4:
        st.metric(
            "🔥 Top Category",
            top_category
        )

    st.markdown("---")

    # ===============================
    # FILTER
    # ===============================

    categories = st.multiselect(
        "Filter Categories",
        options=df["category"].unique(),
        default=df["category"].unique()
    )

    filtered_df = df[
        df["category"].isin(categories)
    ]

    category_total = (
        filtered_df.groupby("category")["amount"]
        .sum()
        .reset_index()
    )

    # ===============================
    # DONUT + BAR CHART
    # ===============================

    col1, col2 = st.columns(2)

    with col1:

        pie = px.pie(
            category_total,
            names="category",
            values="amount",
            hole=0.55,
            title="Expense Distribution"
        )

        st.plotly_chart(
            pie,
            use_container_width=True
        )

    with col2:

        bar = px.bar(
            category_total,
            x="category",
            y="amount",
            text_auto=True,
            title="Category Wise Spending"
        )

        st.plotly_chart(
            bar,
            use_container_width=True
        )

    st.markdown("---")

    # ===============================
    # DAILY TREND
    # ===============================

    if "date" in filtered_df.columns:

        daily = (
            filtered_df.groupby("date")["amount"]
            .sum()
            .reset_index()
        )

        trend = px.area(
            daily,
            x="date",
            y="amount",
            title="📈 Daily Expense Trend"
        )

        st.plotly_chart(
            trend,
            use_container_width=True
        )

    st.markdown("---")

    # ===============================
    # TOP CATEGORIES
    # ===============================

    st.subheader(
        "🏆 Top Spending Categories"
    )

    ranking = (
        filtered_df.groupby("category")["amount"]
        .sum()
        .sort_values(
            ascending=False
        )
        .reset_index()
    )

    st.dataframe(
        ranking,
        use_container_width=True
    )

    st.markdown("---")

    # ===============================
    # TOP EXPENSES
    # ===============================

    st.subheader(
        "💰 Top 10 Transactions"
    )

    top_expenses = (
        filtered_df.sort_values(
            by="amount",
            ascending=False
        )
        .head(10)
    )

    st.dataframe(
        top_expenses,
        use_container_width=True
    )

    st.markdown("---")

    # ===============================
    # INSIGHTS
    # ===============================

    highest_spending = ranking.iloc[0]["category"]

    lowest_spending = ranking.iloc[-1]["category"]

    st.subheader(
        "🧠 AI Financial Insights"
    )

    st.info(
        f"""
        💸 Total Spending: ₹{total_expense:,.0f}

        🔥 Highest Spending Category: {highest_spending}

        📉 Lowest Spending Category: {lowest_spending}

        📊 Average Transaction: ₹{avg_expense:,.0f}

        🧾 Total Transactions: {total_transactions}

        💡 Consider reducing expenses in the highest spending category to improve savings.
        """
    )

    st.markdown("---")

    # ===============================
    # RAW DATA
    # ===============================

    with st.expander(
        "📂 View Full Dataset"
    ):

        st.dataframe(
            filtered_df,
            use_container_width=True
        )