import os
import json
import re
import traceback
import httpx
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from typing import Optional

load_dotenv()

# ── Config ──────────────────────────────────────────────────────────
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_URL = os.getenv("GROQ_URL")
MODEL = "openai/gpt-oss-120b"

app = FastAPI(title="Study Helper API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── Models ──────────────────────────────────────────────────────────
class QuizRequest(BaseModel):
    topic: str
    difficulty: str = "medium"
    num_questions: int = 5
    question_type: str = "mixed"

class ExplainRequest(BaseModel):
    topic: str
    style: str = "simple"

class AnswerCheckRequest(BaseModel):
    question: str
    user_answer: str
    correct_answer: str
    topic: str

class FlashcardRequest(BaseModel):
    topic: str
    count: int = 10

class ChatRequest(BaseModel):
    message: str
    context: Optional[str] = None

# ── Helpers ─────────────────────────────────────────────────────────
def clean_json_response(text: str) -> str:
    """Extract JSON from markdown code blocks if present."""
    match = re.search(r'```(?:json)?\s*\n?([\s\S]*?)\n?```', text)
    if match:
        return match.group(1).strip()
    text = text.strip()
    if text.startswith('[') or text.startswith('{'):
        return text
    return text

async def ask_llm(prompt: str, parse_json: bool = False):
    """Send prompt to Groq API (OpenAI-compatible)."""
    try:
        payload = {
            "model": MODEL,
            "messages": [
                {"role": "user", "content": prompt}
            ],
            "temperature": 0.7,
            "max_tokens": 4096
        }

        async with httpx.AsyncClient(timeout=60.0) as client:
            response = await client.post(
                GROQ_URL,
                headers={
                    "Authorization": f"Bearer {GROQ_API_KEY}",
                    "Content-Type": "application/json"
                },
                json=payload
            )

        if response.status_code != 200:
            error_detail = response.text[:500]
            print(f"❌ Groq API HTTP {response.status_code}: {error_detail}")
            raise HTTPException(status_code=500, detail=f"Groq API error ({response.status_code}): {error_detail}")

        data = response.json()
        text = data["choices"][0]["message"]["content"].strip()

        if parse_json:
            cleaned = clean_json_response(text)
            return json.loads(cleaned)
        return text

    except json.JSONDecodeError as e:
        print(f"❌ JSON parse error: {e}\nRaw response: {text[:500]}")
        raise HTTPException(status_code=500, detail=f"Failed to parse AI response as JSON: {str(e)}")
    except HTTPException:
        raise
    except Exception as e:
        print(f"❌ API error: {traceback.format_exc()}")
        raise HTTPException(status_code=500, detail=f"API error: {str(e)}")

# ── Routes ──────────────────────────────────────────────────────────

@app.get("/api/health")
async def health():
    return {"status": "ok", "model": "openai/gpt-oss-120b"}


@app.post("/api/quiz")
async def generate_quiz(req: QuizRequest):
    """Generate a quiz on any topic."""
    prompt = f"""Generate exactly {req.num_questions} quiz questions about "{req.topic}".
Difficulty: {req.difficulty}
Question types: {req.question_type}

Return ONLY a valid JSON array (no markdown, no explanation) with this structure:
[ 
  {{
    "id": 1,
    "type": "mcq",
    "question": "...",
    "options": ["A) ...", "B) ...", "C) ...", "D) ..."],
    "correct_answer": "A",
    "explanation": "Brief explanation of why this is correct"
  }},
  {{
    "id": 2,
    "type": "true_false",
    "question": "...",
    "options": ["True", "False"],
    "correct_answer": "True",
    "explanation": "Brief explanation"
  }},
  {{
    "id": 3,
    "type": "short_answer",
    "question": "...",
    "options": [],
    "correct_answer": "expected answer keywords",
    "explanation": "Full explanation of the answer"
  }}
]

Rules:
- For "mcq": always provide 4 options labeled A, B, C, D. correct_answer is the letter.
- For "true_false": options are ["True", "False"]. correct_answer is "True" or "False".
- For "short_answer": options is empty array. correct_answer is the expected answer.
- For "mixed": use a variety of question types.
- Make questions educational and clear.
- Return ONLY the JSON array, nothing else."""

    questions = await ask_llm(prompt, parse_json=True)
    return {"topic": req.topic, "difficulty": req.difficulty, "questions": questions}


@app.post("/api/explain")
async def explain_topic(req: ExplainRequest):
    """Explain a topic in the requested style."""
    style_prompts = {
        "simple": "Explain this simply and clearly. Use short sentences. Avoid jargon.",
        "detailed": "Give a thorough, detailed explanation with examples and nuances.",
        "eli5": "Explain this like I'm 5 years old. Use simple analogies and fun language.",
        "analogy": "Explain this using creative real-world analogies. Make it memorable."
    }

    prompt = f"""You are a world-class tutor. Explain the topic: "{req.topic}"

Style: {style_prompts.get(req.style, style_prompts["simple"])}

Structure your response as follows:
1. **Overview** — A 1-2 sentence summary
2. **Explanation** — The main explanation in the requested style
3. **Key Points** — 3-5 bullet points of the most important things to remember
4. **Example** — A concrete example that illustrates the concept

Use markdown formatting. Be educational and engaging."""

    explanation = await ask_llm(prompt)
    return {"topic": req.topic, "style": req.style, "explanation": explanation}


@app.post("/api/check-answer")
async def check_answer(req: AnswerCheckRequest):
    """Check a user's answer and provide feedback."""
    prompt = f"""You are a tutor checking a student's answer.

Topic: {req.topic}
Question: {req.question}
Correct Answer: {req.correct_answer}
Student's Answer: {req.user_answer}

Return ONLY a valid JSON object (no markdown, no extra text):
{{
  "is_correct": true/false,
  "score": 0-100,
  "feedback": "Encouraging feedback explaining what was right/wrong",
  "tip": "A helpful study tip related to this question"
}}"""

    result = await ask_llm(prompt, parse_json=True)
    return result


@app.post("/api/flashcards")
async def generate_flashcards(req: FlashcardRequest):
    """Generate study flashcards for a topic."""
    prompt = f"""Generate exactly {req.count} study flashcards about "{req.topic}".

Return ONLY a valid JSON array (no markdown, no explanation):
[
  {{
    "id": 1,
    "front": "Question or concept",
    "back": "Answer or explanation",
    "hint": "A small hint to help recall"
  }}
]

Make them educational, covering key concepts. Return ONLY the JSON array."""

    cards = await ask_llm(prompt, parse_json=True)
    return {"topic": req.topic, "cards": cards}


@app.post("/api/chat")
async def study_chat(req: ChatRequest):
    """General study assistant chat."""
    context_str = f"\nContext from current study session: {req.context}" if req.context else ""

    prompt = f"""You are StudyBot, a friendly and knowledgeable AI study assistant.
You help students understand topics, answer questions, and prepare for exams.
Be encouraging, clear, and use examples when helpful.
Use markdown formatting for structure.{context_str}

Student's message: {req.message}"""

    response = await ask_llm(prompt)
    return {"response": response}


# ── Serve Frontend ──────────────────────────────────────────────────
app.mount("/", StaticFiles(directory="../frontend", html=True), name="frontend")