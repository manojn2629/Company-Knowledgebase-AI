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

    const handleSend = async (input) => {
        const userMessage = {
            sender: "user",
            text: input,
        };

        // Add user message
        setMessages((prev) => [...prev, userMessage]);

        // Show thinking
        setThinking(true);

        try {
            let currentSessionId = sessionId;
            const email = localStorage.getItem("userEmail");

            // Create new session if none exists
            if (!currentSessionId && email) {
                const title = input.length > 25 ? input.substring(0, 25) + "..." : input;
                const res = await createSession(email, title);
                if (res?.status === "success") {
                    currentSessionId = res.session_id;
                    setSessionId(currentSessionId);
                    setRefreshTrigger(prev => prev + 1);
                }
            }

            const response = await sendMessage(input, currentSessionId);

            const aiMessage = {
                sender: "ai",
                text: response.answer || "No response from backend.",
            };

            setMessages((prev) => [...prev, aiMessage]);

            setQueryDetails({
                original: response.original_query,
                rewritten: response.rewritten_query,
                expanded: response.expanded_query,
                sources: response.sources,
                confidence: response.confidence
            });
        } catch (error) {
            const errorMessage = {
                sender: "ai",
                text: "Backend connection failed.",
            };

            setMessages((prev) => [...prev, errorMessage]);
        }

        setThinking(false);
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