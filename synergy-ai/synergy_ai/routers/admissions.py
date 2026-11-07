import json
from fastapi import APIRouter
from synergy_ai.llm import chat
from synergy_ai.schemas import QuestionRequest, AnswerResponse, LeadRequest, LeadResponse

router = APIRouter(prefix="/admissions", tags=["1. Приёмная кампания"])

SYSTEM = """Ты — консультант приёмной комиссии Университета «Синергия».
Отвечай кратко и по делу на вопросы абитуриентов о программах, стоимости,
сроках подачи документов и формах обучения. Если вопрос вне компетенции —
предложи связаться с оператором."""

@router.post("/ask", response_model=AnswerResponse)
def ask(req: QuestionRequest):
    return AnswerResponse(answer=chat(SYSTEM, req.message))

@router.post("/score-lead", response_model=LeadResponse)
def score_lead(req: LeadRequest):
    prompt = (
        "Проанализируй диалог абитуриента и верни JSON: "
        '{"intent": "hot|warm|cold", "program_interest": "...", "reason": "..."}. '
        f"Диалог: {json.dumps(req.dialog, ensure_ascii=False)}"
    )
    data = json.loads(chat("Ты аналитик приёмной кампании.", prompt, json_mode=True))
    return LeadResponse(**data)