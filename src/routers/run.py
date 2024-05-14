"""
This module defines the endpoint for running Python code snippets and their associated tests.
It validates the input data and returns the test results.
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from src.database import get_db
from src.runner import run_python_code
from src import crud, schemas

router = APIRouter(prefix="/run", tags=["run"])


@router.post("/python", status_code=200)
async def run_python(
    test_run_data: schemas.TestRunRequest, db: Session = Depends(get_db)
):
    if test_run_data.language != "python":
        raise HTTPException(
            status_code=400,
            detail="Only Python snippets are supported for running tests",
        )

    db_snippet = crud.get_snippet(db, test_run_data.snippet_id)
    result = run_python_code(test_run_data.code, test_run_data.test_code)
    db_snippet.test_result = result["result"]
    db_snippet.test_result_message = result["message"]
    db.commit()
    return result
