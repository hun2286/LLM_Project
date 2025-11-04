from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from rag_core import rag_answer

app = FastAPI(title="RAG Web API")

# CORS 설정 (React 개발용)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 필요시 특정 도메인으로 제한 가능
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 요청 모델
class QuestionRequest(BaseModel):
    question: str

@app.post("/ask")
def ask_question(req: QuestionRequest):
    result = rag_answer(req.question)
    return result

@app.get("/")
def root():
    return {"message": "RAG API 서버 정상 동작 중 ✅"}