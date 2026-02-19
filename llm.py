import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
OPENROUTER_API_KEY = os.environ["OPENROUTER_API_KEY"]
MODEL = "google/gemini-2.5-flash"

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=OPENROUTER_API_KEY,
)


def chat(messages: list[dict], system_prompt: str = None) -> str:
    if system_prompt:
        messages = [{"role": "system", "content": system_prompt}] + messages

    response = client.chat.completions.create(
        model=MODEL,
        messages=messages,
    )
    return response.choices[0].message.content


def chat_with_image(image_url: str, prompt: str, system_prompt: str = None) -> str:
    messages = []
    if system_prompt:
        messages.append({"role": "system", "content": system_prompt})
    messages.append({
        "role": "user",
        "content": [
            {"type": "image_url", "image_url": {"url": image_url}},
            {"type": "text", "text": prompt},
        ],
    })

    response = client.chat.completions.create(
        model=MODEL,
        messages=messages,
    )
    return response.choices[0].message.content
