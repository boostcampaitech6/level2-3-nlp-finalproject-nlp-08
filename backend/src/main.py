from fastapi import FastAPI, APIRouter
import uvicorn

from contextlib import asynccontextmanager
from dataclass import DocumentIn, DocumentOut

from model import inference

app = FastAPI()

# define routers ex)
# user_router = APIRouter(prefix='/users')
# model_router = APIRouter(prefix='/model')

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
async def generate_qa(doc : DocumentIn):
    print("got context from client: ", doc.context)
    doc_out = inference(doc)
    print("aligned model output : ", doc_out.question_answer_pairs)
    return doc_out                      


@app.get("/")
def access_root():
    return "root access success"

if __name__ == '__main__':
    # app.include_router(user_router)
    # app.include_router(model_router)
    uvicorn.run(app, host='0.0.0.0', port=8000)
    # uvicorn.run(app, host='10.79.41.39', port=8000)