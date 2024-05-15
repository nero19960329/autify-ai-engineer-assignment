"""
This module defines the Pydantic schemas used for request and response validation.
It includes schemas for creating, updating, and retrieving snippets, as well as schemas for code generation and testing.
"""

from datetime import datetime

from pydantic import BaseModel, ConfigDict


class SnippetCreate(BaseModel):
    """
    Schema for creating a snippet.
    """

    title: str = ""
    language: str = ""
    description: str = ""
    code: str = ""
    feedback: str = ""
    test_code: str = ""
    test_feedback: str = ""
    is_active: bool = True


class SnippetUpdate(BaseModel):
    """
    Schema for updating a snippet.
    """

    title: str | None = None
    language: str | None = None
    description: str | None = None
    code: str | None = None
    feedback: str | None = None
    test_code: str | None = None
    test_feedback: str | None = None


class Snippet(SnippetCreate):
    """
    Schema for a snippet, including additional fields for ID and timestamps.
    """

    model_config = ConfigDict(from_attributes=True)

    id: int
    test_result: str
    test_result_message: str
    created_at: datetime
    updated_at: datetime


class LanguageDetRequest(BaseModel):
    """
    Schema for a language detection request.
    """

    description: str


class LanguageDetResponse(BaseModel):
    """
    Schema for a language detection response.
    """

    language: str | None


class CodeGenRequest(BaseModel):
    """
    Schema for a code generation request.
    """

    description: str


class TitleGenRequest(BaseModel):
    """
    Schema for a title generation request.
    """

    description: str


class CodeFeedbackRequest(BaseModel):
    """
    Schema for a code improvement request based on feedback.
    """

    description: str
    code: str
    language: str
    feedback: str


class TestGenRequest(BaseModel):
    """
    Schema for a test generation request.
    """

    description: str
    code: str
    language: str
    feedback: str


class TestsFeedbackRequest(BaseModel):
    """
    Schema for a test improvement request based on feedback.
    """

    description: str
    code: str
    language: str
    feedback: str
    test_code: str
    test_feedback: str


class TestRunRequest(BaseModel):
    """
    Schema for a test run request.
    """

    snippet_id: int
    code: str
    language: str
    test_code: str


class RegenerateRequest(BaseModel):
    """
    Schema for a code regeneration request based on test results.
    """

    description: str
    code: str
    language: str
    feedback: str
    test_code: str
    test_feedback: str
    error_message: str
