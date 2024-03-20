from loguru import logger
from fastapi import FastAPI
from fastapi_sqlalchemy import DBSessionMiddleware
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from contextlib import asynccontextmanager

from dependencies import load_qg_model, load_config
from routers.qgrouter import qgrouter
from routers.feedbackrouter import feedbackrouter
import models
from database import engine

# Lifespan function : load model once / DB connection management
@asynccontextmanager
async def lifespan(app: FastAPI):    
    logger.info("start up event")
    logger.info("load app config")
    app_config = load_config("config.yaml")
    logger.info("load model and tokenizer")
    ml_models = load_qg_model(tokenizer=app_config['qg_model']["tokenizer_name"],
                              qg_model=app_config['qg_model']["model_name"],
                              hf_token = app_config["qg_model"]["token"],
                              ke_model=app_config['ke_model'])
    # create db connection
    logger.info(f"create db {app_config['database_uri']}")
    models.Base.metadata.create_all(bind=engine)
    yield
    logger.info("shutdown event")
    ml_models.clear()

origins = [
    "http://localhost:3000",
    "http://223.130.163.224:3000",
    "localhost:3000",
]

app = FastAPI(lifespan=lifespan)

app.add_middleware(
    DBSessionMiddleware, 
    db_url=load_config("config.yaml")['database_uri']
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router=qgrouter)
app.include_router(router=feedbackrouter)


@app.get("/")
def access_root():
    return "root access success"

if __name__ == '__main__':
    uvicorn.run("main:app", host='0.0.0.0', port=8000, reload=True)
