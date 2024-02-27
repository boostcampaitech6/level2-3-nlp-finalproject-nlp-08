from fastapi import FastAPI, APIRouter
import uvicorn

from contextlib import asynccontextmanager

from dataclasses import dataclass
from pydantic import BaseModel



# For response
@dataclass
class DocumentOut(BaseModel):
    context: str

# for client request
@dataclass
class DocumentIn(BaseModel):
    context: str

DOCIN_EX = {
    "context": "이순신은 조선 중기의 무신이다."
}

DOCOUT_EX = {
    "question_answer_pairs": [
        {"question":"조선 중기 무신의 이름은?", "answer":"이순신"}, 
        {"question":"이순신은 어느 시대의 무신인가?", "answer":"조선 중기"},
    ]
}

app = FastAPI()

# define routers
user_router = APIRouter(prefix='/users')
order_router = APIRouter(prefix='/order')

# Lifespan function : load model once / DB connection management
@asynccontextmanager
async def lifespan():
    print("start up event")
    # load config
    # load model
    # create db connection
    yield
    print("shutdown event")

# .env configuration management is needed
def load_config():
    pass


# if model inference takes time, utilize BackgroundTasks + async 
@app.post("/document/")
def create_document(doc : DocumentIn):
    # try:
    # 1. doc will be the input of the model
    # 2. doc -> model -> output -> DocumentOut
    # except:
    return DocumentOut('success document out')


@app.get("/")
def read_root():
    return "root access success"

if __name__ == '__main__':
    app.include_router(user_router)
    app.include_router(order_router)
    uvicorn.run(app, host='10.79.41.39', port=8000)