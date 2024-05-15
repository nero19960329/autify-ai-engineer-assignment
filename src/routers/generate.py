"""
This module defines the endpoints for generating code snippets, titles, and tests.
It also includes endpoints for detecting languages and improving code and tests based on feedback.
"""

import json
import os

from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse
import openai

from src import schemas

router = APIRouter(prefix="/generate", tags=["generate"])


def load_system_prompt(filename):
    try:
        with open(os.path.join("src", "prompts", filename), "r", encoding="utf-8") as f:
            return f.read().strip()
    except FileNotFoundError as e:
        raise HTTPException(
            status_code=500, detail=f"Prompt file {filename} not found"
        ) from e


async def chatgpt_stream_response(messages: list):
    """
    Send messages to the ChatGPT API and stream the response.

    Args:
        messages (list): The list of messages to send to the ChatGPT API.

    Yields:
        str: The content of each chunk in the stream response.
    """
    try:
        client = openai.AsyncOpenAI()
        if os.getenv("OPENAI_API_BASE"):
            client.base_url = os.getenv("OPENAI_API_BASE")  # Set custom API base URL

        stream = await client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=messages,
            stream=True,
        )

        async for chunk in stream:
            if chunk.choices[0].delta.content is not None:
                yield chunk.choices[
                    0
                ].delta.content  # Yield content of each chunk in the stream

    except openai.APIConnectionError as e:
        raise HTTPException(status_code=500, detail=f"OpenAI API error: {e}") from e


async def chatgpt_response(messages: list, response_format: dict | None = None):
    """
    Send messages to the ChatGPT API and return the complete response.

    Args:
        messages (list): The list of messages to send to the ChatGPT API.
        response_format (dict, optional): The format of the response. Defaults to None.

    Returns:
        str: The content of the response from the ChatGPT API.
    """
    try:
        client = openai.OpenAI()
        if os.getenv("OPENAI_API_BASE"):
            client.base_url = os.getenv("OPENAI_API_BASE")

        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            response_format=response_format or {},
            messages=messages,
        )

        return response.choices[0].message.content

    except openai.APIConnectionError as e:
        raise HTTPException(status_code=500, detail=f"OpenAI API error: {e}") from e


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
            "content": json.dumps({"description": language_gen_data.description}),
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
                    "language": feedback_data.language,
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
                    "language": test_gen_data.language,
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
                    "language": feedback_data.language,
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
                    "language": regenerate_data.language,
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
