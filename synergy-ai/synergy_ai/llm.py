from openai import OpenAI
from synergy_ai.config import settings

client = OpenAI(api_key=settings.openai_api_key, base_url=settings.openai_base_url)

def chat(system: str, user: str, json_mode: bool = False, temperature: float = 0.3) -> str:
    kwargs = {}
    if json_mode:
        kwargs["response_format"] = {"type": "json_object"}
    resp = client.chat.completions.create(
        model=settings.llm_model,
        messages=[
            {"role": "system", "content": system},
            {"role": "user", "content": user},
        ],
        temperature=temperature,
        **kwargs,
    )
    return resp.choices[0].message.content