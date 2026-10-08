"""
Prompt templates — all LLM prompts live here.
Centralised so they're easy to iterate on without touching business logic.
"""


def quiz_prompt(topic: str, difficulty: str, num_questions: int, question_type: str) -> str:
    return f"""Generate exactly {num_questions} quiz questions about "{topic}".
Difficulty: {difficulty}
Question types: {question_type}

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


EXPLAIN_STYLES = {
    "simple":   "Explain this simply and clearly. Use short sentences. Avoid jargon.",
    "detailed": "Give a thorough, detailed explanation with examples and nuances.",
    "eli5":     "Explain this like I'm 5 years old. Use simple analogies and fun language.",
    "analogy":  "Explain this using creative real-world analogies. Make it memorable.",
}


def explain_prompt(topic: str, style: str) -> str:
    style_instruction = EXPLAIN_STYLES.get(style, EXPLAIN_STYLES["simple"])
    return f"""You are a world-class tutor. Explain the topic: "{topic}"

Style: {style_instruction}

Structure your response as follows:
1. **Overview** — A 1-2 sentence summary
2. **Explanation** — The main explanation in the requested style
3. **Key Points** — 3-5 bullet points of the most important things to remember
4. **Example** — A concrete example that illustrates the concept

Use markdown formatting. Be educational and engaging."""


def check_answer_prompt(topic: str, question: str, correct_answer: str, user_answer: str) -> str:
    return f"""You are a tutor checking a student's answer.

Topic: {topic}
Question: {question}
Correct Answer: {correct_answer}
Student's Answer: {user_answer}

Return ONLY a valid JSON object (no markdown, no extra text):
{{
  "is_correct": true/false,
  "score": 0-100,
  "feedback": "Encouraging feedback explaining what was right/wrong",
  "tip": "A helpful study tip related to this question"
}}"""


def flashcard_prompt(topic: str, count: int) -> str:
    return f"""Generate exactly {count} study flashcards about "{topic}".

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


def chat_prompt(message: str, context: str | None = None) -> str:
    context_line = f"\nContext from current study session: {context}" if context else ""
    return f"""You are StudyBot, a friendly and knowledgeable AI study assistant.
You help students understand topics, answer questions, and prepare for exams.
Be encouraging, clear, and use examples when helpful.
Use markdown formatting for structure.{context_line}

Student's message: {message}"""
