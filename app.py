from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
import os
import subprocess
import sys
import sqlite3
import hashlib

from graph import run_graph, run_graph_stream
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
    try:
        cursor.execute("ALTER TABLE users ADD COLUMN role TEXT DEFAULT 'user'")
    except sqlite3.OperationalError:
        pass
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
        role = "admin" if request.email == "admin@company.com" else "user"
        cursor.execute("INSERT INTO users (email, password, role) VALUES (?, ?, ?)", (request.email, hashed_pw, role))
        conn.commit()
        conn.close()
        return {"status": "success", "message": "User registered successfully", "role": role}
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
        cursor.execute("SELECT id, role FROM users WHERE email = ? AND password = ?", (request.email, hashed_pw))
        user = cursor.fetchone()
        conn.close()
        
        if user:
            return {"status": "success", "message": "Login successful", "role": user[1]}
        else:
            return {"status": "error", "message": "Invalid email or password"}
    except Exception as e:
        return {"status": "error", "message": str(e)}

@app.get("/metrics")
def get_metrics():
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM users")
        total_users = cursor.fetchone()[0]
        cursor.execute("SELECT COUNT(*) FROM sessions")
        total_sessions = cursor.fetchone()[0]
        cursor.execute("SELECT COUNT(*) FROM messages")
        total_messages = cursor.fetchone()[0]
        conn.close()
        return {
            "status": "success",
            "metrics": {
                "total_users": total_users,
                "total_sessions": total_sessions,
                "total_messages": total_messages
            }
        }
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

@app.post("/chat/stream")
async def chat_stream(request: ChatRequest):
    try:
        if request.session_id:
            conn = sqlite3.connect(DB_PATH)
            cursor = conn.cursor()
            cursor.execute("INSERT INTO messages (session_id, sender, text) VALUES (?, ?, ?)", 
                           (request.session_id, "user", request.question))
            conn.commit()
            conn.close()

        def event_generator():
            import json
            full_response = ""
            for chunk in run_graph_stream(request.question):
                full_response += chunk
                yield f"data: {json.dumps(chunk)}\n\n"
            
            if request.session_id:
                conn = sqlite3.connect(DB_PATH)
                cursor = conn.cursor()
                cursor.execute("INSERT INTO messages (session_id, sender, text) VALUES (?, ?, ?)", 
                               (request.session_id, "ai", full_response))
                conn.commit()
                conn.close()
                
            yield "data: [DONE]\n\n"

        return StreamingResponse(event_generator(), media_type="text/event-stream")

    except Exception as e:
        def error_gen():
            yield f"data: Error: {str(e)}\n\n"
            yield "data: [DONE]\n\n"
        return StreamingResponse(error_gen(), media_type="text/event-stream")


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

import base64

@app.post("/vision")
async def vision_query(file: UploadFile = File(...)):
    try:
        content = await file.read()
        base64_image = base64.b64encode(content).decode('utf-8')
        
        completion = groq_client.chat.completions.create(
            model="llama-3.2-11b-vision-preview",
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": "Analyze this image and describe what it contains in detail."
                        },
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{base64_image}",
                            }
                        }
                    ]
                }
            ],
            temperature=0,
            max_tokens=1024,
        )
        return {"status": "success", "text": completion.choices[0].message.content}
    except Exception as e:
        print("VISION ERROR:", str(e))
        return {"status": "error", "message": str(e)}