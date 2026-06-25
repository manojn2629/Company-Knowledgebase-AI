def route_query(question, retrieved_docs):
    if not retrieved_docs:
        return "retry"

    return "generate"