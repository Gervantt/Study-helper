from pydantic import BaseModel


class FlashcardRequest(BaseModel):
    topic: str
    count: int = 10
