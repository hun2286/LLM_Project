# pdf처리, 파일 입출력, 폰트 등

import os
import fitz
from langchain.schema import Document

def pdf_to_markdown(pdf_path):
    md_text = ""
    try:
        with fitz.open(pdf_path) as pdf:
            for i, page in enumerate(pdf):
                blocks = page.get_text("blocks")
                blocks = sorted(blocks, key=lambda b:(b[1], b[0]))
                md_text += f"# Page {i+1}\n\n"
                for block in blocks:
                    text = block[4].strip()
                    if not text:
                        continue
                    num_words = len(text.split())
                    num_lines = text.count("\n") + 1
                    if num_words <= 5 and num_lines <= 2:
                        md_text += f"# {text}\n\n"
                    elif num_words <= 15:
                        md_text += f"## {text}\n\n"
                    else:
                        md_text += f"{text}\n\n"
        return md_text
    except Exception as e:
        print(f"[오류] PDF 변환 실패 : {pdf_path}\n{e}")
        return ""

def load_pdf_safe(pdf_path):
    md_text = pdf_to_markdown(pdf_path)
    if md_text:
        return [Document(page_content=md_text,
                         metadata={"source": os.path.splitext(os.path.basename(pdf_path))[0]})]
    return []

def load_all_pdfs(pdf_folder):
    docs = []
    for pdf_file in os.listdir(pdf_folder):
        if not pdf_file.lower().endswith(".pdf"):
            continue
        path = os.path.join(pdf_folder, pdf_file)
        text = ""
        doc = fitz.open(path)
        for page in doc:
            page_text = page.get_text("text")  # 기본 텍스트 추출
            text += page_text + "\n"
        docs.append(Document(page_content=text, metadata={"source": pdf_file}))
    return docs