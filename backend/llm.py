import os
from dotenv import load_dotenv
import google.generativeai as genai

# Load environment variables
load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")
if not API_KEY:
    raise RuntimeError("GEMINI_API_KEY not set in .env")

# Configure Gemini
genai.configure(api_key=API_KEY)

SCHEMA_PROMPT = """
You are an expert assistant that converts a natural language question into a SQL SELECT query.
Requirements:
- Only return a single SQL query, no explanation.
- The query MUST be a SELECT statement (no INSERT/UPDATE/DELETE/ALTER/DROP).
- Use the following database schema exactly as given.
- Use standard SQL compatible with SQLite (avoid proprietary functions).
- If the user query cannot be answered with the given schema, respond exactly with: CANNOT_ANSWER_WITH_SCHEMA

Schema:
{schema}

User question:
{question}
"""

def nl_to_sql(question: str, schema: str, model="gemini-2.5-flash", max_tokens=512):
    """
    Returns the generated SQL string or 'CANNOT_ANSWER_WITH_SCHEMA'
    """
    prompt = SCHEMA_PROMPT.format(schema=schema, question=question)

    # Call Gemini
    model = genai.GenerativeModel(model)
    response = model.generate_content(prompt)

    if not response.candidates:
        return "CANNOT_ANSWER_WITH_SCHEMA"

    text = response.candidates[0].content.parts[0].text.strip()

    # Remove code fences if Gemini returns markdown blocks
    if text.startswith("```"):
        text = "\n".join(text.splitlines()[1:-1])

    return text
