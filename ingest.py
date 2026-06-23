from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_core.documents import Document
import pdfplumber

from utils import get_pdf_files

load_dotenv()

DATA_FOLDER = "data"
VECTOR_FOLDER = "vectorstore"


def extract_tables(pdf_path):
    table_docs = []

    with pdfplumber.open(pdf_path) as pdf:
        for page_num, page in enumerate(pdf.pages):
            tables = page.extract_tables()

            for table in tables:
                for row in table:
                    row_text = " | ".join(
                        [str(cell) if cell else "" for cell in row]
                    )

                    table_docs.append(
                        Document(
                            page_content=row_text,
                            metadata={
                                "source": pdf_path,
                                "page": page_num + 1
                            }
                        )
                    )

    return table_docs


def ingest_documents():
    all_docs = []

    pdf_files = get_pdf_files(DATA_FOLDER)

    if not pdf_files:
        print("No PDF files found.")
        return

    for pdf in pdf_files:
        print(f"Loading: {pdf}")

        # normal text
        loader = PyPDFLoader(pdf)
        docs = loader.load()

        for doc in docs:
            doc.metadata["source"] = pdf

        all_docs.extend(docs)

        # table extraction
        table_docs = extract_tables(pdf)
        all_docs.extend(table_docs)

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=100
    )

    chunks = splitter.split_documents(all_docs)

    print(f"Total chunks created: {len(chunks)}")

    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

    vectorstore = FAISS.from_documents(
        chunks,
        embeddings
    )

    vectorstore.save_local(VECTOR_FOLDER)

    print("Vectorstore saved successfully.")


if __name__ == "__main__":
    ingest_documents()