import streamlit as st
import os
import subprocess
import sys
from graph import app_graph
from memory import get_chat_memory


# Page config
st.set_page_config(
    page_title="Knowledgebase AI",
    page_icon="🤖",
    layout="wide"
)

# Session state
if "messages" not in st.session_state:
    st.session_state.messages = []

if "uploaded_files" not in st.session_state:
    st.session_state.uploaded_files = []


# Sidebar
with st.sidebar:
    st.title("⚡ Dashboard")

    st.markdown("### System")
    st.success("Connected")

    st.markdown("### Vector Database")
    st.info("FAISS Ready")

    st.markdown("### Model")
    st.info("Groq - Llama 3.3")

    st.divider()

    # Memory panel
    st.markdown("### Chat Memory")
    memory_data = get_chat_memory()

    if memory_data:
        for item in memory_data[-3:]:
            st.caption(f"Q: {item['question']}")

    st.divider()

    # Upload PDFs
    st.markdown("### Upload Documents")
    uploaded_files = st.file_uploader(
        "Upload PDFs",
        type=["pdf"],
        accept_multiple_files=True
    )

    if uploaded_files:
        current_files = [file.name for file in uploaded_files]

        if current_files != st.session_state.uploaded_files:
            os.makedirs("data", exist_ok=True)

            for file in uploaded_files:
                file_path = os.path.join("data", file.name)

                with open(file_path, "wb") as f:
                    f.write(file.read())

            st.success("Files uploaded successfully.")

            # Run ingest automatically
            with st.spinner("Updating vector database..."):
                process = subprocess.run(
                    [sys.executable, "ingest.py"],
                    capture_output=True,
                    text=True
                )

            if process.returncode == 0:
                st.success("Vectorstore updated successfully.")
            else:
                st.error("Vectorstore update failed.")
                st.code(process.stderr)

            st.session_state.uploaded_files = current_files

            # Force reload vectorstore
            st.rerun()

    st.divider()

    # Export chat
    if st.session_state.messages:
        chat_text = "\n".join(
            [f"{msg['role']}: {msg['content']}" for msg in st.session_state.messages]
        )

        st.download_button(
            label="📥 Export Chat",
            data=chat_text,
            file_name="chat_history.txt",
            mime="text/plain"
        )

    # Clear chat
    if st.button("🗑 Clear Chat"):
        st.session_state.messages = []
        st.rerun()


# Header
st.markdown("""
    <div style="
        background: linear-gradient(90deg,#0f172a,#1e293b);
        padding:20px;
        border-radius:15px;
        text-align:center;
        margin-bottom:20px;
    ">
        <h1 style="color:white;">🤖 Company Knowledgebase AI</h1>
        <p style="color:#cbd5e1;">
            Internal Document + Internet Search Assistant
        </p>
    </div>
""", unsafe_allow_html=True)


# Workflow panel
with st.expander("⚙ System Workflow"):
    st.markdown("""
    Query Rewrite  
    → Internal Document Search  
    → Answer Generation  
    → Validation  
    → Reflection  
    → Internet Fallback
    """)


# Suggested questions
st.markdown("### Suggested Questions")

col1, col2, col3 = st.columns(3)

suggested_question = None

with col1:
    if st.button("What is leave policy?"):
        suggested_question = "What is leave policy?"

with col2:
    if st.button("How do I claim reimbursement?"):
        suggested_question = "How do I claim reimbursement?"

with col3:
    if st.button("How to deploy backend?"):
        suggested_question = "How to deploy backend?"


# Chat history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

        if "confidence" in msg:
            confidence = float(msg["confidence"])
            progress_value = max(0.0, min(confidence / 100.0, 1.0))

            st.markdown("### Confidence Score")
            st.progress(progress_value)
            st.caption(f"{round(confidence, 2)}%")

        if "sources" in msg:
            with st.expander("📂 View Sources"):
                for source in msg["sources"]:
                    st.markdown(f"""
                        <div style="
                            padding:10px;
                            border:1px solid #334155;
                            border-radius:10px;
                            margin-bottom:8px;
                            background-color:#111827;
                        ">
                            📄 {source}
                        </div>
                    """, unsafe_allow_html=True)


# Chat input
user_input = st.chat_input("Ask anything about company knowledge...")

if suggested_question is not None:
    user_input = suggested_question


if user_input:
    # Save user message
    st.session_state.messages.append({
        "role": "user",
        "content": user_input
    })

    with st.chat_message("user"):
        st.markdown(user_input)

    # Assistant response
    with st.chat_message("assistant"):
        with st.spinner("Searching knowledgebase..."):
            result = app_graph.invoke({
                "question": user_input
            })

        answer = result.get("answer", "No answer found.")
        sources = result.get("sources", [])
        confidence = float(result.get("confidence", 0))

        # Source type
        if "Internet Search" in sources:
            st.info("🌐 Source: Internet")
        else:
            st.success("📄 Source: Internal Documents")

        st.markdown(answer)

        # Confidence
        progress_value = max(0.0, min(confidence / 100.0, 1.0))

        st.markdown("### Confidence Score")
        st.progress(progress_value)

        if confidence > 80:
            st.success("High confidence")
        elif confidence > 50:
            st.warning("Medium confidence")
        else:
            st.error("Low confidence")

        st.caption(f"{round(confidence, 2)}%")

        # Source count
        st.caption(f"Retrieved {len(sources)} sources")

        # Sources
        if sources:
            with st.expander("📂 View Sources"):
                for source in sources:
                    st.markdown(f"""
                        <div style="
                            padding:10px;
                            border:1px solid #334155;
                            border-radius:10px;
                            margin-bottom:8px;
                            background-color:#111827;
                        ">
                            📄 {source}
                        </div>
                    """, unsafe_allow_html=True)

        # Feedback
        st.markdown("### Feedback")

        col1, col2 = st.columns(2)

        with col1:
            if st.button("👍 Helpful"):
                st.success("Thanks for your feedback!")

        with col2:
            if st.button("👎 Not Helpful"):
                st.warning("Feedback noted.")

    # Save assistant response
    st.session_state.messages.append({
        "role": "assistant",
        "content": answer,
        "sources": sources,
        "confidence": confidence
    })


# Footer
st.markdown("""
    <hr>
    <div style="text-align:center; color:gray; padding:10px;">
        Built with LangChain | LangGraph | FAISS | Groq
    </div>
""", unsafe_allow_html=True)