from sqlalchemy.orm import Session

from src import models, schemas


def create_snippet(db: Session, snippet_data: schemas.SnippetCreate) -> models.Snippet:
    db_snippet = models.Snippet(**snippet_data.model_dump())
    db.add(db_snippet)
    db.commit()
    db.refresh(db_snippet)
    return db_snippet


def get_snippet(db: Session, snippet_id: int) -> models.Snippet:
    return db.query(models.Snippet).filter(models.Snippet.id == snippet_id).first()


def get_snippets(db: Session, skip: int = 0, limit: int = 100) -> list[models.Snippet]:
    return db.query(models.Snippet).offset(skip).limit(limit).all()


def update_snippet(
    db: Session, snippet_id: int, snippet_data: schemas.SnippetUpdate
) -> models.Snippet:
    db_snippet = (
        db.query(models.Snippet).filter(models.Snippet.id == snippet_id).first()
    )
    if not db_snippet:
        return None
    for key, value in snippet_data.model_dump().items():
        if value:
            setattr(db_snippet, key, value)
    db.commit()
    db.refresh(db_snippet)
    return db_snippet


def delete_snippet(db: Session, snippet_id: int) -> bool:
    db_snippet = (
        db.query(models.Snippet).filter(models.Snippet.id == snippet_id).first()
    )
    if db_snippet:
        db.delete(db_snippet)
        db.commit()
        return True
    return False
