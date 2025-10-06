README.md
# AI SQL Assistant — Prototype

1. Copy `.env.example` -> `.env` and set OPENAI_API_KEY.
2. Create sample DB:
   python create_sample_db.py
3. Start backend:
   uvicorn backend.app:app --reload --port 8000
4. Start Streamlit UI:
   streamlit run frontend/streamlit_app.py
5. In the UI, paste the example schema and ask questions like:
   "Which customers spent the most in 2023?"
