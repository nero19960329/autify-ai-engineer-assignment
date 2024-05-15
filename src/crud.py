"""
This module provides CRUD (Create, Read, Update, Delete) operations for the Snippet model.
It interacts with the database using SQLAlchemy sessions.
"""

from sqlalchemy.orm import Session

from src import models, schemas


def create_snippet(db: Session, snippet_data: schemas.SnippetCreate) -> models.Snippet:
    """
    Creates a new snippet in the database.

    Args:
        db (Session): The database session.
        snippet_data (schemas.SnippetCreate): The snippet data to create.

    Returns:
        models.Snippet: The created snippet.
    """
    db_snippet = models.Snippet(**snippet_data.model_dump())
    db.add(db_snippet)
    db.commit()
    db.refresh(db_snippet)
    return db_snippet


def get_snippet(db: Session, snippet_id: int) -> models.Snippet:
    """
    Retrieves a snippet by its ID.

    Args:
        db (Session): The database session.
        snippet_id (int): The ID of the snippet to retrieve.

    Returns:
        models.Snippet: The retrieved snippet, or None if not found.
    """
    return (
        db.query(models.Snippet)
        .filter(models.Snippet.id == snippet_id)
        .filter(models.Snippet.is_active == True)
        .first()
    )


def get_snippets(db: Session, skip: int = 0, limit: int = 100) -> list[models.Snippet]:
    """
    Retrieves a list of active snippets, with optional pagination.

    Args:
        db (Session): The database session.
        skip (int, optional): The number of snippets to skip. Defaults to 0.
        limit (int, optional): The maximum number of snippets to retrieve. Defaults to 100.

    Returns:
        list[models.Snippet]: The list of retrieved snippets.
    """
    return (
        db.query(models.Snippet)
        .filter(models.Snippet.is_active == True)
        .order_by(models.Snippet.updated_at.desc())
        .offset(skip)
        .limit(limit)
        .all()
    )


def update_snippet(
    db: Session, snippet_id: int, snippet_data: schemas.SnippetUpdate
) -> models.Snippet:
    """
    Updates an existing snippet in the database.

    Args:
        db (Session): The database session.
        snippet_id (int): The ID of the snippet to update.
        snippet_data (schemas.SnippetUpdate): The updated snippet data.

    Returns:
        models.Snippet: The updated snippet, or None if not found.
    """
    db_snippet = get_snippet(db, snippet_id)
    if not db_snippet:
        return None
    for key, value in snippet_data.model_dump().items():
        if value:
            setattr(db_snippet, key, value)
    db.commit()
    db.refresh(db_snippet)
    return db_snippet


def delete_snippet(db: Session, snippet_id: int) -> bool:
    """
    Marks a snippet as inactive (soft delete).

    Args:
        db (Session): The database session.
        snippet_id (int): The ID of the snippet to delete.

    Returns:
        bool: True if the snippet was deleted, False otherwise.
    """
    db_snippet = get_snippet(db, snippet_id)
    if db_snippet:
        db_snippet.is_active = False
        db.commit()
        return True
    return False
