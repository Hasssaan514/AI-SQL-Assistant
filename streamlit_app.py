# frontend/streamlit_app.py
import streamlit as st
import requests
import json

# --- PAGE SETUP ---
st.set_page_config(page_title="AI SQL Assistant", page_icon="🤖", layout="wide")

# --- CUSTOM STYLES ---
st.markdown("""
    <style>
        body {
            background-color: #0e1117;
        }
        .main {
            background-color: #111418;
            color: #f0f2f6;
        }
        .stTextArea textarea {
            background-color: #1e2126 !important;
            color: #f0f2f6 !important;
            border-radius: 10px;
            border: 1px solid #333;
        }
        .stButton>button {
            background: linear-gradient(90deg, #00b4db, #0083b0);
            color: white;
            border: none;
            border-radius: 10px;
            padding: 0.6em 1.5em;
            font-weight: 600;
            transition: 0.3s;
        }
        .stButton>button:hover {
            transform: scale(1.03);
            background: linear-gradient(90deg, #0083b0, #00b4db);
        }
        .block-container {
            padding-top: 1rem;
        }
        h1 {
            text-align: center;
            background: linear-gradient(90deg, #00b4db, #0083b0);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            font-weight: 800;
        }
        .sql-box {
            background-color: #1e1e1e;
            padding: 15px;
            border-radius: 8px;
            border: 1px solid #444;
            color: #00bfff;
            font-family: monospace;
        }
    </style>
""", unsafe_allow_html=True)

# --- HEADER ---
st.title("🤖 AI-Powered SQL Query Assistant")
st.markdown("<p style='text-align:center;color:#888;'>Ask questions in plain English and watch them turn into SQL instantly.</p>", unsafe_allow_html=True)
st.markdown("---")

# --- BACKEND CONFIG ---
BACKEND_URL = st.secrets.get("BACKEND_URL", "http://localhost:8000/query")

# --- EXAMPLE SCHEMA ---
with st.expander("📘 Example Database Schema"):
    example_schema = """
Tables:
customers(id, name, email, city)
orders(id, customer_id, amount, order_date, status)
"""
    st.code(example_schema, language="sql")

# --- INPUTS ---
col1, col2 = st.columns([3, 1])

with col1:
    question = st.text_area("💬 Ask a question", placeholder="e.g. Show all customers who spent more than $500...", height=120)

with col2:
    max_results = st.number_input("📊 Max rows", min_value=10, max_value=1000, value=200, step=10)

schema = st.text_area("🧩 Database schema", value=example_schema, height=120)

# --- RUN BUTTON ---
if st.button("🚀 Generate & Run SQL", use_container_width=True):
    if not question.strip():
        st.warning("⚠️ Please enter a question before running.")
    else:
        payload = {"question": question, "schema": schema, "max_results": max_results}
        with st.spinner("🔍 Thinking... Generating SQL and running query..."):
            try:
                resp = requests.post(BACKEND_URL, json=payload, timeout=120)
                if resp.status_code != 200:
                    st.error(f"❌ Backend error: {resp.status_code} — {resp.text}")
                else:
                    data = resp.json()

                    # --- SHOW GENERATED SQL ---
                    st.markdown("### 🧠 Generated SQL Query")
                    st.markdown(f"<div class='sql-box'>{data['sql']}</div>", unsafe_allow_html=True)

                    # --- HANDLE ERRORS ---
                    if data.get("error"):
                        st.error(f"⚠️ Query execution error: {data['error']}")
                    else:
                        rows = data.get("rows", [])
                        if rows:
                            st.markdown("### 📈 Query Results")
                            st.dataframe(rows, use_container_width=True)
                        else:
                            st.info("ℹ️ Query returned no rows.")
            except Exception as e:
                st.exception(e)

# --- FOOTER ---
st.markdown("---")
st.markdown(
    "<p style='text-align:center;color:gray;'>✨ Built with Streamlit & AI — Prototype v1.0</p>",
    unsafe_allow_html=True
)
