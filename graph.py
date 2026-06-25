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


# Load LLM
llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    api_key=os.getenv("GROQ_API_KEY"),
    temperature=0
)


# Graph State
class GraphState(TypedDict, total=False):
    question: str
    rewritten_question: str
    expanded_question: str
    context: str
    answer: str
    sources: List[str]
    confidence: float
    validation: str


# Step 1: Rewrite Query
def rewrite(state):
    prompt = f"""
Rewrite the user query for better retrieval.

Rules:
1. Keep original meaning.
2. Make it clear and searchable.
3. Expand abbreviations.
4. Keep important names, IDs, and values.
5. Return only rewritten query.

User Query:
{state["question"]}
"""

    response = llm.invoke(prompt)

    rewritten_query = response.content.strip()

    print("\nOriginal Query:", state["question"])
    print("Rewritten Query:", rewritten_query)

    return {
        "question": state["question"],
        "rewritten_question": rewritten_query
    }


# Step 2: Expand Query
def expand(state):
    expanded = expand_query(
        state["rewritten_question"]
    )

    print("\nExpanded Query:", expanded)

    return {
        "expanded_question": expanded
    }


# Step 3: Retrieve Documents
def retrieve(state):
    if "image" in state["question"].lower():
        docs = hybrid_search(
            state["expanded_question"],
            filter_type="ocr_image"
        )
    else:
        docs = hybrid_search(
            state["expanded_question"]
        )

    print("\nQuestion:", state["question"])
    print("Retrieved Docs:", len(docs))

    route = route_query(
        state["question"],
        docs
    )

    print("Route Decision:", route)

    if route == "web":
        return {
            "context": "",
            "sources": [],
            "confidence": 0
        }

    if route == "retry":
        if "image" in state["question"].lower():
            docs = hybrid_search(
                state["rewritten_question"],
                filter_type="ocr_image"
            )
        else:
            docs = hybrid_search(
                state["rewritten_question"]
            )

        print("Retry Docs:", len(docs))

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

    print("Reranked Docs:", len(docs))

    if not docs:
        return {
            "context": "",
            "sources": [],
            "confidence": 0
        }

    context = "\n\n".join([
        doc.page_content for doc in docs
    ])

    sources = []

    for doc in docs:
        source = doc.metadata.get(
            "source",
            "Unknown"
        )

        page = doc.metadata.get(
            "page",
            "N/A"
        )

        source_text = f"{source} | Page {page}"

        if source_text not in sources:
            sources.append(source_text)

    confidence = min(
        len(docs) * 20,
        100
    )

    return {
        "context": context,
        "sources": sources,
        "confidence": confidence
    }


# Step 4: Generate Answer
def generate(state):
    if not state.get("context"):
        return {
            "answer": "NOT_FOUND"
        }

    prompt = f"""
You are an internal company knowledge assistant.

STRICT RULES:
1. Answer ONLY from context.
2. Never use outside knowledge.
3. Be short and precise.
4. Use bullet points.
5. Mention exact values.
6. Add source citations.
7. If answer not found, return ONLY NOT_FOUND.

Context:
{state["context"]}

Question:
{state["question"]}
"""

    response = llm.invoke(prompt)

    answer = response.content.strip()

    print("\nGenerated Answer:", answer)

    return {
        "answer": answer
    }


# Step 5: Validate Answer
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

        print("Validation:", result)

        # Safety fallback
        if result not in ["VALID", "INVALID"]:
            result = "VALID"

    except Exception as e:
        print("Validation Error:", e)
        result = "VALID"

    return {
        "validation": result
    }

# Decide next node
def decide_next(state):
    # Only go to web if NO answer found
    if state["answer"] == "NOT_FOUND":
        return "web_search"

    return "reflect"


# Step 6: Web Search Fallback
def web_fallback(state):
    print("\nUsing Web Fallback")

    web_answer = search_web(
        state["question"]
    )

    return {
        "answer": web_answer,
        "sources": ["Internet Search"],
        "confidence": 100
    }


# Step 7: Reflection
def reflect(state):
    improved_answer = reflect_answer(
        state["question"] + "\n" + state["answer"]
    )

    save_chat(
        state["question"],
        improved_answer
    )

    print("\nFinal Answer:", improved_answer)

    return {
        "answer": improved_answer,
        "sources": state["sources"],
        "confidence": state["confidence"]
    }


# Build Workflow
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

# Compile Graph
app_graph = workflow.compile()


# Runner
def run_graph(question):
    result = app_graph.invoke({
        "question": question
    })

    return result