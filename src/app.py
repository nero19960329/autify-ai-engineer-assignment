from fastapi import FastAPI, Request, Depends
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from src.database import SessionLocal, engine
from src import models

models.Base.metadata.create_all(bind=engine)

app = FastAPI()
templates = Jinja2Templates(directory="src/templates")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
async def home(request: Request):
    return templates.TemplateResponse("home.html", {"request": request})


@app.get("/test-db")
async def test_db(db: Session = Depends(get_db)):
    test_snippet = models.CodeSnippet(
        title="Test Snippet", language="Python", code="print('Hello, World!')"
    )
    db.add(test_snippet)
    db.commit()
    db.refresh(test_snippet)

    retrieved_snippet = (
        db.query(models.CodeSnippet)
        .filter(models.CodeSnippet.id == test_snippet.id)
        .first()
    )

    return {
        "created_snippet": {
            "id": test_snippet.id,
            "title": test_snippet.title,
            "language": test_snippet.language,
            "code": test_snippet.code,
        },
        "retrieved_snippet": {
            "id": retrieved_snippet.id,
            "title": retrieved_snippet.title,
            "language": retrieved_snippet.language,
            "code": retrieved_snippet.code,
        },
    }
