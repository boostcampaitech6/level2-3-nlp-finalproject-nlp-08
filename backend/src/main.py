from loguru import logger
from fastapi import FastAPI
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


app = FastAPI(lifespan=lifespan)

app.include_router(router=qgrouter)

# .env configuration management is needed
# def load_config():
    # pass
                  

@app.get("/")
def access_root():
    return "root access success"

if __name__ == '__main__':
    uvicorn.run("main:app", host='0.0.0.0', port=8000, reload=True)
