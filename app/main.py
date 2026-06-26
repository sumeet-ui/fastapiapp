from fastapi import FastAPI
from routers import company,job

app = FastAPI()

app.include_router(company.router)
app.include_router(job.router)

@app.get("/")
def read_rooot():
    return{"Hello":"World"}


@app.get("/about")
def read_about():
    return{"about": "this is about gobi"}

@app.get("/contact")
def read_contact():
    return{"contact": "this contact from gobi+"}