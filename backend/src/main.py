from fastapi import FastAPI, APIRouter
import uvicorn
from contextlib import asynccontextmanager

from model import load_qg_model
from dataclass import DocumentOut, DocumentIn, doc_in_ex, doc_out_ex

import torch


ml_models = {}

# Lifespan function : load model once / DB connection management
@asynccontextmanager
async def lifespan(app: FastAPI):
    print("start up event")
    # load model, tokenizer
    ml_models['tokenizer'], ml_models["qg_model"] = load_qg_model()
    # load config
    # create db connection
    yield
    print("shutdown event")
    ml_models.clear()


app = FastAPI(lifespan=lifespan)

# define routers ex)
# user_router = APIRouter(prefix='/users')
# model_router = APIRouter(prefix='/model')

# .env configuration management is needed
# def load_config():
    # pass


# if model inference takes time, utilize BackgroundTasks + async 
@app.post("/document/")
async def generate_qa(doc : DocumentIn):
    doc = doc_in_ex
    text = doc.context
    print("got context from client: ", text)

    tokenizer = ml_models['tokenizer']
    model = ml_models['qg_model']

    raw_input_ids = tokenizer.encode(text)
    input_ids = [tokenizer.bos_token_id] + raw_input_ids + [tokenizer.eos_token_id]
    print('input ids: ', input_ids)
    summary_ids = model.generate(torch.tensor([input_ids]))

    generated_question = tokenizer.decode(summary_ids.squeeze().tolist(), skip_special_tokens=True)

    result = {
        "question_answer_pairs": [
            {"question": generated_question, "answer": "1989년 2월 15일"}
        ]
    }
    result_doc = DocumentOut(**result)
    return result_doc                      


@app.get("/")
def access_root():
    return "root access success"

if __name__ == '__main__':
    # app.include_router(user_router)
    # app.include_router(model_router)
    uvicorn.run(app, host='0.0.0.0', port=8000)
    # uvicorn.run(app, host='10.79.41.39', port=8000)