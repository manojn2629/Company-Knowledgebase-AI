from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain.schema import Document

from utils import get_pdf_files
from ocr_reader import extract_ocr_text
from excel_loader import load_excel
from chart_extractor import extract_chart_text

import pdfplumber
import os

load_dotenv()

DATA_FOLDER = "data"
VECTOR_FOLDER = "vectorstore"


def ingest_documents():
    all_docs = []

    files = os.listdir(DATA_FOLDER)

    for file in files:
        file_path = os.path.join(DATA_FOLDER, file)

        # PDF files
        if file.endswith(".pdf"):
            print(f"Loading PDF: {file}")

            loader = PyPDFLoader(file_path)
            docs = loader.load()

            # Normal text
            for doc in docs:
                doc.metadata["source"] = file
            all_docs.extend(docs)

            # Table extraction
            with pdfplumber.open(file_path) as pdf:
                for page_num, page in enumerate(pdf.pages):
                    tables = page.extract_tables()

                    for table in tables:
                        for row in table:
                            row_text = " | ".join(
                                [str(cell) for cell in row if cell]
                            )

                            all_docs.append(
                                Document(
                                    page_content=row_text,
                                    metadata={
                                        "source": file,
                                        "page": page_num + 1,
                                        "type": "table"
                                    }
                                )
                            )

            # OCR extraction
            ocr_text = extract_ocr_text(file_path)

            if ocr_text.strip():
                all_docs.append(
                    Document(
                        page_content=ocr_text,
                        metadata={
                            "source": file,
                            "type": "ocr"
                        }
                    )
                )

            # Chart extraction
            chart_data = extract_chart_text(file_path)

            if chart_data:
                all_docs.append(
                    Document(
                        page_content=" ".join(chart_data),
                        metadata={
                            "source": file,
                            "type": "chart"
                        }
                    )
                )

        # Excel / CSV
        elif file.endswith(".xlsx") or file.endswith(".csv"):
            print(f"Loading Sheet: {file}")

            rows = load_excel(file_path)

            for row in rows:
                all_docs.append(
                    Document(
                        page_content=row,
                        metadata={
                            "source": file,
                            "type": "sheet"
                        }
                    )
                )

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200
    )

    chunks = splitter.split_documents(all_docs)

    print(f"Total chunks: {len(chunks)}")

    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

    vectorstore = FAISS.from_documents(
        chunks,
        embeddings
    )

    vectorstore.save_local(VECTOR_FOLDER)

    print("Vectorstore saved successfully")


if __name__ == "__main__":
    ingest_documents()