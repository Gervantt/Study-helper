from fastapi import APIRouter
from app.schemas.explain import ExplainRequest
from app.services import llm_service
from app.prompts.templates import explain_prompt

router = APIRouter(prefix="/api", tags=["explain"])


@router.post("/explain")
async def explain_topic(req: ExplainRequest):
    """Explain a topic in the requested style."""
    prompt = explain_prompt(req.topic, req.style)
    explanation = await llm_service.complete(prompt)
    return {"topic": req.topic, "style": req.style, "explanation": explanation}
