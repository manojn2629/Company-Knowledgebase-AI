# Company Knowledgebase AI 🧠

A state-of-the-art enterprise Retrieval-Augmented Generation (RAG) system with a FastAPI backend, Groq LLM intelligence, FAISS vector search, OCR image processing, voice transcription, and a beautiful React frontend.

---

## 🚀 Getting Started

Follow these step-by-step instructions to get the application running on your local machine.

### 1. Clone the Repository
Open your terminal and clone the repository from GitHub:
```bash
git clone https://github.com/manojn2629/Company-Knowledgebase-AI.git
cd Company-Knowledgebase-AI
```

### 2. Backend Setup (Python / FastAPI)
The backend handles the AI routing, database memory, FAISS retrieval, and Whisper voice transcription.

1. **Create a Virtual Environment**:
   ```bash
   python -m venv venv
   ```

2. **Activate the Virtual Environment**:
   - On **Windows**:
     ```bash
     venv\Scripts\activate
     ```
   - On **Mac/Linux**:
     ```bash
     source venv/bin/activate
     ```

3. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Environment Variables**:
   Create a `.env` file in the root folder (where `app.py` is) and add your Groq and Tavily API keys:
   ```env
   GROQ_API_KEY=your_groq_api_key_here
   TAVILY_API_KEY=your_tavily_api_key_here
   ```

5. **Start the Backend Server**:
   ```bash
   python -m uvicorn app:app --reload
   ```
   *The backend will now be running on `http://127.0.0.1:8000`.*

---

### 3. Frontend Setup (React / Vite)
The frontend is a beautiful, animated dashboard built with React and Tailwind CSS.

1. **Open a NEW Terminal window** (keep the backend terminal running).

2. **Navigate into the frontend folder**:
   ```bash
   cd frontend
   ```

3. **Install Node Modules**:
   ```bash
   npm install
   ```

4. **Start the Development Server**:
   ```bash
   npm run dev
   ```
   *The frontend will provide you with a `localhost` URL (usually `http://localhost:5173`). Open that link in your browser!*

---

## ✨ Features
- **Agentic Routing**: Automatically routes questions to FAISS, Web Search, or OCR depending on the context.
- **Persistent Chat Memory**: Uses SQLite to store your past sessions and chats securely.
- **Voice Transcription**: Record your voice using the microphone icon (powered by Groq's Whisper API).
- **Intelligent Reranking**: Reorders retrieved chunks for maximum LLM accuracy.
- **Enterprise Security**: Basic login/signup authentication baked into the SQLite database.
