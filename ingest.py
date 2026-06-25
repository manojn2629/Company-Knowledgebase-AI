from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from langchain.schema import Document

from ocr_reader import extract_ocr_text
from excel_loader import load_excel
from chart_extractor import extract_chart_text

import pdfplumber
import os
import shutil

load_dotenv()

DATA_FOLDER = "data"
VECTOR_FOLDER = "vectorstore"

os.makedirs(DATA_FOLDER, exist_ok=True)


def ingest_documents():
    all_docs = []

    files = os.listdir(DATA_FOLDER)

    if not files:
        print("No files found in data folder")
        return

    for file in files:
        file_path = os.path.join(DATA_FOLDER, file)

        # ---------------- PDF ----------------
        if file.endswith(".pdf"):
            print(f"Loading PDF: {file}")

            loader = PyPDFLoader(file_path)
            docs = loader.load()

            for doc in docs:
                doc.metadata["source"] = file
                doc.metadata["type"] = "pdf"
                doc.metadata["citation"] = f"{file} | Page {doc.metadata.get('page', 'N/A')}"

            all_docs.extend(docs)

            # Table Extraction
            with pdfplumber.open(file_path) as pdf:
                for page_num, page in enumerate(pdf.pages):
                    tables = page.extract_tables()

                    if tables:
                        for table in tables:
                            for row in table:
                                if row:
                                    row_text = " | ".join(
                                        [str(cell) for cell in row if cell]
                                    )

                                    if row_text.strip():
                                        all_docs.append(
                                            Document(
                                                page_content=row_text,
                                                metadata={
                                                    "source": file,
                                                    "page": page_num + 1,
                                                    "type": "table",
                                                    "citation": f"{file} | Table | Page {page_num + 1}"
                                                }
                                            )
                                        )

            # OCR from PDF
            ocr_text = extract_ocr_text(file_path)

            if ocr_text and ocr_text.strip():
                all_docs.append(
                    Document(
                        page_content=ocr_text,
                        metadata={
                            "source": file,
                            "type": "ocr_pdf",
                            "citation": f"{file} | OCR Extract"
                        }
                    )
                )

            # Chart Extraction
            chart_data = extract_chart_text(file_path)

            if chart_data:
                all_docs.append(
                    Document(
                        page_content=" ".join(chart_data),
                        metadata={
                            "source": file,
                            "type": "chart",
                            "citation": f"{file} | Chart Data"
                        }
                    )
                )

        # ---------------- Images OCR ----------------
        elif file.endswith((".png", ".jpg", ".jpeg")):
            print(f"Processing Image OCR: {file}")

            ocr_text = extract_ocr_text(file_path)

            if ocr_text and ocr_text.strip():
                all_docs.append(
                    Document(
                        page_content=ocr_text,
                        metadata={
                            "source": file,
                            "type": "ocr_image",
                            "citation": f"{file} | OCR Image Extract"
                        }
                    )
                )

        # ---------------- Excel / CSV ----------------
        elif file.endswith((".xlsx", ".csv")):
            print(f"Loading Sheet: {file}")

            rows = load_excel(file_path)

            for idx, row in enumerate(rows):
                all_docs.append(
                    Document(
                        page_content=row,
                        metadata={
                            "source": file,
                            "type": "sheet",
                            "row": idx + 1,
                            "citation": f"{file} | Row {idx + 1}"
                        }
                    )
                )

    if not all_docs:
        print("No documents extracted")
        return

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200
    )

    chunks = splitter.split_documents(all_docs)

    print("Total chunks:", len(chunks))

    embeddings = HuggingFaceEmbeddings(
        model_name="BAAI/bge-small-en-v1.5"
    )

    if os.path.exists(VECTOR_FOLDER):
        shutil.rmtree(VECTOR_FOLDER)

    vectorstore = FAISS.from_documents(
        chunks,
        embeddings
    )

    vectorstore.save_local(VECTOR_FOLDER)

    print("Vectorstore saved successfully")


if __name__ == "__main__":
    ingest_documents()