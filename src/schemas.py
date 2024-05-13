from datetime import datetime

from pydantic import BaseModel, ConfigDict


class SnippetCreate(BaseModel):
    title: str = ""
    language: str = ""
    description: str = ""
    code: str = ""
    feedback: str = ""
    test_code: str = ""
    test_feedback: str = ""


class SnippetUpdate(BaseModel):
    title: str | None = None
    language: str | None = None
    description: str | None = None
    code: str | None = None
    feedback: str | None = None
    test_code: str | None = None
    test_feedback: str | None = None


class Snippet(SnippetCreate):
    model_config = ConfigDict(from_attributes=True)

    id: int
    test_result: str
    test_result_message: str
    created_at: datetime
    updated_at: datetime


class LanguageDetRequest(BaseModel):
    description: str
    code: str


class LanguageDetResponse(BaseModel):
    language: str | None


class CodeGenRequest(BaseModel):
    description: str


class TitleGenRequest(BaseModel):
    description: str


class CodeFeedbackRequest(BaseModel):
    description: str
    code: str
    feedback: str


class TestGenRequest(BaseModel):
    description: str
    code: str
    feedback: str


class TestsFeedbackRequest(BaseModel):
    description: str
    code: str
    feedback: str
    test_code: str
    test_feedback: str


class TestRunRequest(BaseModel):
    snippet_id: int
    code: str
    test_code: str
    language: str


class RegenerateRequest(BaseModel):
    description: str
    code: str
    feedback: str
    test_code: str
    test_feedback: str
    error_message: str
