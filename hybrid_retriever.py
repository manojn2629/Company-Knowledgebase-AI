from rank_bm25 import BM25Okapi
from retriever import get_vectorstore


def hybrid_search(query, filter_type=None):
    vectorstore = get_vectorstore()

    kwargs = {"k": 10, "fetch_k": 100}
    if filter_type:
        kwargs["filter"] = {"type": filter_type}

    faiss_docs = vectorstore.similarity_search(
        query,
        **kwargs
    )

    if not faiss_docs:
        return []

    tokenized_docs = [
        doc.page_content.split()
        for doc in faiss_docs
    ]

    bm25 = BM25Okapi(tokenized_docs)

    bm25_docs = bm25.get_top_n(
        query.split(),
        faiss_docs,
        n=5
    )

    merged_docs = []
    seen = set()

    for doc in faiss_docs + bm25_docs:
        if doc.page_content not in seen:
            merged_docs.append(doc)
            seen.add(doc.page_content)

    return merged_docs