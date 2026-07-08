from pathlib import Path

from fastapi import FastAPI
from routers import auth, company, job, chat,rag
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse

from database import Base, engine
from models import company as company_model, job as job_model, users as user_model
from routers import auth, chat, company, job

app = FastAPI()
BASE_DIR = Path(__file__).resolve().parent.parent
INDEX_HTML_PATH = BASE_DIR / "index.html"

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def on_startup():
    Base.metadata.create_all(bind=engine)

app.include_router(auth.router)
app.include_router(company.router)
app.include_router(job.router)
app.include_router(chat.router)

@app.get("/", response_class=HTMLResponse)
def read_root():
    return INDEX_HTML_PATH.read_text(encoding="utf-8")

@app.get("/about")
def read_about():
    return {"about": "This is about page"}

@app.get("/contact")
def read_contact():
    return {"contact": "This is contact page"}