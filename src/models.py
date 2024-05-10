from datetime import datetime

from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship

from src.database import Base


class CodeSnippet(Base):
    __tablename__ = "snippets"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    language = Column(String, index=True)
    code = Column(Text)
    description = Column(Text, default="")
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)

    feedbacks = relationship("Feedback", back_populates="snippet")
    tests = relationship("Test", back_populates="snippet")


class Feedback(Base):
    __tablename__ = "feedbacks"

    id = Column(Integer, primary_key=True, index=True)
    snippet_id = Column(Integer, ForeignKey("snippets.id"))
    language = Column(String)
    content = Column(Text)
    created_at = Column(DateTime, default=datetime.now)

    snippet = relationship("CodeSnippet", back_populates="feedbacks")


class Test(Base):
    __tablename__ = "tests"

    id = Column(Integer, primary_key=True, index=True)
    snippet_id = Column(Integer, ForeignKey("snippets.id"))
    test_code = Column(Text)
    created_at = Column(DateTime, default=datetime.now)

    snippet = relationship("CodeSnippet", back_populates="tests")
    results = relationship("TestResult", back_populates="test")


class TestResult(Base):
    __tablename__ = "test_results"

    id = Column(Integer, primary_key=True, index=True)
    test_id = Column(Integer, ForeignKey("tests.id"))
    result = Column(String)
    message = Column(Text)
    created_at = Column(DateTime, default=datetime.now)

    test = relationship("Test", back_populates="results")
