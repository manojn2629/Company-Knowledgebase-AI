from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os
import subprocess
import sys
import sqlite3
import hashlib

from graph import run_graph
from groq import Groq

groq_client = Groq(api_key=os.getenv("GROQ_API_KEY"))

app = FastAPI(
    title="Company Knowledgebase API"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

DATA_FOLDER = "data"
os.makedirs(DATA_FOLDER, exist_ok=True)

# DB Setup
DB_PATH = "auth.db"

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS sessions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT NOT NULL,
            title TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            session_id INTEGER NOT NULL,
            sender TEXT NOT NULL,
            text TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(session_id) REFERENCES sessions(id)
        )
    ''')
    conn.commit()
    conn.close()

init_db()

def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()

class ChatRequest(BaseModel):
    question: str
    email: str = None
    session_id: int = None

class AuthRequest(BaseModel):
    email: str
    password: str

class SessionRequest(BaseModel):
    email: str
    title: str


@app.get("/")
def home():
    return {
        "message": "Backend Running"
    }

@app.post("/signup")
def signup(request: AuthRequest):
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        hashed_pw = hash_password(request.password)
        cursor.execute("INSERT INTO users (email, password) VALUES (?, ?)", (request.email, hashed_pw))
        conn.commit()
        conn.close()
        return {"status": "success", "message": "User registered successfully"}
    except sqlite3.IntegrityError:
        return {"status": "error", "message": "Email already exists"}
    except Exception as e:
        return {"status": "error", "message": str(e)}

@app.post("/login")
def login(request: AuthRequest):
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        hashed_pw = hash_password(request.password)
        cursor.execute("SELECT id FROM users WHERE email = ? AND password = ?", (request.email, hashed_pw))
        user = cursor.fetchone()
        conn.close()
        
        if user:
            return {"status": "success", "message": "Login successful"}
        else:
            return {"status": "error", "message": "Invalid email or password"}
    except Exception as e:
        return {"status": "error", "message": str(e)}

@app.post("/sessions")
def create_session(request: SessionRequest):
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("INSERT INTO sessions (email, title) VALUES (?, ?)", (request.email, request.title))
        session_id = cursor.lastrowid
        conn.commit()
        conn.close()
        return {"status": "success", "session_id": session_id}
    except Exception as e:
        return {"status": "error", "message": str(e)}

@app.get("/sessions")
def get_sessions(email: str):
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("SELECT id, title, created_at FROM sessions WHERE email = ? ORDER BY created_at DESC", (email,))
        sessions = [{"id": row[0], "title": row[1], "created_at": row[2]} for row in cursor.fetchall()]
        conn.close()
        return {"status": "success", "sessions": sessions}
    except Exception as e:
        return {"status": "error", "message": str(e)}

@app.get("/sessions/{session_id}/messages")
def get_messages(session_id: int):
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("SELECT sender, text FROM messages WHERE session_id = ? ORDER BY created_at ASC", (session_id,))
        messages = [{"sender": row[0], "text": row[1]} for row in cursor.fetchall()]
        conn.close()
        return {"status": "success", "messages": messages}
    except Exception as e:
        return {"status": "error", "message": str(e)}


@app.post("/chat")
async def chat(request: ChatRequest):
    try:
        if request.session_id:
            conn = sqlite3.connect(DB_PATH)
            cursor = conn.cursor()
            cursor.execute("INSERT INTO messages (session_id, sender, text) VALUES (?, ?, ?)", 
                           (request.session_id, "user", request.question))
            conn.commit()
            conn.close()

        result = run_graph(
            request.question
        )

        answer = result.get("answer", "Error generating answer")

        if request.session_id:
            conn = sqlite3.connect(DB_PATH)
            cursor = conn.cursor()
            cursor.execute("INSERT INTO messages (session_id, sender, text) VALUES (?, ?, ?)", 
                           (request.session_id, "ai", answer))
            conn.commit()
            conn.close()

        return {
            "answer": answer,
            "sources": result.get("sources", []),
            "confidence": result.get("confidence", 0),
            "original_query": result.get("question", ""),
            "rewritten_query": result.get("rewritten_question", ""),
            "expanded_query": result.get("expanded_question", "")
        }

    except Exception as e:
        return {
            "answer": str(e),
            "sources": [],
            "confidence": 0
        }


@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    try:
        file_path = os.path.join(
            DATA_FOLDER,
            file.filename
        )

        # Save uploaded file
        with open(file_path, "wb") as f:
            content = await file.read()
            f.write(content)

        print(f"Saved file: {file.filename}")

        # Run ingestion
        process = subprocess.run(
            [sys.executable, "ingest.py"],
            capture_output=True,
            text=True
        )

        print("INGEST STDOUT:", process.stdout)
        print("INGEST STDERR:", process.stderr)

        # If ingestion failed
        if process.returncode != 0:
            return {
                "status": "error",
                "message": process.stderr,
                "indexed": False
            }

        # Success response
        return {
            "status": "success",
            "message": f"{file.filename} uploaded and indexed successfully",
            "indexed": True,
            "indexed_file": file.filename
        }

    except Exception as e:
        print("UPLOAD ERROR:", str(e))

        return {
            "status": "error",
            "message": str(e),
            "indexed": False
        }

@app.post("/transcribe")
async def transcribe(audio: UploadFile = File(...)):
    try:
        audio_path = f"temp_{audio.filename}"
        with open(audio_path, "wb") as f:
            f.write(await audio.read())
        
        with open(audio_path, "rb") as file:
            transcription = groq_client.audio.transcriptions.create(
                file=(audio_path, file.read()),
                model="whisper-large-v3",
                response_format="json",
            )
        
        os.remove(audio_path)
        return {"text": transcription.text}
    except Exception as e:
        return {"error": str(e)}