from functools import lru_cache
import pandas as pd
from fastapi import APIRouter, HTTPException
from sklearn.ensemble import RandomForestClassifier
from synergy_ai.config import settings
from synergy_ai.schemas import RiskRequest, RiskResponse

router = APIRouter(prefix="/analytics", tags=["4. Аналитика и оценка"])

@lru_cache(maxsize=1)
def train_model():
    try:
        df = pd.read_csv(settings.students_csv_path)
    except FileNotFoundError:
        raise HTTPException(500, "students.csv не найден")
    X = df[["attendance", "assignments_done", "avg_grade"]]
    y = df["at_risk"]
    model = RandomForestClassifier(
        n_estimators=200, class_weight="balanced", random_state=42
    )
    model.fit(X, y)
    return model

@router.post("/risk", response_model=RiskResponse)
def predict_risk(req: RiskRequest):
    model = train_model()
    proba = model.predict_proba(
        [[req.attendance, req.assignments_done, req.avg_grade]]
    )[0][1]
    return RiskResponse(risk=round(float(proba), 3))