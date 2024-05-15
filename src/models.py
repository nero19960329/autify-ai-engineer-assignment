"""
This module defines the database models using SQLAlchemy's declarative base.
It includes the Snippet model, which represents a code snippet with associated metadata.
"""

from datetime import datetime

from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class Snippet(Base):
    __tablename__ = "snippets"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    language = Column(String, index=True)
    description = Column(Text, default="")
    code = Column(Text)
    feedback = Column(Text, default="")
    test_code = Column(Text, default="")
    test_feedback = Column(Text, default="")
    test_result = Column(String, default="")
    test_result_message = Column(Text, default="")
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)
