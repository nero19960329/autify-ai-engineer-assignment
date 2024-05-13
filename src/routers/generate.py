import json
import os

from fastapi import APIRouter
from fastapi.responses import StreamingResponse
import openai

from src import schemas

router = APIRouter(prefix="/generate", tags=["generate"])


def load_system_prompt(filename):
    with open(os.path.join("src", "prompts", filename), "r", encoding="utf-8") as f:
        return f.read().strip()


async def chatgpt_stream_response(messages):
    client = openai.AsyncOpenAI(
        base_url=os.environ.get("OPENAI_API_BASE", openai.NOT_GIVEN),
    )

    stream = await client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=messages,
        stream=True,
    )

    async for chunk in stream:
        if chunk.choices[0].delta.content is not None:
            yield chunk.choices[0].delta.content


async def chatgpt_response(messages, response_format=openai.NOT_GIVEN):
    client = openai.OpenAI(
        base_url=os.environ.get("OPENAI_API_BASE", openai.NOT_GIVEN),
    )

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        response_format=response_format,
        messages=messages,
    )

    return response.choices[0].message.content


@router.post("/title")
async def generate_title(title_gen_data: schemas.TitleGenRequest):
    messages = [
        {"role": "system", "content": load_system_prompt("generate_title.txt")},
        {
            "role": "user",
            "content": json.dumps({"description": title_gen_data.description}),
        },
    ]

    return StreamingResponse(
        chatgpt_stream_response(messages), media_type="text/event-stream"
    )


@router.post("/code")
async def generate_code(code_gen_data: schemas.CodeGenRequest):
    messages = [
        {"role": "system", "content": load_system_prompt("generate_code.txt")},
        {
            "role": "user",
            "content": json.dumps({"description": code_gen_data.description}),
        },
    ]

    return StreamingResponse(
        chatgpt_stream_response(messages), media_type="text/event-stream"
    )


@router.post("/detect_language", response_model=schemas.LanguageDetResponse)
async def detect_language(language_gen_data: schemas.LanguageDetRequest):
    messages = [
        {"role": "system", "content": load_system_prompt("detect_language.txt")},
        {
            "role": "user",
            "content": json.dumps(
                {
                    "description": language_gen_data.description,
                    "code": language_gen_data.code,
                }
            ),
        },
    ]

    response = await chatgpt_response(messages, response_format={"type": "json_object"})
    return json.loads(response)


@router.post("/code_from_feedback")
async def generate_code_from_feedback(feedback_data: schemas.CodeFeedbackRequest):
    messages = [
        {
            "role": "system",
            "content": load_system_prompt("generate_code_from_feedback.txt"),
        },
        {
            "role": "user",
            "content": json.dumps(
                {
                    "description": feedback_data.description,
                    "code": feedback_data.code,
                    "feedback": feedback_data.feedback,
                }
            ),
        },
    ]

    return StreamingResponse(
        chatgpt_stream_response(messages), media_type="text/event-stream"
    )


@router.post("/tests")
async def generate_tests(test_gen_data: schemas.TestGenRequest):
    messages = [
        {"role": "system", "content": load_system_prompt("generate_tests.txt")},
        {
            "role": "user",
            "content": json.dumps(
                {
                    "description": test_gen_data.description,
                    "code": test_gen_data.code,
                    "feedback": test_gen_data.feedback,
                }
            ),
        },
    ]

    return StreamingResponse(
        chatgpt_stream_response(messages), media_type="text/event-stream"
    )


@router.post("/tests_from_feedback")
async def generate_tests_from_feedback(feedback_data: schemas.TestsFeedbackRequest):
    messages = [
        {
            "role": "system",
            "content": load_system_prompt("generate_tests_from_feedback.txt"),
        },
        {
            "role": "user",
            "content": json.dumps(
                {
                    "description": feedback_data.description,
                    "code": feedback_data.code,
                    "feedback": feedback_data.feedback,
                    "test_code": feedback_data.test_code,
                    "test_feedback": feedback_data.test_feedback,
                }
            ),
        },
    ]

    return StreamingResponse(
        chatgpt_stream_response(messages), media_type="text/event-stream"
    )


@router.post("/regenerate")
async def regenerate_code(regenerate_data: schemas.RegenerateRequest):
    messages = [
        {"role": "system", "content": load_system_prompt("regenerate.txt")},
        {
            "role": "user",
            "content": json.dumps(
                {
                    "description": regenerate_data.description,
                    "code": regenerate_data.code,
                    "feedback": regenerate_data.feedback,
                    "test_code": regenerate_data.test_code,
                    "test_feedback": regenerate_data.test_feedback,
                    "error_message": regenerate_data.error_message,
                }
            ),
        },
    ]

    return StreamingResponse(
        chatgpt_stream_response(messages), media_type="text/event-stream"
    )
