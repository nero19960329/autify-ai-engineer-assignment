from fastapi import FastAPI, Request, Depends, HTTPException
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from src.database import engine, get_db
from src import models, crud, schemas

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

templates = Jinja2Templates(directory="src/templates")


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


@app.get("/snippets", response_model=list[schemas.Snippet])
async def get_snippets(db: Session = Depends(get_db)):
    return crud.get_snippets(db)


@app.post("/snippets", response_model=schemas.Snippet)
async def create_snippet(
    snippet_data: schemas.SnippetCreate, db: Session = Depends(get_db)
):
    return crud.create_snippet(db, snippet_data)


@app.get("/snippets/{snippet_id}", response_model=schemas.Snippet)
async def get_snippet(snippet_id: int, db: Session = Depends(get_db)):
    db_snippet = crud.get_snippet(db, snippet_id)
    if not db_snippet:
        raise HTTPException(status_code=404, detail="Snippet not found")
    return db_snippet


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
