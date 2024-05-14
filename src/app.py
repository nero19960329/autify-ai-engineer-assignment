from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates

from src.database import engine
from src.routers import snippets, generate, run
from src import models

models.Base.metadata.create_all(bind=engine)

app = FastAPI()
app.include_router(snippets.router)
app.include_router(generate.router)
app.include_router(run.router)

templates = Jinja2Templates(directory="src/templates")


@app.get("/")
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})
