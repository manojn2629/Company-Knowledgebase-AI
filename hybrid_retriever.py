from rank_bm25 import BM25Okapi
from retriever import get_vectorstore

vectorstore = get_vectorstore()

all_docs = vectorstore.similarity_search("", k=50)

tokenized_docs = [doc.page_content.split() for doc in all_docs]

bm25 = BM25Okapi(tokenized_docs)


def hybrid_search(query):
    faiss_docs = vectorstore.similarity_search(query, k=20)

    bm25_docs = bm25.get_top_n(
        query.split(),
        all_docs,
        n=5
    )

    merged_docs = []

    seen = set()

    for doc in faiss_docs + bm25_docs:
        if doc.page_content not in seen:
            merged_docs.append(doc)
            seen.add(doc.page_content)

    return merged_docs