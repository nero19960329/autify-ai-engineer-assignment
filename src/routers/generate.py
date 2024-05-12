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
        base_url="https://ai-yyds.com/v1",
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
        base_url="https://ai-yyds.com/v1",
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
            "content": f"Generate a title for the following code description:\n\n{title_gen_data.description}",
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
            "content": f"Generate code for the following description:\n\n{code_gen_data.description}",
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
            "content": f"Detect the programming language of the following code:\n\n{language_gen_data.code}",
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
            "content": f"Here is a function:\n\n{feedback_data.code}\n\nHere is some feedback on how to improve it:\n\n{feedback_data.feedback}",
        },
    ]

    print(messages)

    return StreamingResponse(
        chatgpt_stream_response(messages), media_type="text/event-stream"
    )


@router.post("/tests")
async def generate_tests(test_gen_data: schemas.TestGenRequest):
    messages = [
        {"role": "system", "content": load_system_prompt("generate_tests.txt")},
        {
            "role": "user",
            "content": f"Generate test cases for the following code:\n\n{test_gen_data.code}",
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
            "content": f"Here is some code:\n\n{feedback_data.code}\n\nAnd here are the existing test cases:\n\n{feedback_data.test_code}\n\nHere is some feedback on how to improve the test cases:\n\n{feedback_data.feedback}",
        },
    ]

    return StreamingResponse(
        chatgpt_stream_response(messages), media_type="text/event-stream"
    )
