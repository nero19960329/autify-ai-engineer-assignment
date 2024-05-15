"""
This module defines the endpoint for running Python code snippets and their associated tests.
It validates the input data and returns the test results.
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from src.database import get_db
from src.runner import run_python_code
from src.logger import logger
from src import crud, schemas

router = APIRouter(prefix="/run", tags=["run"])


@router.post("/python", status_code=200)
async def run_python(
    test_run_data: schemas.TestRunRequest, db: Session = Depends(get_db)
):
    """
    Runs Python code and tests, returning the results.

    Args:
        test_run_data (schemas.TestRunRequest): The request data containing the code, test code, and snippet ID.
        db (Session): The database session.

    Returns:
        dict: The result and message of the code execution.

    Raises:
        HTTPException: If the snippet is not found or an error occurs during code execution.
    """
    if test_run_data.language != "python":
        logger.warning(
            f"Unsupported language for running tests: {test_run_data.language}"
        )
        raise HTTPException(
            status_code=400,
            detail="Only Python snippets are supported for running tests",
        )

    db_snippet = crud.get_snippet(db, test_run_data.snippet_id)
    if not db_snippet:
        logger.warning(f"Snippet not found: {test_run_data.snippet_id}")
        raise HTTPException(status_code=404, detail="Snippet not found")

    try:
        result = run_python_code(test_run_data.code, test_run_data.test_code)
        db_snippet.test_result = result["result"]
        db_snippet.test_result_message = result["message"]
        db.commit()
        return result
    except Exception as e:
        logger.exception(f"Error running Python code: {e}")
        raise HTTPException(status_code=500, detail="Error running Python code") from e
