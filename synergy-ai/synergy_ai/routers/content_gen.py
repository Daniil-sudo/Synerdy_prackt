import json
from fastapi import APIRouter
from synergy_ai.llm import chat
from synergy_ai.schemas import QuizRequest, QuizResponse, QuizItem

router = APIRouter(prefix="/content", tags=["3. Генерация контента"])

PROMPT = """По фрагменту учебного текста сгенерируй {n} тестовых вопросов.
Верни строго JSON: {{"items": [{{"question": "...", "options": ["A","B","C","D"],
"correct": 0, "explanation": "..."}}]}}
Текст: {text}"""

@router.post("/generate-quiz", response_model=QuizResponse)
def generate_quiz(req: QuizRequest):
    raw = chat(
        "Ты методист, создающий тестовые задания.",
        PROMPT.format(n=req.n, text=req.text),
        json_mode=True,
        temperature=0.5,
    )
    data = json.loads(raw)
    items = [QuizItem(**item) for item in data["items"]]
    return QuizResponse(items=items)