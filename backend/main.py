from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from rag.rag_pipeline import RagPipeline

app = FastAPI(title="RAG Backend")

# CORS 허용 (frontend에서 요청 가능)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# RAG 파이프라인 객체 생성
rag_pipeline = RagPipeline()

@app.get("/")
def root():
    return {"message": "RAG Backend is running"}

@app.post("/rag/query")
def query_rag(question: str):
    answer = rag_pipeline.answer_question(question)
    return {"answer": answer}

@app.post("/rag/upload_pdf")
def upload_pdf(file: bytes = None):
    result = rag_pipeline.process_pdf(file)
    return result