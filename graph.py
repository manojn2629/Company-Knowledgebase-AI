from langgraph.prebuilt import create_react_agent
from langchain_groq import ChatGroq
from dotenv import load_dotenv
import os

from tools import agent_tools
from memory import save_chat

load_dotenv()

# Load LLM
llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    api_key=os.getenv("GROQ_API_KEY"),
    temperature=0
)

# System Prompt
system_prompt = """
You are an intelligent internal company knowledge assistant.
Your goal is to answer user queries accurately, clearly, and concisely.
You have access to a set of tools. ALWAYS use your tools when you need to lookup information.

Rules:
1. ALWAYS use the `search_knowledgebase` tool FIRST when asked about company policies, internal data, or documentation.
2. If the answer is not in the knowledgebase, you may use the `web_search_tool` to find external information.
3. OUTPUT FORMAT: Be clear and ALWAYS format your output using bullet points.
4. CITATIONS: ALWAYS include citations for the sources you used directly in your text (e.g., "[Source: DocumentName.pdf]").
5. If you cannot find the answer anywhere, clearly state that you do not know.
6. Do NOT guess or make up tool names. ONLY use the tools exactly as provided to you.
"""

# Compile the ReAct Agent Graph
app_graph = create_react_agent(llm, tools=agent_tools, prompt=system_prompt)

# Runner
def run_graph(question):
    # Run the agent
    result = app_graph.invoke({"messages": [("user", question)]})
    
    # Extract the final answer
    messages = result.get("messages", [])
    final_message = messages[-1].content if messages else "No response generated."
    
    # Extract tool usage for sources
    sources = []
    for msg in messages:
        if msg.type == "tool":
            sources.append(f"Tool Invoked: {msg.name}")
    
    # De-duplicate sources
    sources = list(set(sources))
    
    # Save the chat to memory (optional, maintaining original behavior)
    save_chat(question, final_message)
    
    # Return formatted result matching old contract for app.py
    return {
        "answer": final_message,
        "sources": sources,
        "confidence": 100 if final_message else 0,
        "question": question,
        "rewritten_question": "",
        "expanded_question": ""
    }

def run_graph_stream(question):
    content_length = 0
    try:
        for msg, metadata in app_graph.stream({"messages": [("user", question)]}, stream_mode="messages"):
            msg_type = getattr(msg, "type", "")
            node_name = metadata.get("langgraph_node", "")
            if msg.content and node_name == "agent" and (msg_type == "ai" or msg_type == "AIMessageChunk" or "AIMessage" in str(type(msg))):
                # The agent might yield tool calls as well, we only want the text content
                content_length += len(msg.content)
                yield msg.content
    except Exception as e:
        if content_length < 10:
            yield f"\n\n[Error from AI Provider: {str(e)}]"