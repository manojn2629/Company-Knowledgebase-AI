from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings

VECTOR_FOLDER = "vectorstore"

# Load embedding model once
embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)


def get_vectorstore():
    vectorstore = FAISS.load_local(
        VECTOR_FOLDER,
        embeddings,
        allow_dangerous_deserialization=True
    )

    return vectorstore