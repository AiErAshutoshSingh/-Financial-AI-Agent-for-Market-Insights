import streamlit as st
from groq import Groq
from dotenv import load_dotenv
from datetime import datetime
import os

from utils.prompts import SYSTEM_PROMPT

# =====================
# CONFIG
# =====================

load_dotenv()

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)

st.set_page_config(
    page_title="FinanceGPT Pro",
    page_icon="💰",
    layout="wide"
)

# =====================
# LOAD CSS
# =====================

def load_css():
    try:
        with open("assets/style.css") as f:
            st.markdown(
                f"<style>{f.read()}</style>",
                unsafe_allow_html=True
            )
    except:
        pass

load_css()

# =====================
# SIDEBAR
# =====================

with st.sidebar:

    st.title("💰 FinanceGPT Pro")

    st.markdown("---")

    st.subheader("Quick Actions")

    if st.button("🗑 Clear Chat"):
        st.session_state.messages = []
        st.rerun()

    st.markdown("---")

    st.subheader("Suggested Questions")

    suggestions = [
        "How can I save ₹5000 per month?",
        "Create a student budget plan",
        "Explain SIP investment",
        "How should I start investing?",
        "What is an emergency fund?"
    ]

    for q in suggestions:
        st.caption("• " + q)

    st.markdown("---")

    st.info(
        """
        FinanceGPT Pro

        Powered by:
        - Llama 3.3
        - Streamlit
        """
    )

# =====================
# HEADER
# =====================

st.title("💰 FinanceGPT Pro")

st.caption(
    "Your AI-Powered Personal Finance Assistant"
)

# =====================
# KPI SECTION
# =====================

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "Budget Planning",
        "AI"
    )

with col2:
    st.metric(
        "Investment Help",
        "24/7"
    )

with col3:
    st.metric(
        "Financial Education",
        "Unlimited"
    )

st.markdown("---")

# =====================
# CHAT HISTORY
# =====================

if "messages" not in st.session_state:

    st.session_state.messages = [
        {
            "role": "assistant",
            "content":
            """
👋 Welcome to FinanceGPT Pro!

I can help you with:

✅ Budget Planning

✅ Savings Strategies

✅ SIP & Mutual Funds

✅ Investment Basics

✅ Tax Concepts

Ask me any finance question.
            """
        }
    ]

# DISPLAY CHAT

for msg in st.session_state.messages:

    with st.chat_message(msg["role"]):

        st.write(msg["content"])

# =====================
# USER INPUT
# =====================

prompt = st.chat_input(
    "Ask a finance question..."
)

if prompt:

    timestamp = datetime.now().strftime(
        "%H:%M"
    )

    st.session_state.messages.append(
        {
            "role": "user",
            "content": f"{prompt}\n\n🕒 {timestamp}"
        }
    )

    with st.chat_message("user"):
        st.write(prompt)

    with st.chat_message("assistant"):

        with st.spinner(
            "Analyzing financial query..."
        ):

            messages = [
                {
                    "role": "system",
                    "content": SYSTEM_PROMPT
                }
            ]

            for m in st.session_state.messages:

                role = (
                    "assistant"
                    if m["role"] == "assistant"
                    else "user"
                )

                messages.append(
                    {
                        "role": role,
                        "content": m["content"]
                    }
                )

            response = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=messages,
                temperature=0.4,
                max_tokens=1000
            )

            answer = (
                response
                .choices[0]
                .message
                .content
            )

            st.write(answer)

    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": answer
        }
    )