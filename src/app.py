"""
This module sets up the FastAPI application, including routers, static files, and templates.
It also creates the database tables and defines the root endpoint.
"""

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from src.database import engine
from src.routers import snippets, generate, run
from src.logger import logger
from src import models

models.Base.metadata.create_all(bind=engine)  # Create database tables

app = FastAPI()
app.mount(
    "/static", StaticFiles(directory="src/static"), name="static"
)  # Mount static files
app.include_router(snippets.router, prefix="/api")  # Include snippets router
app.include_router(generate.router, prefix="/api")  # Include generate router
app.include_router(run.router, prefix="/api")  # Include run router

templates = Jinja2Templates(directory="src/templates")


@app.exception_handler(Exception)
async def generic_exception_handler(request: Request, exc: Exception):
    logger.exception(f"Unhandled exception: {exc}")
    return JSONResponse(
        status_code=500,
        content={"message": "Internal server error"},
    )


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    logger.error(f"Validation error: {exc}")
    return JSONResponse(
        status_code=422,
        content={"message": "Invalid request", "details": exc.errors()},
    )


@app.get("/")
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})
