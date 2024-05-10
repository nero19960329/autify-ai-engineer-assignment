from datetime import datetime

from pydantic import BaseModel, ConfigDict


class SnippetCreate(BaseModel):
    title: str = "New Snippet"
    language: str = ""
    code: str = ""


class SnippetUpdate(BaseModel):
    title: str | None = None
    language: str | None = None
    code: str | None = None


class Snippet(SnippetCreate):
    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: datetime
    updated_at: datetime
