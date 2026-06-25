from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
import os

VECTOR_FOLDER = "vectorstore"


def get_vectorstore():
    if not os.path.exists(VECTOR_FOLDER):
        raise FileNotFoundError(
            "Vectorstore not found. Upload and ingest documents first."
        )

    embeddings = HuggingFaceEmbeddings(
        model_name="BAAI/bge-small-en-v1.5"
    )

    vectorstore = FAISS.load_local(
        VECTOR_FOLDER,
        embeddings,
        allow_dangerous_deserialization=True
    )

    return vectorstore