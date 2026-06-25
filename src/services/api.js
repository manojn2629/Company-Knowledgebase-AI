const BASE_URL = "http://127.0.0.1:8000";

export const sendMessage = async (question, sessionId = null) => {
    try {
        const email = localStorage.getItem("userEmail");
        const response = await fetch(`${BASE_URL}/chat`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({ question, email, session_id: sessionId }),
        });

        const data = await response.json();
        return data;
    } catch (error) {
        console.error("API Error:", error);

        return {
            answer: "Backend connection failed.",
        };
    }
};

export const uploadDocument = async (file) => {
    const formData = new FormData();
    formData.append("file", file);

    try {
        const response = await fetch(`${BASE_URL}/upload`, {
            method: "POST",
            body: formData,
        });

        return await response.json();
    } catch (error) {
        console.error("Upload Error:", error);
    }
};

export const signup = async (email, password) => {
    try {
        const response = await fetch(`${BASE_URL}/signup`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({ email, password }),
        });
        return await response.json();
    } catch (error) {
        console.error("Signup Error:", error);
        return { status: "error", message: "Backend connection failed." };
    }
};

export const login = async (email, password) => {
    try {
        const response = await fetch(`${BASE_URL}/login`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({ email, password }),
        });
        return await response.json();
    } catch (error) {
        console.error("Login Error:", error);
        return { status: "error", message: "Backend connection failed." };
    }
};

export const fetchSessions = async (email) => {
    try {
        const response = await fetch(`${BASE_URL}/sessions?email=${encodeURIComponent(email)}`);
        return await response.json();
    } catch (error) {
        console.error("Fetch Sessions Error:", error);
        return { status: "error", sessions: [] };
    }
};

export const createSession = async (email, title) => {
    try {
        const response = await fetch(`${BASE_URL}/sessions`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ email, title })
        });
        return await response.json();
    } catch (error) {
        console.error("Create Session Error:", error);
        return { status: "error", session_id: null };
    }
};

export const fetchMessages = async (sessionId) => {
    try {
        const response = await fetch(`${BASE_URL}/sessions/${sessionId}/messages`);
        return await response.json();
    } catch (error) {
        console.error("Fetch Messages Error:", error);
        return { status: "error", messages: [] };
    }
};

export const transcribeAudio = async (audioBlob) => {
    try {
        const formData = new FormData();
        formData.append("audio", audioBlob, "voice.webm");

        const response = await fetch(`${BASE_URL}/transcribe`, {
            method: "POST",
            body: formData,
        });
        return await response.json();
    } catch (error) {
        console.error("Transcription Error:", error);
        return { error: "Failed to transcribe audio." };
    }
};
