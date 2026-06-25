function Workflow() {
    const steps = [
        "Upload",
        "OCR",
        "Parse",
        "Chunk",
        "Embed",
        "Store",
        "Retrieve",
        "Reason",
        "Memory",
        "Generate",
    ];

    return (
        <div id="workflow" className="pt-32 pb-24 px-20 scroll-mt-24">
            <h2 className="text-4xl font-bold mb-16">AI Workflow Engine</h2>

            <div className="relative overflow-x-auto pb-6">

                <div className="flex items-center gap-10 min-w-max">

                    {steps.map((step, index) => (
                        <div key={index} className="flex items-center gap-10">

                            {/* Step Card */}
                            <div className="relative group">

                                <div className="absolute inset-0 bg-purple-500 blur-xl opacity-20 group-hover:opacity-40 transition-all duration-500 rounded-3xl"></div>

                                <div className="relative w-44 h-32 rounded-3xl border border-white/10 bg-white/5 backdrop-blur-xl flex flex-col items-center justify-center hover:border-purple-500 transition-all duration-500 hover:scale-105">

                                    <div className="text-sm text-purple-400 mb-2">
                                        STEP {index + 1}
                                    </div>

                                    <h3 className="text-xl font-semibold">
                                        {step}
                                    </h3>

                                </div>
                            </div>

                            {/* Connector */}
                            {index !== steps.length - 1 && (
                                <div className="w-20 h-[3px] bg-gradient-to-r from-purple-500 to-cyan-500 rounded-full"></div>
                            )}
                        </div>
                    ))}

                </div>

            </div>

            {/* Workflow Description */}
            <div className="mt-14 p-8 rounded-3xl bg-white/5 border border-white/10 backdrop-blur-xl">
                <h3 className="text-2xl font-semibold mb-4 text-purple-400">
                    How It Works
                </h3>

                <p className="text-gray-400 leading-relaxed text-lg">
                    The RAG Intelligence System begins by accepting enterprise documents
                    such as PDFs, scanned files, images, reports, Excel sheets, and policies
                    through the upload layer. Once uploaded, the OCR engine extracts raw text
                    from scanned or image-based documents, while the parsing engine processes
                    structured data like tables, CSVs, and spreadsheets.

                    After extraction, the chunking engine divides large documents into smaller
                    meaningful sections so the AI can process them efficiently. These chunks
                    are then passed into an embedding model, which converts textual content
                    into high-dimensional vectors representing semantic meaning.

                    The generated embeddings are stored inside the FAISS vector database,
                    enabling fast similarity-based retrieval. When a user asks a question,
                    the retriever searches FAISS to find the most relevant document chunks
                    related to that query.

                    These retrieved chunks are passed into the LLM reasoning engine, where
                    the language model analyzes the context, understands the intent, and
                    formulates accurate responses. Alongside this, the chat memory layer
                    maintains previous conversation history, preserving context for multi-turn
                    interactions and improving continuity.

                    If internal company knowledge is insufficient, the internet fallback
                    module activates to fetch external knowledge. Finally, the response
                    generator combines all retrieved context, reasoning outputs, and memory
                    into a final source-backed answer. The analytics layer then tracks
                    confidence scores, source references, retrieval quality, token usage,
                    and response latency for transparency and performance monitoring.
                </p>
            </div>
        </div>
    );
}

export default Workflow;