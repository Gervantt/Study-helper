from pydantic import BaseModel


class QuizRequest(BaseModel):
    topic: str
    difficulty: str = "medium"        # easy | medium | hard
    num_questions: int = 5
    question_type: str = "mixed"      # mixed | mcq | true_false | short_answer


class AnswerCheckRequest(BaseModel):
    question: str
    user_answer: str
    correct_answer: str
    topic: str
