function Preview() {
    return (
        <div id="preview" className="pt-32 pb-24 px-20 scroll-mt-24">
            <h2 className="text-4xl font-bold mb-14">Dashboard Preview</h2>

            <div className="w-full h-[650px] rounded-[40px] border border-white/10 bg-white/5 backdrop-blur-xl p-8 flex gap-8">

                {/* LEFT PANEL */}
                <div className="w-[22%] h-full rounded-3xl bg-black/40 border border-white/10 p-6 flex flex-col">

                    <button className="w-full py-4 rounded-2xl bg-white text-black hover:shadow-[0_0_20px_rgba(255,255,255,0.3)] transition-all duration-300">
                        Upload Files
                    </button>

                    <div className="mt-8">
                        <h3 className="text-lg font-semibold mb-4 text-gray-300">
                            Knowledge Base
                        </h3>

                        <div className="space-y-3">
                            <div className="p-3 rounded-xl bg-white/5 border border-white/10">
                                Employee Handbook.pdf
                            </div>

                            <div className="p-3 rounded-xl bg-white/5 border border-white/10">
                                HR Policy.pdf
                            </div>

                            <div className="p-3 rounded-xl bg-white/5 border border-white/10">
                                Leave Rules.pdf
                            </div>
                        </div>
                    </div>

                    <div className="mt-10">
                        <h3 className="text-lg font-semibold mb-4 text-gray-300">
                            Recent Chats
                        </h3>

                        <div className="space-y-3">
                            <div className="p-3 rounded-xl bg-white/5 border border-white/10">
                                Leave policy
                            </div>

                            <div className="p-3 rounded-xl bg-white/5 border border-white/10">
                                Expense rules
                            </div>

                            <div className="p-3 rounded-xl bg-white/5 border border-white/10">
                                Attendance
                            </div>
                        </div>
                    </div>
                </div>

                {/* CENTER CHAT PANEL */}
                <div className="w-[50%] h-full rounded-3xl bg-black/40 border border-white/10 p-6 flex flex-col justify-between">

                    <div className="space-y-6">

                        {/* User */}
                        <div className="flex justify-end">
                            <div className="px-5 py-4 rounded-2xl bg-white text-black max-w-md">
                                What is the leave policy?
                            </div>
                        </div>

                        {/* AI */}
                        <div className="flex justify-start">
                            <div className="px-5 py-4 rounded-2xl bg-white/5 border border-white/10 max-w-md">
                                Based on the Employee Handbook, employees are entitled to 12 annual paid leaves and sick leave benefits.
                            </div>
                        </div>

                        {/* Sources */}
                        <div className="space-y-3 mt-6">
                            <h4 className="text-sm text-gray-400">Retrieved Sources</h4>

                            <div className="p-3 rounded-xl bg-white/10 border border-white/30">
                                Employee Handbook.pdf
                            </div>

                            <div className="p-3 rounded-xl bg-gray-400/10 border border-gray-400/30">
                                HR Policy.pdf
                            </div>
                        </div>

                    </div>

                    {/* Input */}
                    <div className="w-full p-4 rounded-2xl bg-white/5 border border-white/10 flex justify-between items-center">
                        <span className="text-gray-400">
                            Ask your company AI...
                        </span>

                        <button className="px-6 py-2 rounded-xl bg-white text-black">
                            Send
                        </button>
                    </div>

                </div>

                {/* RIGHT PANEL */}
                <div className="w-[28%] h-full rounded-3xl bg-black/40 border border-white/10 p-6">

                    <h3 className="text-xl font-semibold mb-6">
                        Intelligence Layer
                    </h3>

                    <div className="space-y-5">

                        <div className="p-4 rounded-2xl bg-white/5 border border-white/10">
                            Confidence Score
                            <div className="mt-3 h-2 rounded-full bg-white text-black w-[96%]"></div>
                            <p className="mt-2 text-sm text-gray-400">96%</p>
                        </div>

                        <div className="p-4 rounded-2xl bg-white/5 border border-white/10">
                            Retrieval Latency
                            <div className="mt-3 h-2 rounded-full bg-gray-400 w-[70%]"></div>
                            <p className="mt-2 text-sm text-gray-400">1.2 sec</p>
                        </div>

                        <div className="p-4 rounded-2xl bg-white/5 border border-white/10">
                            Token Usage
                            <p className="mt-2 text-gray-300">842 tokens</p>
                        </div>

                        <div className="p-4 rounded-2xl bg-white/5 border border-white/10">
                            Active Systems
                            <div className="mt-3 space-y-2 text-sm text-gray-300">
                                <p>✓ FAISS Vector DB</p>
                                <p>✓ OCR Engine</p>
                                <p>✓ Groq LLM</p>
                                <p>✓ Chat Memory</p>
                            </div>
                        </div>

                    </div>
                </div>

            </div>
        </div>
    );
}

export default Preview;