"""
This module defines the endpoints for CRUD operations on code snippets.
It includes endpoints for creating, retrieving, updating, and deleting snippets.
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from src.database import get_db
from src import crud, schemas

router = APIRouter(prefix="/snippets", tags=["snippets"])


@router.get("/", response_model=list[schemas.Snippet])
async def get_snippets(db: Session = Depends(get_db)):
    return crud.get_snippets(db)


@router.post("/", response_model=schemas.Snippet)
async def create_snippet(
    snippet_data: schemas.SnippetCreate, db: Session = Depends(get_db)
):
    return crud.create_snippet(db, snippet_data)


@router.get("/{snippet_id}", response_model=schemas.Snippet)
async def get_snippet(snippet_id: int, db: Session = Depends(get_db)):
    db_snippet = crud.get_snippet(db, snippet_id)
    if not db_snippet:
        raise HTTPException(status_code=404, detail="Snippet not found")
    return db_snippet


@router.put("/{snippet_id}", response_model=schemas.Snippet)
async def update_snippet(
    snippet_id: int, snippet_data: schemas.SnippetUpdate, db: Session = Depends(get_db)
):
    db_snippet = crud.update_snippet(db, snippet_id, snippet_data)
    if not db_snippet:
        raise HTTPException(status_code=404, detail="Snippet not found")
    return db_snippet


@router.delete("/{snippet_id}", status_code=204)
async def delete_snippet(snippet_id: int, db: Session = Depends(get_db)):
    if not crud.delete_snippet(db, snippet_id):
        raise HTTPException(status_code=404, detail="Snippet not found")
