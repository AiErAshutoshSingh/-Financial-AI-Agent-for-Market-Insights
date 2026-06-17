import streamlit as st
import pandas as pd
import plotly.express as px

# ==================================
# PAGE CONFIG
# ==================================

st.set_page_config(
    page_title="Finance Dashboard",
    page_icon="💰",
    layout="wide"
)

st.title("💰 Finance Dashboard")
st.caption("Track, Analyze & Optimize Your Spending")

# ==================================
# FILE UPLOAD
# ==================================

uploaded_file = st.file_uploader(
    "📂 Upload Expense CSV",
    type=["csv"]
)

if uploaded_file:

    try:

        # ==========================
        # LOAD DATA
        # ==========================

        df = pd.read_csv(uploaded_file)

        # Clean column names
        df.columns = (
            df.columns
            .str.strip()
            .str.lower()
        )

        # Required columns
        required_columns = [
            "date",
            "category",
            "amount"
        ]

        missing_columns = [
            col for col in required_columns
            if col not in df.columns
        ]

        if missing_columns:

            st.error(
                f"Missing columns: {', '.join(missing_columns)}"
            )

            st.stop()

        # ==========================
        # DATA CLEANING
        # ==========================

        df["amount"] = pd.to_numeric(
            df["amount"],
            errors="coerce"
        )

        # Supports:
        # 08/05/2022
        # 08-05-2022
        # 08/05/22

        df["date"] = pd.to_datetime(
            df["date"],
            dayfirst=True,
            errors="coerce"
        )

        df = df.dropna(
            subset=["date", "amount"]
        )

        if len(df) == 0:

            st.error(
                "No valid records found."
            )

            st.stop()

        # ==========================
        # DATA PREVIEW
        # ==========================

        with st.expander(
            "📄 Dataset Preview"
        ):

            st.write(
                "Columns Found:"
            )

            st.write(
                df.columns.tolist()
            )

            st.dataframe(
                df.head()
            )

        st.markdown("---")

        # ==========================
        # KPI CARDS
        # ==========================

        total_expense = df["amount"].sum()

        avg_expense = df["amount"].mean()

        total_transactions = len(df)

        category_summary = (
            df.groupby("category")["amount"]
            .sum()
        )

        highest_category = (
            category_summary.idxmax()
            if not category_summary.empty
            else "N/A"
        )

        col1, col2, col3, col4 = st.columns(4)

        with col1:

            st.metric(
                "💸 Total Expenses",
                f"₹{total_expense:,.0f}"
            )

        with col2:

            st.metric(
                "📊 Average Expense",
                f"₹{avg_expense:,.0f}"
            )

        with col3:

            st.metric(
                "🔥 Top Category",
                highest_category
            )

        with col4:

            st.metric(
                "🧾 Transactions",
                total_transactions
            )

        st.markdown("---")

        # ==========================
        # FILTERS
        # ==========================

        st.subheader("🔍 Filters")

        categories = st.multiselect(
            "Category",
            options=df["category"].unique(),
            default=df["category"].unique()
        )

        filtered_df = df[
            df["category"].isin(categories)
        ]

        # ==========================
        # CHART DATA
        # ==========================

        category_total = (
            filtered_df.groupby("category")["amount"]
            .sum()
            .reset_index()
        )

        # ==========================
        # PIE + BAR CHART
        # ==========================

        col1, col2 = st.columns(2)

        with col1:

            pie = px.pie(
                category_total,
                names="category",
                values="amount",
                hole=0.5,
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
                title="Expenses by Category"
            )

            st.plotly_chart(
                bar,
                use_container_width=True
            )

        st.markdown("---")

        # ==========================
        # MONTHLY TREND
        # ==========================

        monthly = (
            filtered_df.groupby(
                filtered_df["date"].dt.to_period("M")
            )["amount"]
            .sum()
            .reset_index()
        )

        monthly["date"] = (
            monthly["date"]
            .astype(str)
        )

        trend = px.line(
            monthly,
            x="date",
            y="amount",
            markers=True,
            title="📈 Monthly Spending Trend"
        )

        st.plotly_chart(
            trend,
            use_container_width=True
        )

        st.markdown("---")

        # ==========================
        # DAILY TREND
        # ==========================

        daily = (
            filtered_df.groupby("date")["amount"]
            .sum()
            .reset_index()
        )

        daily_chart = px.area(
            daily,
            x="date",
            y="amount",
            title="📅 Daily Spending Trend"
        )

        st.plotly_chart(
            daily_chart,
            use_container_width=True
        )

        st.markdown("---")

        # ==========================
        # CATEGORY SUMMARY
        # ==========================

        st.subheader(
            "📊 Category Summary"
        )

        summary = (
            filtered_df
            .groupby("category")["amount"]
            .agg(
                [
                    "sum",
                    "mean",
                    "count",
                    "max",
                    "min"
                ]
            )
            .reset_index()
        )

        summary.columns = [
            "Category",
            "Total",
            "Average",
            "Transactions",
            "Maximum",
            "Minimum"
        ]

        st.dataframe(
            summary,
            use_container_width=True
        )

        st.markdown("---")

        # ==========================
        # TOP EXPENSES
        # ==========================

        st.subheader(
            "🏆 Top 10 Expenses"
        )

        top_expenses = (
            filtered_df
            .sort_values(
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

        # ==========================
        # FINANCIAL INSIGHTS
        # ==========================

        st.subheader(
            "🧠 Insights"
        )

        st.info(
            f"""
            💰 Total Spending: ₹{total_expense:,.0f}

            🔥 Highest Category: {highest_category}

            📊 Average Transaction: ₹{avg_expense:,.0f}

            🧾 Total Transactions: {total_transactions}
            """
        )

        # ==========================
        # RAW DATA
        # ==========================

        with st.expander(
            "📂 View Raw Data"
        ):

            st.dataframe(
                filtered_df,
                use_container_width=True
            )

    except Exception as e:

        st.error(
            f"Error: {e}"
        )

        st.stop()