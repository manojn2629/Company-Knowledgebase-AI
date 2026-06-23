import streamlit as st
import os
import subprocess
import sys
from graph import app_graph
from memory import get_chat_memory
from image_query import extract_text_from_image


# Page config
st.set_page_config(
    page_title="Company Knowledgebase AI",
    page_icon="🤖",
    layout="wide"
)

# Session state
if "messages" not in st.session_state:
    st.session_state.messages = []

if "uploaded_files" not in st.session_state:
    st.session_state.uploaded_files = []

if "latest_image_text" not in st.session_state:
    st.session_state.latest_image_text = ""


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

    # Upload Documents
    st.markdown("### Upload Documents")
    uploaded_files = st.file_uploader(
        "Upload Files",
        type=["pdf", "csv", "xlsx", "png", "jpg"],
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

                # OCR for uploaded images
                if file.name.endswith(".png") or file.name.endswith(".jpg"):
                    extracted_text = extract_text_from_image(file_path)

                    txt_path = file_path + ".txt"

                    with open(txt_path, "w", encoding="utf-8") as txt_file:
                        txt_file.write(extracted_text)

            st.success("Files uploaded successfully.")

            for file in uploaded_files:
                st.caption(f"Uploaded: {file.name}")

            # Auto ingest
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
    → Query Expansion  
    → Hybrid Retrieval  
    → Table Extraction  
    → OCR Extraction  
    → Excel/CSV Search  
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


# Chat Input + Upload Icon
col_chat, col_upload = st.columns([12, 1])

with col_chat:
    user_input = st.chat_input(
        "Ask anything about company knowledge..."
    )

with col_upload:
    st.markdown("""
    <style>
    div[data-testid="stFileUploader"] {
        width: 40px !important;
    }

    div[data-testid="stFileUploader"] section {
        border: none !important;
        padding: 0 !important;
        background: transparent !important;
    }

    div[data-testid="stFileUploaderDropzone"] {
        min-height: 40px !important;
        padding: 0 !important;
        border: none !important;
        background: transparent !important;
    }

    div[data-testid="stFileUploaderDropzoneInstructions"] {
        display: none !important;
    }

    div[data-testid="stBaseButton-secondary"] {
        display: none !important;
    }

    .upload-icon {
        font-size: 24px;
        cursor: pointer;
        text-align: center;
        margin-top: 8px;
    }
    </style>
    """, unsafe_allow_html=True)

    st.markdown(
        '<div class="upload-icon">📎</div>',
        unsafe_allow_html=True
    )

    image_file = st.file_uploader(
        "Upload Image",
        type=["png", "jpg", "jpeg"],
        key="chat_image_upload",
        label_visibility="collapsed"
    )

if suggested_question is not None:
    user_input = suggested_question


# Process uploaded image
if image_file:
    os.makedirs("data", exist_ok=True)

    image_path = os.path.join(
        "data",
        image_file.name
    )

    with open(image_path, "wb") as f:
        f.write(image_file.read())

    extracted_text = extract_text_from_image(
        image_path
    )

    # Save latest OCR text
    st.session_state["latest_image_text"] = extracted_text

    txt_path = image_path + ".txt"

    with open(txt_path, "w", encoding="utf-8") as txt_file:
        txt_file.write(extracted_text)

    with st.spinner("Indexing uploaded image..."):
        process = subprocess.run(
            [sys.executable, "ingest.py"],
            capture_output=True,
            text=True
        )

    if process.returncode == 0:
        st.success("Image uploaded and indexed successfully.")
    else:
        st.error("Image indexing failed.")
        st.code(process.stderr)


# Main chat process
if user_input:
    st.session_state.messages.append({
        "role": "user",
        "content": user_input
    })

    with st.chat_message("user"):
        st.markdown(user_input)

    with st.chat_message("assistant"):
        with st.spinner("Searching knowledgebase..."):

            query_text = user_input

            # Inject latest uploaded image OCR text
            if st.session_state["latest_image_text"]:
                query_text += (
                    "\n\nUploaded Image Content:\n"
                    + st.session_state["latest_image_text"]
                )

            result = app_graph.invoke({
                "question": query_text
            })

        answer = result.get("answer", "No answer found.")
        sources = result.get("sources", [])
        confidence = float(result.get("confidence", 0))

        if "Internet Search" in sources:
            st.info("🌐 Source: Internet")
        else:
            st.success("📄 Source: Internal Documents")

        st.markdown(answer)

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
        st.caption(f"Retrieved {len(sources)} sources")

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

        st.markdown("### Feedback")

        col1, col2 = st.columns(2)

        with col1:
            if st.button("👍 Helpful"):
                st.success("Thanks for your feedback!")

        with col2:
            if st.button("👎 Not Helpful"):
                st.warning("Feedback noted.")

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