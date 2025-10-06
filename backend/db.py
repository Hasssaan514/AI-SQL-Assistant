# backend/db.py
from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError
import os
from dotenv import load_dotenv
import sqlparse

load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./sample.db")

engine = create_engine(DATABASE_URL, future=True)

FORBIDDEN_KEYWORDS = {"drop", "delete", "alter", "insert", "update", "create", "replace", "truncate", "grant", "revoke"}

def is_safe_select(sql: str) -> bool:
    """
    A defensive check:
    - Must start with SELECT (after removing comments)
    - Must not contain forbidden keywords
    - Must be parseable by sqlparse
    This is a heuristic — in production use DB-specific permissions + prepared statements + query sandboxes.
    """
    stripped = sql.strip().lower()
    # remove leading comments
    parsed = sqlparse.format(sql, strip_comments=True).strip().lower()
    if not parsed.startswith("select"):
        return False
    for kw in FORBIDDEN_KEYWORDS:
        if kw in parsed and not parsed.startswith(kw):  # allow 'select * from mytable where ...' containing 'select' obviously
            # If keyword exists anywhere but the query doesn't start with that keyword,
            # still reject because user shouldn't be able to run DDL/DML fragments.
            return False
    # Additional parse sanity check
    try:
        parsed_list = sqlparse.parse(sql)
        if not parsed_list:
            return False
    except Exception:
        return False
    return True

def run_readonly_query(sql_text: str, limit: int = 1000):
    """
    Execute a SELECT query and return a list of dict rows and column names.
    We wrap the query to enforce a safe LIMIT if none is present.
    """
    sql = sql_text.strip().rstrip(";")
    # If there's no "limit" token, append a limit to avoid huge scans.
    if "limit" not in sql.lower():
        sql = f"SELECT * FROM ({sql}) LIMIT {limit}"
    try:
        with engine.connect() as conn:
            result = conn.execute(text(sql))
            columns = result.keys()
            rows = [dict(row) for row in result.fetchall()]
        return {"columns": columns, "rows": rows}
    except SQLAlchemyError as e:
        return {"error": str(e)}
