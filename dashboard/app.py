"""Streamlit frontend for the GenAI-powered business chatbot."""

import sys
from pathlib import Path

import pandas as pd
import streamlit as st


PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.utils import handle_query


st.set_page_config(page_title="AI Demand Assistant", layout="wide")

st.markdown(
    """
    <style>
    .block-container {
        max-width: 1100px;
        padding-top: 2rem;
    }
    [data-testid="stChatMessage"] {
        border-radius: 10px;
        padding: 0.35rem 0.5rem;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# Header
col1, col2 = st.columns([1, 5])
with col1:
    st.image("assets/Trailset_logo.png", width=50)
    if st.button("Reset to Home", key="logo_button"):
        st.session_state.messages = [
            {
                "role": "assistant",
                "content": {
                    "type": "text",
                    "message": "Hi. Ask me things like 'show top products', 'category sales', 'forecast TE001', or 'show forecast chart'.",
                    "data": None,
                },
            }
        ]
with col2:
    st.title("AI Demand Forecast Assistant")
    st.caption("Powered by TrailEdge")

# Body
# Suggested prompts
st.markdown("### Suggested Prompts")
col1, col2, col3 = st.columns(3)
with col1:
    if st.button("Show top products", key="top_products"):
        prompt = "show top products"
with col2:
    if st.button("Category sales", key="category_sales"):
        prompt = "category sales"
with col3:
    if st.button("Forecast TE001", key="forecast_te001"):
        prompt = "forecast TE001"

# Category quick-start buttons
st.markdown("### Quick Start by Category")
categories = ["Electronics", "Clothing", "Home Goods", "Sports"]
cols = st.columns(len(categories))
for i, cat in enumerate(categories):
    with cols[i]:
        if st.button(f"{cat} Sales", key=f"cat_{cat}"):
            prompt = f"sales for {cat}"

if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": {
                "type": "text",
                "message": "Hi. Ask me things like 'show top products', 'category sales', 'forecast TE001', or 'show forecast chart'.",
                "data": None,
            },
        }
    ]


def render_response(response: dict) -> None:
    """Render a structured chatbot response."""
    message = response.get("message", "")
    response_type = response.get("type", "text")
    data = response.get("data")

    if message:
        st.write(message)

    if response_type == "table" and data is not None:
        st.dataframe(pd.DataFrame(data), use_container_width=True)
    elif response_type == "image" and data:
        st.image(data, use_container_width=True)
    elif response_type == "plot" and data is not None:
        st.pyplot(data)
    elif response_type == "text" and not message:
        st.write(data or "")


prompt = None

# Messages
for item in st.session_state.messages:
    with st.chat_message(item["role"]):
        content = item["content"]
        if isinstance(content, dict):
            render_response(content)
        else:
            st.write(content)

# Chat input
prompt_input = st.chat_input("Ask a business question")

if prompt_input:
    prompt = prompt_input

if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

    response = handle_query(prompt)
    st.session_state.messages.append({"role": "assistant", "content": response})
    with st.chat_message("assistant"):
        render_response(response)
