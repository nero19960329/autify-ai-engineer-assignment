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
    return templates.TemplateResponse("index.html", {"request": request})


fake_snippets = [
    {
        "id": 1,
        "title": "Even Tester",
        "language": "Python",
        "code": "def is_even(n):\n    return n % 2 == 0",
        "tests": "assert is_even(2)\nassert not is_even(3)",
        "test_result": "success",
        "test_result_message": "Code Executed Successfully",
    },
    {
        "id": 2,
        "title": "Prime number generator",
        "language": "Javascript",
        "code": "function isPrime(n) {\n  // ...\n}",
        "tests": "console.assert(isPrime(2));\nconsole.assert(!isPrime(4));",
    },
]


@app.get("/snippets")
async def get_snippets():
    return fake_snippets


@app.post("/snippets")
async def create_snippet(snippet):
    # Fake creating a new snippet
    return {
        "id": 3,
        "title": "New Snippet",
        "language": "python",
        "description": "",
        "code": "",
        "code_feedback": "",
        "tests": "",
        "tests_feedback": "",
        "test_result": "",
        "test_result_message": "",
    }


@app.get("/snippets/{snippet_id}")
async def get_snippet(snippet_id: int):
    # Fake retrieving a snippet by ID
    return fake_snippets[snippet_id - 1]


@app.put("/snippets/{snippet_id}")
async def update_snippet(snippet_id: int, updated_snippet):
    # Fake updating a snippet
    return {
        "id": snippet_id,
        "title": "Updated Snippet",
        "language": "python",
        "description": "",
        "code": "# Updated code",
        "code_feedback": "",
        "tests": "# Updated tests",
        "tests_feedback": "",
        "test_result": "",
        "test_result_message": "",
    }


@app.delete("/snippets/{snippet_id}")
async def delete_snippet(snippet_id: int):
    # Fake deleting a snippet
    return {"message": f"Snippet with ID {snippet_id} has been deleted"}


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
