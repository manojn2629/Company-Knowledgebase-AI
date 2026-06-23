def route_query(question, retrieved_docs):
    if not retrieved_docs:
        return "web"

    if len(retrieved_docs) < 2:
        return "retry"

    return "generate"