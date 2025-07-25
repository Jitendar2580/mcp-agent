# app/main.py
from fastapi import FastAPI
from routes import router 

app = FastAPI(title="Smart AI Assistant")
 
app.include_router(router)