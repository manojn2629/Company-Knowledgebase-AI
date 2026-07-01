import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';

function ChatWindow({ messages, thinking }) {
    return (
        <div className="flex-1 h-full p-8 pb-32 overflow-y-auto">
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
                                    ? "bg-white text-black"
                                    : "bg-white/5 border border-white/10 text-gray-200"
                                }`}
                        >
                            {msg.sender === "user" ? (
                                <p className="whitespace-pre-wrap">{msg.text}</p>
                            ) : (
                                <ReactMarkdown
                                    remarkPlugins={[remarkGfm]}
                                    components={{
                                        ul: ({ node, ...props }) => <ul className="list-disc ml-5 space-y-1 my-2" {...props} />,
                                        ol: ({ node, ...props }) => <ol className="list-decimal ml-5 space-y-1 my-2" {...props} />,
                                        li: ({ node, ...props }) => <li className="pl-1" {...props} />,
                                        p: ({ node, ...props }) => <p className="mb-2 last:mb-0" {...props} />,
                                        a: ({ node, ...props }) => <a className="text-blue-400 hover:underline" {...props} />,
                                        h1: ({ node, ...props }) => <h1 className="text-lg font-bold my-2" {...props} />,
                                        h2: ({ node, ...props }) => <h2 className="text-md font-bold my-2" {...props} />,
                                        h3: ({ node, ...props }) => <h3 className="text-sm font-bold my-2" {...props} />
                                    }}
                                >
                                    {msg.text}
                                </ReactMarkdown>
                            )}
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
                                <div className="w-2 h-2 rounded-full bg-white animate-bounce"></div>
                                <div className="w-2 h-2 rounded-full bg-white animate-bounce delay-150"></div>
                                <div className="w-2 h-2 rounded-full bg-white animate-bounce delay-300"></div>
                            </div>

                        </div>
                    </div>
                )}

            </div>
        </div>
    );
}

export default ChatWindow;