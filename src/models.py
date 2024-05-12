from datetime import datetime

from sqlalchemy import Column, Integer, String, Text, DateTime
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
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)
