import { useState } from "react";
import {
    Database,
    FileSearch,
    ScanSearch,
    Table2,
    Brain,
    Globe,
} from "lucide-react";

function Features() {
    const [openCard, setOpenCard] = useState(null);

    const features = [
        {
            title: "RAG Search",
            icon: <Database size={32} />,
            desc: "Search internal company knowledge instantly with retrieval AI.",
            steps: [
                "Upload documents",
                "Chunk documents",
                "Generate embeddings",
                "Store in vector DB",
                "Retrieve relevant chunks",
                "Generate final answer",
            ],
        },
        {
            title: "OCR Extraction",
            icon: <ScanSearch size={32} />,
            desc: "Extract text from scanned images and documents.",
            steps: [
                "Upload image",
                "Detect text",
                "Extract with OCR",
                "Clean text",
                "Store structured content",
            ],
        },
        {
            title: "Document Analysis",
            icon: <FileSearch size={32} />,
            desc: "Analyze policies, reports, and PDFs.",
            steps: [
                "Read document",
                "Parse content",
                "Summarize sections",
                "Extract metadata",
                "Generate insights",
            ],
        },
        {
            title: "Table Parsing",
            icon: <Table2 size={32} />,
            desc: "Extract tables from files.",
            steps: [
                "Detect table",
                "Read rows",
                "Read columns",
                "Normalize data",
                "Store structured table",
            ],
        },
        {
            title: "Chat Memory",
            icon: <Brain size={32} />,
            desc: "Remember previous conversations.",
            steps: [
                "Store chat history",
                "Track context",
                "Recall old messages",
                "Use for future answers",
            ],
        },
        {
            title: "Internet Fallback",
            icon: <Globe size={32} />,
            desc: "Use web search if internal data fails.",
            steps: [
                "Search internal docs",
                "No result found",
                "Trigger web search",
                "Fetch latest data",
                "Generate answer",
            ],
        },
    ];

    const handleCardClick = (index) => {
        if (openCard === index) {
            setOpenCard(null);
        } else {
            setOpenCard(index);
        }
    };

    return (
        <div id="features" className="pt-32 pb-24 px-20 scroll-mt-24">
            <h2 className="text-4xl font-bold mb-14">Core Features</h2>

            <div className="grid grid-cols-3 gap-8">
                {features.map((feature, index) => (
                    <div
                        key={index}
                        onClick={() => handleCardClick(index)}
                        className="p-8 bg-white/5 border border-white/10 rounded-3xl cursor-pointer hover:border-white transition-all duration-300"
                    >
                        <div className="text-gray-300 mb-6">
                            {feature.icon}
                        </div>

                        <h3 className="text-2xl font-semibold mb-4">
                            {feature.title}
                        </h3>

                        <p className="text-gray-400 mb-4">
                            {feature.desc}
                        </p>

                        {openCard === index && (
                            <div className="mt-4 border-t border-white/10 pt-4">
                                <h4 className="text-gray-300 mb-3 font-semibold">
                                    Working Flow:
                                </h4>

                                <div className="space-y-2">
                                    {feature.steps.map((step, i) => (
                                        <p key={i} className="text-sm text-gray-300">
                                            {i + 1}. {step}
                                        </p>
                                    ))}
                                </div>
                            </div>
                        )}
                    </div>
                ))}
            </div>
        </div>
    );
}

export default Features;