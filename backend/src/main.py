from loguru import logger
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from contextlib import asynccontextmanager

from dependencies import load_qg_model
from routers.qgrouter import qgrouter

# Lifespan function : load model once / DB connection management
@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("start up event")
    logger.info("load model and tokenizer")
    ml_models = load_qg_model()
    # load config
    # create db connection
    yield
    logger.info("shutdown event")
    ml_models.clear()

origins = [
    "http://localhost:3000",
    "localhost:3000",
]

app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router=qgrouter)

# .env configuration management is needed
# def load_config():
    # pass
                  

@app.get("/")
def access_root():
    return "root access success"

if __name__ == '__main__':
    uvicorn.run("main:app", host='0.0.0.0', port=8000, reload=True)
