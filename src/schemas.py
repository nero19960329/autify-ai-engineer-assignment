from datetime import datetime

from pydantic import BaseModel, ConfigDict


class SnippetCreate(BaseModel):
    title: str = ""
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


class CodeGenRequest(BaseModel):
    description: str


class CodeGenResponse(BaseModel):
    code: str
    language: str


class TitleGenRequest(BaseModel):
    description: str


class TitleGenResponse(BaseModel):
    title: str


class CodeFeedbackRequest(BaseModel):
    code: str
    feedback: str


class TestGenRequest(BaseModel):
    code: str


class TestGenResponse(BaseModel):
    test_code: str


class TestsFeedbackRequest(BaseModel):
    code: str
    test_code: str
    feedback: str


class TestRunRequest(BaseModel):
    code: str
    test_code: str
    language: str
