from fastapi import APIRouter
from app.schemas.chat import ChatRequest
from app.services import llm_service
from app.prompts.templates import chat_prompt

router = APIRouter(prefix="/api", tags=["chat"])


@router.post("/chat")
async def study_chat(req: ChatRequest):
    """General study assistant chat."""
    prompt = chat_prompt(req.message, req.context)
    response = await llm_service.complete(prompt)
    return {"response": response}
