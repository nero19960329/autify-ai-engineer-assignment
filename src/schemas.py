from pydantic import BaseModel, ConfigDict


class SnippetCreate(BaseModel):
    title: str = "New Snippet"
    language: str = ""
    code: str = ""


class Snippet(SnippetCreate):
    model_config = ConfigDict(from_attributes=True)

    id: int