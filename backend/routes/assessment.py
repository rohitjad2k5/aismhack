from fastapi import APIRouter
from agents.assessment_agent import evaluate_domain_fit

router = APIRouter(prefix="/assessment", tags=["Assessment"])


@router.post("/evaluate/{domain}")
def evaluate(domain: str, data: dict):
    return evaluate_domain_fit(domain, data["profile"])
