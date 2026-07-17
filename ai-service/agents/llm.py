import os

from agents.client import client


MODEL = os.getenv("MODEL_NAME", "llama-3.3-70b-versatile")


def ask_llm(system_prompt: str, user_prompt: str) -> str:

    response = client.chat.completions.create(
        model=MODEL,
        temperature=0,
        response_format={"type": "json_object"},
        messages=[
            {
                "role": "system",
                "content": system_prompt
            },
            {
                "role": "user",
                "content": user_prompt
            }
        ]
    )

    return response.choices[0].message.content