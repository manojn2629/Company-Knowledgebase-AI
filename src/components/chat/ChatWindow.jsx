function ChatWindow({ messages, thinking }) {
    return (
        <div className="flex-1 h-full p-8 overflow-y-auto">
            <div className="space-y-6">

                {/* Chat Messages */}
                {messages.map((msg, index) => (
                    <div
                        key={index}
                        className={`flex ${msg.sender === "user"
                                ? "justify-end"
                                : "justify-start"
                            }`}
                    >
                        <div
                            className={`max-w-xl p-4 rounded-2xl ${msg.sender === "user"
                                    ? "bg-purple-600 text-white"
                                    : "bg-white/5 border border-white/10 text-gray-200"
                                }`}
                        >
                            {msg.text}
                        </div>
                    </div>
                ))}

                {/* AI Thinking Animation */}
                {thinking && (
                    <div className="flex justify-start">
                        <div className="max-w-xl p-4 rounded-2xl bg-white/5 border border-white/10">

                            {/* Status Text */}
                            <p className="text-sm text-gray-400 mb-3">
                                Retrieving company knowledge...
                            </p>

                            {/* Animated Dots */}
                            <div className="flex gap-2">
                                <div className="w-2 h-2 rounded-full bg-purple-500 animate-bounce"></div>
                                <div className="w-2 h-2 rounded-full bg-purple-500 animate-bounce delay-150"></div>
                                <div className="w-2 h-2 rounded-full bg-purple-500 animate-bounce delay-300"></div>
                            </div>

                        </div>
                    </div>
                )}

            </div>
        </div>
    );
}

export default ChatWindow;