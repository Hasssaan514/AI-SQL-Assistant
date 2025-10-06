# app.py
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from backend.db import is_safe_select, run_readonly_query
from backend.llm import nl_to_sql

app = FastAPI(title="AI SQL Assistant")

class QueryRequest(BaseModel):
    question: str
    schema: str
    max_results: int = 200

class QueryResponse(BaseModel):
    sql: str
    columns: list | None = None
    rows: list | None = None
    error: str | None = None

@app.post("/query", response_model=QueryResponse)
async def generate_and_run(req: QueryRequest):
    sql = nl_to_sql(req.question, req.schema)
    if sql.strip() == "CANNOT_ANSWER_WITH_SCHEMA":
        raise HTTPException(status_code=400, detail="Question cannot be answered with the provided schema.")

    if not is_safe_select(sql):
        raise HTTPException(status_code=400, detail="Generated query failed safety checks. Only read-only SELECTs allowed.")

    result = run_readonly_query(sql, limit=req.max_results)
    if "error" in result:
        return QueryResponse(sql=sql, error=result["error"]
        )

    return QueryResponse(sql=sql, columns=list(result["columns"]), rows=result["rows"])
