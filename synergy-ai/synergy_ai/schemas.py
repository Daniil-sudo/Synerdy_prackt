from pydantic import BaseModel, Field
from typing import List

# 1. Приёмная кампания
class QuestionRequest(BaseModel):
    message: str

class AnswerResponse(BaseModel):
    answer: str

class LeadRequest(BaseModel):
    dialog: List[str]

class LeadResponse(BaseModel):
    intent: str
    program_interest: str
    reason: str

# 2. Поддержка студентов
class CourseQuestion(BaseModel):
    question: str

class CourseAnswer(BaseModel):
    answer: str

# 3. Генерация контента
class QuizRequest(BaseModel):
    text: str
    n: int = Field(default=5, ge=1, le=20)

class QuizItem(BaseModel):
    question: str
    options: List[str]
    correct: int
    explanation: str

class QuizResponse(BaseModel):
    items: List[QuizItem]

# 4. Аналитика
class RiskRequest(BaseModel):
    attendance: float = Field(ge=0, le=1)
    assignments_done: float = Field(ge=0, le=1)
    avg_grade: float = Field(ge=2, le=5)

class RiskResponse(BaseModel):
    risk: float

# 5. Админ-ассистент
class DocumentRequest(BaseModel):
    text: str

class DocumentSummary(BaseModel):
    summary: str
    action_items: List[str]
    deadlines: List[str]