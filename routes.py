# app/routes.py

from fastapi import APIRouter , Request
from database import SessionLocal
from pydantic import BaseModel
from mcp_agent.agent import ask_agent
from mcp_agent.groq_client import client
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

 
router = APIRouter()
class AskRequest(BaseModel):
    question: str


templates = Jinja2Templates(directory="./mcp_agent/templates")

@router.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@router.post("/ask")
async def ask(request: AskRequest):
    result = await ask_agent(request.question)
    return {"response": result}
 

 
@router.post("/query-llm")
async def query_llm(request: Request):
    body = await request.json()
    question = body.get("question")

    prompt = f"""You are a helpful AI assistant. Generate a PostgreSQL query to answer the following:
    
    Question: {question}
    
    Only return the SQL query and nothing else."""
 
    response = client.chat.completions.create(
		model="llama-3.3-70b-versatile",
		messages=[
			# {"role": "system", "content": "You are an expert MCQ creator."},
			{"role": "user", "content": prompt}
		], 
	)

    sql_query = response.choices[0].message.content.strip()
    try:
        conn = SessionLocal()
        cursor = conn.cursor()
        cursor.execute(sql_query)
        result = cursor.fetchall()
        cursor.close()
        conn.close()
        return {"query": sql_query, "result": result}
    except Exception as e:
        return {"query": sql_query, "error": str(e)}
    