import os

from fastapi import FastAPI, Request, Depends, HTTPException
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from src.database import engine, get_db
from src.runner import run_python_code
from src.routers import snippets, generate_fake
from src import models, crud, schemas

models.Base.metadata.create_all(bind=engine)

app = FastAPI()
app.include_router(snippets.router)
if os.getenv("ENV") == "test":
    app.include_router(generate_fake.router)

templates = Jinja2Templates(directory="src/templates")


@app.get("/")
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/run_tests", status_code=200)
async def run_tests(
    test_run_data: schemas.TestRunRequest, db: Session = Depends(get_db)
):
    if test_run_data.language != "python":
        raise HTTPException(
            status_code=400,
            detail="Only Python snippets are supported for running tests",
        )

    db_snippet = crud.get_snippet(db, test_run_data.snippet_id)
    result = run_python_code(test_run_data.code, test_run_data.test_code)
    db_snippet.test_result = result["result"]
    db_snippet.test_result_message = result["message"]
    db.commit()
    return result
