from fastapi import APIRouter
from app.schemas.flashcards import FlashcardRequest
from app.services import llm_service
from app.prompts.templates import flashcard_prompt

router = APIRouter(prefix="/api", tags=["flashcards"])


@router.post("/flashcards")
async def generate_flashcards(req: FlashcardRequest):
    """Generate study flashcards for a topic."""
    prompt = flashcard_prompt(req.topic, req.count)
    cards = await llm_service.complete(prompt, parse_json=True)
    return {"topic": req.topic, "cards": cards}
