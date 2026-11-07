from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from synergy_ai.routers import (
    admissions,
    student_support,
    content_gen,
    analytics,
    admin_assistant,
)

app = FastAPI(
    title="Synergy AI Services",
    description="Единый ИИ-сервис для бизнес-процессов Университета «Синергия»",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(admissions.router)
app.include_router(student_support.router)
app.include_router(content_gen.router)
app.include_router(analytics.router)
app.include_router(admin_assistant.router)

@app.get("/health", tags=["system"])
def health():
    return {"status": "ok"}