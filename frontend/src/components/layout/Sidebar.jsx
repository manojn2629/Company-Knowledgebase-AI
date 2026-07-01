import { useState, useEffect } from "react";
import { uploadDocument, fetchSessions } from "../../services/api";
function Sidebar({ onFileUpload, onSessionSelect, onNewSession, refreshTrigger, onExportChat }) {
    const [selectedFile, setSelectedFile] = useState(null);
    const [sessions, setSessions] = useState([]);
    const [isDragging, setIsDragging] = useState(false);

    useEffect(() => {
        const email = localStorage.getItem("userEmail");
        if (email) {
            fetchSessions(email).then(res => {
                if (res?.status === "success") {
                    setSessions(res.sessions);
                }
            });
        }
    }, [refreshTrigger]);

    const handleFileUpload = async (e) => {
        const file = e.target.files?.[0] || e.dataTransfer?.files?.[0];

        if (file) {
            setSelectedFile(file.name);
            const result = await uploadDocument(file);
            console.log(result);
            onFileUpload(file.name);
        }
    };

    const handleDragOver = (e) => {
        e.preventDefault();
        setIsDragging(true);
    };

    const handleDragLeave = (e) => {
        e.preventDefault();
        setIsDragging(false);
    };

    const handleDrop = (e) => {
        e.preventDefault();
        setIsDragging(false);
        if (e.dataTransfer.files && e.dataTransfer.files.length > 0) {
            handleFileUpload(e);
            e.dataTransfer.clearData();
        }
    };

    return (
        <div className="w-72 h-full border-r border-white/10 bg-white/5 backdrop-blur-xl p-6 overflow-y-auto">

            <h2 className="text-xl font-semibold mb-8">
                Knowledge Hub
            </h2>

            {/* Upload */}
            <div className="mb-6">
                <label 
                    onDragOver={handleDragOver}
                    onDragLeave={handleDragLeave}
                    onDrop={handleDrop}
                    className={`w-full p-8 rounded-xl border-2 border-dashed cursor-pointer block text-center transition-all duration-300 ${
                        isDragging ? "border-white bg-white/20" : "bg-white/5 border-white/10 hover:border-white"
                    }`}>
                    <div className="text-gray-300 text-sm">
                        {isDragging ? "Drop here..." : "Drag & Drop or Click to Upload"}
                    </div>

                    <input
                        type="file"
                        className="hidden"
                        onChange={handleFileUpload}
                    />
                </label>

                {selectedFile && (
                    <div className="mt-4 p-3 rounded-xl bg-black border border-white/10 text-sm text-gray-300">
                        {selectedFile}
                    </div>
                )}
            </div>

            {/* Actions */}
            <div className="space-y-4">
                <button 
                    onClick={onNewSession}
                    className="w-full p-4 rounded-xl bg-white text-black border border-white hover:shadow-[0_0_20px_rgba(255,255,255,0.3)] transition-all duration-300">
                    + New Chat
                </button>

                <button className="w-full p-4 rounded-xl bg-white/5 border border-white/10 hover:border-white transition-all duration-300">
                    Quick Prompts
                </button>

                <button onClick={onExportChat} className="w-full p-4 rounded-xl bg-white/5 border border-white/10 hover:border-white transition-all duration-300">
                    Export Chat
                </button>
            </div>

            {/* Recent Chats */}
            <div className="mt-10">
                <h3 className="text-sm text-gray-400 mb-4">
                    Recent Chats
                </h3>

                <div className="space-y-3">
                    {sessions.map(s => (
                        <div 
                            key={s.id} 
                            onClick={() => onSessionSelect(s.id)}
                            className="p-3 rounded-xl bg-black border border-white/10 text-sm cursor-pointer hover:border-white transition-all"
                        >
                            {s.title}
                        </div>
                    ))}
                    {sessions.length === 0 && (
                        <div className="text-sm text-gray-500 italic">No recent chats.</div>
                    )}
                </div>
            </div>

        </div>
    );
}

export default Sidebar;