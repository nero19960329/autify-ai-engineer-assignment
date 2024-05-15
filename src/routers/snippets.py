"""
This module defines the endpoints for CRUD operations on code snippets.
It includes endpoints for creating, retrieving, updating, and deleting snippets.
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from src.database import get_db
from src.logger import logger
from src import crud, schemas

router = APIRouter(prefix="/snippets", tags=["snippets"])


@router.get("/", response_model=list[schemas.Snippet])
async def get_snippets(db: Session = Depends(get_db)):
    """
    Retrieves a list of active snippets.

    Args:
        db (Session): The database session.

    Returns:
        list[schemas.Snippet]: The list of active snippets.
    """
    return crud.get_snippets(db)


@router.post("/", response_model=schemas.Snippet)
async def create_snippet(
    snippet_data: schemas.SnippetCreate, db: Session = Depends(get_db)
):
    """
    Creates a new snippet.

    Args:
        snippet_data (schemas.SnippetCreate): The data for the new snippet.
        db (Session): The database session.

    Returns:
        schemas.Snippet: The created snippet.
    """
    return crud.create_snippet(db, snippet_data)


@router.get("/{snippet_id}", response_model=schemas.Snippet)
async def get_snippet(snippet_id: int, db: Session = Depends(get_db)):
    """
    Retrieves a snippet by its ID.

    Args:
        snippet_id (int): The ID of the snippet to retrieve.
        db (Session): The database session.

    Returns:
        schemas.Snippet: The retrieved snippet.

    Raises:
        HTTPException: If the snippet is not found.
    """
    db_snippet = crud.get_snippet(db, snippet_id)
    if not db_snippet:
        logger.warning(f"Snippet not found: {snippet_id}")
        raise HTTPException(status_code=404, detail="Snippet not found")
    return db_snippet


@router.put("/{snippet_id}", response_model=schemas.Snippet)
async def update_snippet(
    snippet_id: int, snippet_data: schemas.SnippetUpdate, db: Session = Depends(get_db)
):
    """
    Updates a snippet by its ID.

    Args:
        snippet_id (int): The ID of the snippet to update.
        snippet_data (schemas.SnippetUpdate): The updated data for the snippet.
        db (Session): The database session.

    Returns:
        schemas.Snippet: The updated snippet.

    Raises:
        HTTPException: If the snippet is not found.
    """
    db_snippet = crud.update_snippet(db, snippet_id, snippet_data)
    if not db_snippet:
        logger.warning(f"Snippet not found: {snippet_id}")
        raise HTTPException(status_code=404, detail="Snippet not found")
    return db_snippet


@router.delete("/{snippet_id}", status_code=204)
async def delete_snippet(snippet_id: int, db: Session = Depends(get_db)):
    """
    Deletes a snippet by its ID.

    Args:
        snippet_id (int): The ID of the snippet to delete.
        db (Session): The database session.

    Raises:
        HTTPException: If the snippet is not found.
    """
    if not crud.delete_snippet(db, snippet_id):
        logger.warning(f"Snippet not found: {snippet_id}")
        raise HTTPException(status_code=404, detail="Snippet not found")
