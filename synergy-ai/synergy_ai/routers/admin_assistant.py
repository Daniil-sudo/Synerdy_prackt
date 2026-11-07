import json
from fastapi import APIRouter
from synergy_ai.llm import chat
from synergy_ai.schemas import DocumentRequest, DocumentSummary

router = APIRouter(prefix="/admin", tags=["5. Админ-ассистент"])

PROMPT = """Сделай краткое резюме документа (3-5 предложений) и извлеки ключевые пункты.
Верни JSON: {{"summary": "...", "action_items": ["..."], "deadlines": ["..."]}}
Документ: {text}"""

@router.post("/summarize", response_model=DocumentSummary)
def summarize(req: DocumentRequest):
    raw = chat(
        "Ты помощник административного отдела.",
        PROMPT.format(text=req.text),
        json_mode=True,
    )
    return DocumentSummary(**json.loads(raw))