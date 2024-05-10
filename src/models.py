from sqlalchemy import Column, Integer, String, Text

from src.database import Base


class CodeSnippet(Base):
    __tablename__ = "code_snippets"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    language = Column(String, index=True)
    code = Column(Text)
