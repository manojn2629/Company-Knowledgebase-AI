import { useState } from "react";
import { motion } from "framer-motion";
import DashboardNavbar from "../components/layout/DashboardNavbar";
import Sidebar from "../components/layout/Sidebar";
import RightPanel from "../components/layout/RightPanel";
import FloatingInput from "../components/layout/FloatingInput";
import ChatWindow from "../components/chat/ChatWindow";
import AnimatedBackground from "../components/ui/AnimatedBackground";
import { sendMessage, createSession, fetchMessages } from "../services/api";

function Dashboard() {
    const [messages, setMessages] = useState([]);
    const [sessionId, setSessionId] = useState(null);
    const [refreshTrigger, setRefreshTrigger] = useState(0);

    const [thinking, setThinking] = useState(false);
    const [uploadedFile, setUploadedFile] = useState(null);
    const [queryDetails, setQueryDetails] = useState(null);

    const handleFileUpload = (fileName) => {
        setUploadedFile(fileName);
    };

    const handleSessionSelect = async (id) => {
        setSessionId(id);
        const res = await fetchMessages(id);
        if (res?.status === "success") {
            setMessages(res.messages);
        }
    };

    const handleNewSession = () => {
        setSessionId(null);
        setMessages([]);
    };

    const handleExportChat = () => {
        if (messages.length === 0) {
            alert("No messages to export.");
            return;
        }

        let content = "# Chat Export\n\n";
        messages.forEach(msg => {
            const sender = msg.sender === "user" ? "You" : "AI";
            content += `**${sender}:**\n${msg.text}\n\n---\n\n`;
        });

        const blob = new Blob([content], { type: "text/markdown" });
        const url = URL.createObjectURL(blob);
        const a = document.createElement("a");
        a.href = url;
        a.download = `chat-export-${sessionId || "new"}.md`;
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        URL.revokeObjectURL(url);
    };

    const handleSend = async (input) => {
        const userMessage = { sender: "user", text: input };
        setMessages((prev) => [...prev, userMessage]);
        setThinking(true);

        try {
            let currentSessionId = sessionId;
            const email = localStorage.getItem("userEmail");

            if (!currentSessionId && email) {
                const title = input.length > 25 ? input.substring(0, 25) + "..." : input;
                const res = await createSession(email, title);
                if (res?.status === "success") {
                    currentSessionId = res.session_id;
                    setSessionId(currentSessionId);
                    setRefreshTrigger(prev => prev + 1);
                }
            }

            setMessages((prev) => [...prev, { sender: "ai", text: "" }]);
            setThinking(false);

            const response = await fetch("http://127.0.0.1:8000/chat/stream", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ question: input, email: email, session_id: currentSessionId }),
            });

            const reader = response.body.getReader();
            const decoder = new TextDecoder("utf-8");
            let done = false;
            let buffer = "";

            while (!done) {
                const { value, done: readerDone } = await reader.read();
                done = readerDone;
                if (value) {
                    buffer += decoder.decode(value, { stream: true });
                    const events = buffer.split("\n\n");
                    buffer = events.pop(); // Keep partial event in buffer

                    for (let event of events) {
                        if (event.startsWith("data: ")) {
                            const dataStr = event.substring(6);
                            if (dataStr === "[DONE]") continue;
                            try {
                                const textChunk = JSON.parse(dataStr);
                                setMessages((prev) => {
                                    const newMessages = [...prev];
                                    const lastMsg = { ...newMessages[newMessages.length - 1] };
                                    lastMsg.text += textChunk;
                                    newMessages[newMessages.length - 1] = lastMsg;
                                    return newMessages;
                                });
                            } catch (e) {
                                console.error("Error parsing chunk", dataStr);
                            }
                        }
                    }
                }
            }
        } catch (error) {
            setMessages((prev) => {
                const newMessages = [...prev];
                newMessages[newMessages.length - 1].text = "Backend connection failed.";
                return newMessages;
            });
            setThinking(false);
        }
    };

    return (
        <motion.div
            className="h-screen bg-black text-white relative flex flex-col overflow-hidden"
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ duration: 0.8 }}
        >
            <AnimatedBackground />

            <DashboardNavbar />

            {/* Main Layout */}
            <div className="flex flex-1 overflow-hidden">
                <Sidebar 
                    onFileUpload={handleFileUpload} 
                    onSessionSelect={handleSessionSelect}
                    onNewSession={handleNewSession}
                    refreshTrigger={refreshTrigger}
                    onExportChat={handleExportChat}
                />

                {/* Chat Section */}
                <ChatWindow
                    messages={messages}
                    thinking={thinking}
                />

                <RightPanel details={queryDetails} />
            </div>

            {/* Floating Input */}
            <FloatingInput onSend={handleSend} />
        </motion.div>
    );
}

export default Dashboard;