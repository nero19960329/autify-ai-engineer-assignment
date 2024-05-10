from sqlalchemy.orm import Session

from src import models, schemas


def create_snippet(db: Session, snippet_data: schemas.SnippetCreate) -> models.Snippet:
    db_snippet = models.Snippet(**snippet_data.model_dump())
    db.add(db_snippet)
    db.commit()
    db.refresh(db_snippet)
    return db_snippet
