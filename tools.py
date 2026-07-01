from langchain.tools import tool
from datetime import datetime
from hybrid_retriever import hybrid_search
import os

try:
    from langchain_community.tools.tavily_search import TavilySearchResults
    web_search_tool = TavilySearchResults(max_results=3)
except Exception:
    # Fallback if Tavily is not set up correctly
    @tool
    def web_search_tool(query: str) -> str:
        """Search the web for current events or general knowledge when internal docs don't have the answer."""
        return "Web search is currently unavailable. Ask the user to configure Tavily API key."

@tool
def search_knowledgebase(query: str) -> str:
    """
    Search the internal company knowledgebase for policies, documentation, and specific company data.
    ALWAYS use this tool first when answering questions about the company.
    """
    docs = hybrid_search(query)
    if not docs:
        return "No relevant internal documents found."
    
    # Format the docs
    formatted = []
    for doc in docs:
        source = doc.metadata.get("source", "Unknown")
        formatted.append(f"Source: {source}\nContent: {doc.page_content}")
    
    return "\n\n".join(formatted)

@tool
def get_current_time(query: str = "") -> str:
    """
    Get the current date and time. Useful for answering questions about 'today', 'now', or time-sensitive events.
    """
    return f"The current date and time is {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"

@tool
def calculator(expression: str) -> str:
    """
    Evaluate a simple mathematical expression. Use this for math questions. 
    Example expression: '125 * 34' or '100 / 4'
    """
    try:
        allowed_names = {"__builtins__": None}
        return str(eval(expression, allowed_names, {}))
    except Exception as e:
        return f"Error evaluating math expression: {e}"

agent_tools = [search_knowledgebase, web_search_tool, get_current_time, calculator]
