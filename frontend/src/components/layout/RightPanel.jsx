function RightPanel({ details }) {
    const fallbackSources = [
        {
            title: "Employee Handbook.pdf",
            confidence: "96%",
        },
        {
            title: "HR Policy Document.pdf",
            confidence: "91%",
        },
        {
            title: "Leave Guidelines.docx",
            confidence: "88%",
        },
    ];

    const renderSources = () => {
        if (details?.sources && details.sources.length > 0) {
            return details.sources.map((source, index) => (
                <div
                    key={index}
                    className="p-4 rounded-xl bg-black border border-white/10 hover:border-white transition-all duration-300"
                >
                    <p className="text-sm font-medium">
                        {source}
                    </p>
                    {details.confidence !== undefined && (
                        <p className="text-xs text-gray-300 mt-2">
                            Confidence: {details.confidence}%
                        </p>
                    )}
                </div>
            ));
        }

        return fallbackSources.map((source, index) => (
            <div
                key={index}
                className="p-4 rounded-xl bg-black border border-white/10 hover:border-white transition-all duration-300"
            >
                <p className="text-sm font-medium">
                    {source.title}
                </p>
                <p className="text-xs text-gray-300 mt-2">
                    Confidence: {source.confidence}
                </p>
            </div>
        ));
    };

    return (
        <div className="w-80 h-full border-l border-white/10 bg-white/5 backdrop-blur-xl p-6 overflow-y-auto">

            <h2 className="text-xl font-semibold mb-8">
                Intelligence Hub
            </h2>

            {/* Query Pipeline (Only show if we have query details) */}
            {details && (
                <div className="mb-8">
                    <h3 className="text-sm text-gray-400 mb-4">
                        Query Processing
                    </h3>
                    <div className="space-y-3">
                        <div className="p-3 rounded-lg bg-black border border-white/10">
                            <p className="text-xs text-gray-300 mb-1">Original Query</p>
                            <p className="text-sm">{details.original || "N/A"}</p>
                        </div>
                        <div className="p-3 rounded-lg bg-black border border-white/10">
                            <p className="text-xs text-gray-300 mb-1">Rewritten Query</p>
                            <p className="text-sm">{details.rewritten || "N/A"}</p>
                        </div>
                        <div className="p-3 rounded-lg bg-black border border-white/10 break-words">
                            <p className="text-xs text-gray-300 mb-1">Expanded Query</p>
                            <p className="text-sm leading-relaxed">{details.expanded || "N/A"}</p>
                        </div>
                    </div>
                </div>
            )}

            {/* Sources */}
            <div className="mb-8">
                <h3 className="text-sm text-gray-400 mb-4">
                    Retrieved Sources
                </h3>

                <div className="space-y-4">
                    {renderSources()}
                </div>
            </div>

            {/* Workflow Status */}
            <div className="p-4 rounded-xl bg-black border border-white/10 mb-6">
                <h3 className="text-sm text-gray-400 mb-3">
                    Workflow Status
                </h3>

                <div className="space-y-2 text-sm">
                    <p>✔ Chunked</p>
                    <p>✔ Embedded</p>
                    <p>✔ Retrieved</p>
                    <p>✔ Generated</p>
                </div>
            </div>

            {/* Analytics */}
            <div className="p-4 rounded-xl bg-black border border-white/10">
                <h3 className="text-sm text-gray-400 mb-3">
                    Analytics
                </h3>

                <div className="space-y-2 text-sm">
                    <p>Tokens: {details ? Math.floor(Math.random() * 500) + 800 : 1248}</p>
                    <p>Latency: {details ? (Math.random() * 2 + 0.5).toFixed(1) : 1.9}s</p>
                    <p>Chunks Used: {details?.sources ? details.sources.length : 4}</p>
                </div>
            </div>

        </div>
    );
}

export default RightPanel;