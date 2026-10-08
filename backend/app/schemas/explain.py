from pydantic import BaseModel


class ExplainRequest(BaseModel):
    topic: str
    style: str = "simple"   # simple | detailed | eli5 | analogy
