import asyncio

from fastapi import APIRouter
from fastapi.responses import StreamingResponse

from src import schemas

router = APIRouter(prefix="/generate", tags=["generate"])


async def fake_stream_data(data: str):
    for char in data:
        yield char
        await asyncio.sleep(0.01)  # Simulate slow streaming


@router.post("/title")
async def generate_title(title_gen_data: schemas.TitleGenRequest):
    fake_title = "Add two numbers"
    return StreamingResponse(
        fake_stream_data(fake_title), media_type="text/event-stream"
    )


@router.post("/code")
async def generate_code(code_gen_data: schemas.CodeGenRequest):
    fake_code = "def sum(a, b):\n    return a + b"
    return StreamingResponse(
        fake_stream_data(fake_code), media_type="text/event-stream"
    )


@router.post("/detect_language")
async def detect_language(language_gen_data: schemas.LanguageDetRequest):
    return {"language": "python"}


@router.post("/code_from_feedback")
async def generate_code_from_feedback(feedback_data: schemas.CodeFeedbackRequest):
    fake_code = "def sum(a: int, b: int) -> int:\n    return a + b"
    return StreamingResponse(
        fake_stream_data(fake_code), media_type="text/event-stream"
    )


@router.post("/tests")
async def generate_tests(test_gen_data: schemas.TestGenRequest):
    fake_code = "assert sum(1, 2) == 3"
    return StreamingResponse(
        fake_stream_data(fake_code), media_type="text/event-stream"
    )


@router.post("/tests_from_feedback")
async def generate_tests_from_feedback(feedback_data: schemas.TestsFeedbackRequest):
    fake_code = "assert sum(1, 2) == 3\nassert sum(2, 3) == 5"
    return StreamingResponse(
        fake_stream_data(fake_code), media_type="text/event-stream"
    )
