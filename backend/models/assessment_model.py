from pydantic import BaseModel
from typing import Dict

class AnswerInput(BaseModel):
    answers: Dict[str, int]
