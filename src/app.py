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
