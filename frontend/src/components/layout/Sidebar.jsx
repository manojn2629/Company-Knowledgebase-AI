import { useState, useEffect } from "react";
import { uploadDocument, fetchSessions } from "../../services/api";
function Sidebar({ onFileUpload, onSessionSelect, onNewSession, refreshTrigger }) {
    const [selectedFile, setSelectedFile] = useState(null);
    const [sessions, setSessions] = useState([]);

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
        const file = e.target.files[0];

        if (file) {
            setSelectedFile(file.name);

            const result = await uploadDocument(file);

            console.log(result);

            onFileUpload(file.name);
        }
    };

    return (
        <div className="w-72 h-full border-r border-white/10 bg-white/5 backdrop-blur-xl p-6 overflow-y-auto">

            <h2 className="text-xl font-semibold mb-8">
                Knowledge Hub
            </h2>

            {/* Upload */}
            <div className="mb-6">
                <label className="w-full p-4 rounded-xl bg-white/5 border border-white/10 cursor-pointer block text-center hover:border-purple-500 transition-all duration-300">
                    Upload Files

                    <input
                        type="file"
                        className="hidden"
                        onChange={handleFileUpload}
                    />
                </label>

                {selectedFile && (
                    <div className="mt-4 p-3 rounded-xl bg-black border border-white/10 text-sm text-purple-400">
                        {selectedFile}
                    </div>
                )}
            </div>

            {/* Actions */}
            <div className="space-y-4">
                <button 
                    onClick={onNewSession}
                    className="w-full p-4 rounded-xl bg-purple-600 border border-purple-500 hover:shadow-[0_0_20px_rgba(168,85,247,0.4)] transition-all duration-300">
                    + New Chat
                </button>

                <button className="w-full p-4 rounded-xl bg-white/5 border border-white/10 hover:border-purple-500 transition-all duration-300">
                    Quick Prompts
                </button>

                <button className="w-full p-4 rounded-xl bg-white/5 border border-white/10 hover:border-purple-500 transition-all duration-300">
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
                            className="p-3 rounded-xl bg-black border border-white/10 text-sm cursor-pointer hover:border-purple-500 transition-all"
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