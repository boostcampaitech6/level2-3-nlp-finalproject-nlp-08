from loguru import logger
from fastapi import APIRouter

from schemas import QuestionGenerationResponse, QuestionGenerationRequest
from model import generate_question

qgrouter = APIRouter()

# if model inference takes time, utilize BackgroundTasks + async 
@qgrouter.post("/generate")
async def generate_qa(doc : QuestionGenerationRequest):
    response_dict = {
        "question_answer_pairs": []
    }

    context = doc.context
    answers_list = doc.answers
    logger.debug(f"context from client={context}")
    logger.debug(f"num to generate={len(answers_list)}")

    for answer in answers_list:
        generated_question = generate_question(context=context, answer=answer)
        response_dict['question_answer_pairs'].append({
            "question": generated_question, 
            "answer": answer
        })
        logger.debug(f"gemerated qusetion={generated_question} answer={answer}")
    
    result_doc = QuestionGenerationResponse(**response_dict)
    return result_doc    
