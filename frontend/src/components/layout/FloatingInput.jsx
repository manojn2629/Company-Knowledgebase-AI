import { useState, useRef } from "react";
import { Paperclip, Mic, Square } from "lucide-react";
import { transcribeAudio } from "../../services/api";

function FloatingInput({ onSend }) {
    const [input, setInput] = useState("");
    const [uploading, setUploading] = useState(false);
    const [isRecording, setIsRecording] = useState(false);
    const mediaRecorder = useRef(null);
    const audioChunks = useRef([]);

    const handleSend = () => {
        if (!input.trim()) return;

        onSend(input);
        setInput("");
    };

    const startRecording = async () => {
        try {
            const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
            mediaRecorder.current = new MediaRecorder(stream);
            
            mediaRecorder.current.ondataavailable = (event) => {
                if (event.data.size > 0) {
                    audioChunks.current.push(event.data);
                }
            };

            mediaRecorder.current.onstop = async () => {
                const audioBlob = new Blob(audioChunks.current, { type: "audio/webm" });
                audioChunks.current = [];
                setUploading(true);
                
                const res = await transcribeAudio(audioBlob);
                if (res.text) {
                    setInput(prev => prev + (prev ? " " : "") + res.text);
                } else {
                    alert("Transcription failed.");
                }
                setUploading(false);
                
                stream.getTracks().forEach(track => track.stop());
            };

            mediaRecorder.current.start();
            setIsRecording(true);
        } catch (err) {
            console.error("Error accessing microphone:", err);
            alert("Please allow microphone access to use voice input.");
        }
    };

    const stopRecording = () => {
        if (mediaRecorder.current && isRecording) {
            mediaRecorder.current.stop();
            setIsRecording(false);
        }
    };

    const handleFileUpload = async (e) => {
        const file = e.target.files[0];
        if (!file) return;

        const formData = new FormData();
        formData.append("file", file);

        setUploading(true);

        const isImage = file.type.startsWith("image/");
        const endpoint = isImage ? "http://127.0.0.1:8000/vision" : "http://127.0.0.1:8000/upload";

        try {
            const response = await fetch(endpoint, {
                method: "POST",
                body: formData,
            });

            const data = await response.json();
            
            if (isImage && data.status === "success") {
                setInput(prev => prev + (prev ? " " : "") + `[Image Analysis: ${data.text}] `);
            } else {
                alert(data.message || (isImage ? "Vision analysis failed" : "Upload successful"));
            }
        } catch (error) {
            console.error(error);
            alert("Upload failed");
        }

        setUploading(false);
    };

    return (
        <div className="fixed bottom-6 left-1/2 -translate-x-1/2 z-50 w-[750px] p-3 rounded-2xl bg-white/5 backdrop-blur-2xl border border-white/10 flex items-center gap-4 shadow-[0_0_40px_rgba(255,255,255,0.3)]">

            {/* Upload Button */}
            <label className="cursor-pointer flex items-center justify-center w-12 h-12 rounded-xl bg-white/10 hover:bg-white/20 transition-all duration-300">
                <input
                    type="file"
                    className="hidden"
                    accept=".pdf,.png,.jpg,.jpeg,.csv,.xlsx"
                    onChange={handleFileUpload}
                />
                <Paperclip className="w-5 h-5 text-gray-300" />
            </label>

            {/* Mic Button */}
            <button
                onClick={isRecording ? stopRecording : startRecording}
                className={`flex items-center justify-center w-12 h-12 rounded-xl transition-all duration-300 ${
                    isRecording 
                        ? "bg-white/20 border border-white/50 animate-pulse text-red-400" 
                        : "bg-white/10 hover:bg-white/20 text-gray-300"
                }`}
            >
                {isRecording ? <Square className="w-5 h-5" /> : <Mic className="w-5 h-5" />}
            </button>

            {/* Input */}
            <input
                type="text"
                placeholder="Ask about company policies, documents, workflows..."
                value={input}
                onChange={(e) => setInput(e.target.value)}
                onKeyDown={(e) => {
                    if (e.key === "Enter") {
                        handleSend();
                    }
                }}
                className="flex-1 bg-transparent px-4 outline-none text-white placeholder:text-gray-500"
                disabled={isRecording}
            />

            {/* Send Button */}
            <button
                onClick={handleSend}
                className="px-6 py-3 rounded-xl bg-white text-black hover:bg-purple-700 hover:shadow-[0_0_20px_rgba(255,255,255,0.3)] transition-all duration-300"
            >
                Send
            </button>

            {/* Upload Status */}
            {uploading && (
                <span className="text-xs text-gray-300 animate-pulse">
                    Uploading...
                </span>
            )}
        </div>
    );
}

export default FloatingInput;