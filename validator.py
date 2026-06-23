from langchain_groq import ChatGroq
from dotenv import load_dotenv
import os

load_dotenv()

llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    api_key=os.getenv("GROQ_API_KEY")
)


def validate_answer(context, answer):
    prompt = f"""
Check if the answer is grounded in context.

Context:
{context}

Answer:
{answer}

Reply ONLY:
VALID
or
INVALID
"""

    response = llm.invoke(prompt)

    return response.content.strip()