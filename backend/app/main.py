# FastAPI 엔드 포인트 정의

from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os
from .rag_module import rag_answer, append_to_pdf, save_pdf

app = FastAPI(title="RAG PDF QA API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 필요 시 프론트 도메인으로 제한
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class QueryRequest(BaseModel):
    question: str
#    save_pdf: bool = False

@app.post("/ask")
async def ask_question(request: QueryRequest):
    answer = rag_answer(request.question)
    if request.save_pdf:
        append_to_pdf(request.question, answer)
    return {"question": request.question, "answer": answer}

# @app.post("/upload_pdf/")
# async def upload_pdf(file: UploadFile = File(...)):
#     file_location = f"temp_uploads/{file.filename}"
#     os.makedirs("temp_uploads", exist_ok=True)
#     with open(file_location, "wb") as f:
#         f.write(file.file.read())
#     # 업로드 후 DB 갱신 처리 가능
#     return {"filename": file.filename, "status": "uploaded"}

# @app.get("/save_pdf/")
# async def download_pdf():
#     if not pending_saves:
#         return {"status": "no data to save"}

#     # 누적된 yes 질문들만 PDF로 저장
#     for item in pending_saves:
#         append_to_pdf(item["question"], item["answer"])

#     save_pdf()
#     pending_saves.clear()
#     return {"status": "PDF saved", "path": "result_log.pdf"}