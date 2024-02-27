from fastapi import FastAPI
import uvicorn

from pydantic import BaseModel

app = FastAPI()

# For response
class DocumentIn(BaseModel):
    content: str


# For request
class DocumentIn(BaseModel):
    content: str

# get is also avalilable : if using data for feedback use post to save at db
# if sending document only for inference use get
@app.get("/document/")
def send_document(doc : DocumentIn):
    return doc

@app.get("/")
def read_root():
    return {"Hello":"World"}

if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8000)