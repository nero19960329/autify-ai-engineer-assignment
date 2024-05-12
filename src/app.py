from fastapi import FastAPI, Request, Depends, HTTPException
from fastapi.responses import StreamingResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from src.database import engine, get_db
from src.runner import run_python_code
from src import models, crud, schemas

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

templates = Jinja2Templates(directory="src/templates")


@app.get("/")
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


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


@app.put("/snippets/{snippet_id}", response_model=schemas.Snippet)
async def update_snippet(
    snippet_id: int, snippet_data: schemas.SnippetUpdate, db: Session = Depends(get_db)
):
    db_snippet = crud.update_snippet(db, snippet_id, snippet_data)
    if not db_snippet:
        raise HTTPException(status_code=404, detail="Snippet not found")
    return db_snippet


@app.delete("/snippets/{snippet_id}", status_code=204)
async def delete_snippet(snippet_id: int, db: Session = Depends(get_db)):
    if not crud.delete_snippet(db, snippet_id):
        raise HTTPException(status_code=404, detail="Snippet not found")


async def fake_stream_data(data: str):
    import asyncio

    for char in data:
        yield char
        await asyncio.sleep(0.01)  # Simulate slow streaming


@app.post("/generate_title")
async def generate_title(title_gen_data: schemas.TitleGenRequest):
    fake_title = "Add two numbers"
    return StreamingResponse(
        fake_stream_data(fake_title), media_type="application/json"
    )


@app.post("/generate_code")
async def generate_code(code_gen_data: schemas.CodeGenRequest):
    fake_code = "def sum(a, b):\n    return a + b"
    return StreamingResponse(fake_stream_data(fake_code), media_type="application/json")


@app.post("/detect_language", response_model=schemas.LanguageDetResponse)
async def detect_language(language_gen_data: schemas.LanguageDetRequest):
    return {"language": "python"}


@app.post("/generate_code_from_feedback")
async def generate_code_from_feedback(feedback_data: schemas.CodeFeedbackRequest):
    fake_code = "def sum(a: int, b: int) -> int:\n    return a + b"
    return StreamingResponse(fake_stream_data(fake_code), media_type="application/json")


@app.post("/generate_tests")
async def generate_tests(test_gen_data: schemas.TestGenRequest):
    fake_code = "assert sum(1, 2) == 3"
    return StreamingResponse(fake_stream_data(fake_code), media_type="application/json")


@app.post("/generate_tests_from_feedback")
async def generate_tests_from_feedback(feedback_data: schemas.TestsFeedbackRequest):
    fake_code = "assert sum(1, 2) == 3\nassert sum(2, 3) == 5"
    return StreamingResponse(fake_stream_data(fake_code), media_type="application/json")


@app.post("/run_tests", status_code=200)
async def run_tests(test_run_data: schemas.TestRunRequest):
    if test_run_data.language != "python":
        raise HTTPException(
            status_code=400,
            detail="Only Python snippets are supported for running tests",
        )

    result = run_python_code(test_run_data.code, test_run_data.test_code)
    return result
