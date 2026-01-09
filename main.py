from fastapi import FastAPI
from pydantic import BaseModel
from transformers import pipeline
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
import os

app = FastAPI(title="QA system")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR,"PatelAnjali/qa-roberta-finetuned")
FRONTEND_PATH = os.path.join(BASE_DIR,"frontend")

QA_pipeline = pipeline(
    "question-answering",
    model = MODEL_PATH,
    tokenizer = MODEL_PATH
)

class QAInput(BaseModel):
    context:str
    question:str

@app.post("/ask")
def ask_question(data: QAInput):
    result = QA_pipeline(
        question=data.question,
        context=data.context
    )

    if result["score"] < 0.3:
        return {
            "answer": "Answer not found in context",
            "confidence": round(result["score"], 3)
        }

    return {
        "answer": result["answer"],
        "confidence": round(result["score"], 3)
    }

app.mount("/static", StaticFiles(directory=FRONTEND_PATH), name="static")

@app.get("/")
def serve_frontend():
    return FileResponse(os.path.join(FRONTEND_PATH, "index.html"))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="127.0.0.1",
        port=8001,
        reload=True
    )
