from langchain_groq import ChatGroq
from dotenv import load_dotenv
import os

load_dotenv()

llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    api_key=os.getenv("GROQ_API_KEY")
)


def reflect_answer(answer):
    prompt = f"""
Improve this answer and make it clearer.

Answer:
{answer}
"""

    response = llm.invoke(prompt)

    return response.content