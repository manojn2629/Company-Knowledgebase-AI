from typing import TypedDict, List
from langgraph.graph import StateGraph, END
from langchain_groq import ChatGroq
from dotenv import load_dotenv
import os

from query_expander import expand_query
from hybrid_retriever import hybrid_search
from reranker import rerank_documents
from validator import validate_answer
from reflection import reflect_answer
from web_search import search_web
from memory import save_chat
from agentic_router import route_query

load_dotenv()

llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    api_key=os.getenv("GROQ_API_KEY"),
    temperature=0
)


class GraphState(TypedDict):
    question: str
    expanded_question: str
    context: str
    answer: str
    sources: List[str]
    confidence: float
    validation: str


# Node 1 — Rewrite
def rewrite(state):
    return {
        "question": state["question"]
    }


# Node 2 — Expand Query
def expand(state):
    expanded = expand_query(
        state["question"]
    )

    return {
        "expanded_question": expanded
    }


# Node 3 — Retrieve
def retrieve(state):
    expanded_question = state["expanded_question"]

    docs = hybrid_search(
        expanded_question
    )

    route = route_query(
        state["question"],
        docs
    )

    # No docs → web
    if route == "web":
        return {
            "context": "",
            "sources": [],
            "confidence": 0
        }

    # Retry retrieval with original question
    if route == "retry":
        docs = hybrid_search(
            state["question"]
        )

    if not docs:
        return {
            "context": "",
            "sources": [],
            "confidence": 0
        }

    docs = rerank_documents(
        state["question"],
        docs
    )

    if not docs:
        return {
            "context": "",
            "sources": [],
            "confidence": 0
        }

    context = "\n\n".join([
        doc.page_content for doc in docs
    ])

    sources = list(set([
        f"{doc.metadata.get('source')} | Page {doc.metadata.get('page', 'N/A')}"
        for doc in docs
    ]))

    return {
        "context": context,
        "sources": sources,
        "confidence": 95
    }


# Node 4 — Generate
def generate(state):
    question = state["question"]
    context = state["context"]

    if not context:
        return {
            "answer": "NOT_FOUND"
        }

    prompt = f"""
Answer ONLY from the internal documents.

If answer not found reply ONLY:

NOT_FOUND

Context:
{context}

Question:
{question}
"""

    response = llm.invoke(prompt)

    return {
        "answer": response.content.strip()
    }


# Node 5 — Validate
def validate(state):
    if state["answer"] == "NOT_FOUND":
        return {
            "validation": "INVALID"
        }

    try:
        result = validate_answer(
            state["context"],
            state["answer"]
        )
    except:
        result = "INVALID"

    return {
        "validation": result
    }


# Decision
def decide_next(state):
    if state["validation"] == "INVALID":
        return "web_search"

    return "reflect"


# Node 6 — Web fallback
def web_fallback(state):
    web_answer = search_web(
        state["question"]
    )

    return {
        "answer": web_answer,
        "sources": ["Internet Search"],
        "confidence": 100
    }


# Node 7 — Reflection
def reflect(state):
    improved_answer = reflect_answer(
        state["answer"]
    )

    save_chat(
        state["question"],
        improved_answer
    )

    return {
        "answer": improved_answer,
        "sources": state["sources"],
        "confidence": state["confidence"]
    }


workflow = StateGraph(GraphState)

workflow.add_node("rewrite", rewrite)
workflow.add_node("expand", expand)
workflow.add_node("retrieve", retrieve)
workflow.add_node("generate", generate)
workflow.add_node("validate", validate)
workflow.add_node("web_search", web_fallback)
workflow.add_node("reflect", reflect)

workflow.set_entry_point("rewrite")

workflow.add_edge("rewrite", "expand")
workflow.add_edge("expand", "retrieve")
workflow.add_edge("retrieve", "generate")
workflow.add_edge("generate", "validate")

workflow.add_conditional_edges(
    "validate",
    decide_next,
    {
        "web_search": "web_search",
        "reflect": "reflect"
    }
)

workflow.add_edge("web_search", END)
workflow.add_edge("reflect", END)

app_graph = workflow.compile()