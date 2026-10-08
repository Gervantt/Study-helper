from fastapi import APIRouter
from app.schemas.quiz import QuizRequest, AnswerCheckRequest
from app.services import llm_service
from app.prompts.templates import quiz_prompt, check_answer_prompt

router = APIRouter(prefix="/api", tags=["quiz"])


@router.post("/quiz")
async def generate_quiz(req: QuizRequest):
    """Generate a quiz on any topic."""
    prompt = quiz_prompt(req.topic, req.difficulty, req.num_questions, req.question_type)
    questions = await llm_service.complete(prompt, parse_json=True)
    return {"topic": req.topic, "difficulty": req.difficulty, "questions": questions}


@router.post("/check-answer")
async def check_answer(req: AnswerCheckRequest):
    """Check a user's answer and provide feedback."""
    prompt = check_answer_prompt(req.topic, req.question, req.correct_answer, req.user_answer)
    return await llm_service.complete(prompt, parse_json=True)
