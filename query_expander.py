from langchain_groq import ChatGroq
from dotenv import load_dotenv
import os

load_dotenv()

llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    api_key=os.getenv("GROQ_API_KEY")
)


def expand_query(question):
    prompt = f"""
Expand this query for better retrieval.

Question:
{question}
"""

    response = llm.invoke(prompt)

    return response.content