# RAG 핵심 로직(PDF 읽기, 마크다운 변환, 벡터 DB 구축, 질문 답변 생성)

import os
import io
from langchain_openai import ChatOpenAI
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain.schema import Document, SystemMessage, HumanMessage
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import Paragraph
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from PyPDF2 import PdfReader, PdfWriter
from dotenv import load_dotenv
from .utils import load_all_pdfs

# 환경
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

pdf_folder = r"C:\Users\BGR_NC_2_NOTE\Desktop\pdfs\20151103"
persist_dir = "./mk_pdf_chroma_db"
font_path = r"C:\Users\BGR_NC_2_NOTE\Desktop\Project\rag_web\backend\fonts"

# LLM / Embedding
llm = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0.2,
    max_tokens=6000,
    openai_api_key=api_key
)

embedding_model = HuggingFaceEmbeddings(
    model_name="bespin-global/klue-sroberta-base-continue-learning-by-mnr"
)

# 폰트 등록
pdfmetrics.registerFont(TTFont('NanumGothic', os.path.join(font_path, 'NanumGothic.ttf')))
pdfmetrics.registerFont(TTFont('NanumGothicBold', os.path.join(font_path, 'NanumGothicBold.ttf')))

# PDF 저장 객체
pdf_writer = PdfWriter()
current_canvas = None
current_packet = None
y_position = None

# Vector DB
if not os.path.exists(persist_dir) or not os.listdir(persist_dir):
    print("[DB 없음] 새로 구축합니다.")
    docs = load_all_pdfs(pdf_folder)
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1200, chunk_overlap=300)
    split_docs = text_splitter.split_documents(docs)
    print(f"총 청크 수: {len(split_docs)}")

    vectorstore = Chroma.from_documents(
        documents=split_docs,
        embedding=embedding_model,
        persist_directory=persist_dir
    )
    vectorstore.persist()
else:
    print("[DB 있음] 기존 DB를 재사용합니다.")
    vectorstore = Chroma(persist_directory=persist_dir, embedding_function=embedding_model)

retriever = vectorstore.as_retriever(search_type="similarity", search_kwargs={"k": 5})

# RAG 답변
def rag_answer(question):
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
        - 질문에 등장하는 단어를 각각 구분하여 정확히 답변하세요.
        - 문서에 없으면 '정보 없음'으로 표시하세요.
        - 가능한 한 문서 내 문맥과 키워드에 기반하여 정확하게 답변하세요.
        - 각 항목의 출처는 반드시 별도의 줄에 '[출처: ...]' 형태로 표시하세요.
        - 연속된 문단이 동일한 출처를 참조하는 경우, 마지막 관련 문단에만 출처를 표시하세요.
        - 다른 출처가 나오면 그 문단 바로 아래에 해당 출처를 표시하세요.
        """),
        HumanMessage(content=f"문서 내용:\n{context}\n\n질문:\n{question}\n\n출처 : {sources_text}")
    ]
    response = llm.invoke(messages)
    return response.content

# PDF 추가
def append_to_pdf(question, answer):
    global pdf_writer, current_canvas, current_packet, y_position
    # 중복 출처 제거
    unique_lines = []
    seen_sources = set()
    for line in answer.split("\n"):
        line = line.strip()
        if not line:
            continue
        if line.startswith("[출처:"):
            if line not in seen_sources:
                unique_lines.append(line)
                seen_sources.add(line)
        else:
            unique_lines.append(line)
    answer = "\n".join(unique_lines)

    width, height = A4
    margin_top, margin_bottom, margin_left, margin_right = 25, 25, 20, 20
    nanum_style = ParagraphStyle('Nanum', fontName='NanumGothic', fontSize=11, leading=15)
    nanum_bold_style = ParagraphStyle('NanumBold', fontName='NanumGothicBold', fontSize=13, leading=17)

    if current_canvas is None:
        current_packet = io.BytesIO()
        current_canvas = canvas.Canvas(current_packet, pagesize=A4)
        y_position = height - margin_top

    can = current_canvas
    y = y_position

    # 질문
    para = Paragraph(f"질문: {question}", nanum_bold_style)
    w, h = para.wrap(width - margin_left - margin_right, y)
    if y - h < margin_bottom:
        can.showPage()
        y = height - margin_top
    para.drawOn(can, margin_left, y - h)
    y -= h + 10

    # 답변
    lines = answer.split("\n")
    for line in lines:
        line = line.strip()
        if not line:
            continue
        if line.startswith("[출처:"):
            para = Paragraph(line, nanum_style)
        elif line.startswith("# "):
            para = Paragraph(line[2:].strip(), nanum_bold_style)
        elif line.startswith("## "):
            para = Paragraph(line[3:].strip(), nanum_bold_style)
        else:
            para = Paragraph(line, nanum_style)

        w, h = para.wrap(width - margin_left - margin_right, y)
        if y - h < margin_bottom:
            can.showPage()
            y = height - margin_top
        para.drawOn(can, margin_left, y - h)
        y -= h + 5

    y_position = y - 15

def save_pdf(path="result_log.pdf"):
    global pdf_writer, current_canvas, current_packet
    if current_canvas is None:
        print("저장할 PDF가 없습니다.")
        return
    current_canvas.save()
    current_packet.seek(0)
    new_pdf = PdfReader(current_packet)
    for page in new_pdf.pages:
        pdf_writer.add_page(page)
    with open(path, "wb") as f:
        pdf_writer.write(f)
    print(f"PDF 최종 저장 완료: {path}")