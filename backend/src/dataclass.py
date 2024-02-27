from dataclasses import dataclass
from pydantic import BaseModel


# For response
@dataclass
class DocumentOut(BaseModel):
    question_answer_pairs: list

    def __init__(self, question_answer_pairs: list) -> None:
        super().__init__(question_answer_pairs=question_answer_pairs)

# for client request
@dataclass
class DocumentIn(BaseModel):
    context: str

    def __init__(self, context: str) -> None:
        super().__init__(context=context)


DOCIN_EX = {
    "context": "이순신은 조선 중기의 무신이다."
}
doc_in_ex = DocumentIn(**DOCIN_EX)

DOCOUT_EX = {
    "question_answer_pairs": [
        {"question":"조선 중기 무신의 이름은?", "answer":"이순신"}, 
        {"question":"이순신은 어느 시대의 무신인가?", "answer":"조선 중기"},
    ]
}
doc_out_ex = DocumentOut(**DOCOUT_EX)