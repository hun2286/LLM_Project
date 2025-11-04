import os
from dotenv import load_dotenv
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_openai import ChatOpenAI
from langchain.schema import Document, SystemMessage, HumanMessage

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

persist_dir = "./backend/mk_pdf_chroma_db"

# 모델 초기화
llm = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0.2,
    max_tokens=6000,
    openai_api_key=api_key
)

embedding_model = HuggingFaceEmbeddings(
    model_name="bespin-global/klue-sroberta-base-continue-learning-by-mnr"
)

# 벡터DB 로드
vectorstore = Chroma(persist_directory=persist_dir, embedding_function=embedding_model)
retriever = vectorstore.as_retriever(search_type="similarity", search_kwargs={"k": 5})


def rag_answer(question: str) -> dict:
    """RAG 기반 질의응답"""
    retriever_docs = retriever.invoke(question)
    if isinstance(retriever_docs, Document):
        retriever_docs = [retriever_docs]

    context_texts = []
    for doc in retriever_docs:
        content = doc.page_content.strip()
        if not content:
            continue
        context_texts.append(content)

    context = "\n\n".join(context_texts)
    sources = sorted(set([doc.metadata.get("source", "출처 없음") for doc in retriever_docs]))
    sources_text = ", ".join(sources)

    messages = [
        SystemMessage(content="""
        당신은 여러 PDF 문서를 참고하여 질문에 답하는 전문가입니다.
        문서에 없는 정보는 '정보 없음'으로 표시하세요.
        출처는 반드시 '[출처: ...]' 형식으로 작성하세요.
        """),
        HumanMessage(content=f"문서 내용:\n{context}\n\n질문:\n{question}\n\n출처 : {sources_text}")
    ]

    response = llm.invoke(messages)
    return {"answer": response.content, "sources": sources}