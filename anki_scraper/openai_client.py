from pathlib import Path
from openai import OpenAI
import os

API_KEY = os.environ["OPENAI_API_KEY"]
client = OpenAI(api_key=API_KEY)

def prompt_gpt(system_prompt: str, user_prompt: str) -> str:
    try:
        response = client.responses.create(
            model="gpt-5-nano",
            input=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
        )
    except Exception as e:
        raise RuntimeError(f"Failed to prompt: {e}") from e
    return response.output_text.strip()
