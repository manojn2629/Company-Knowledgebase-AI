import { useNavigate } from "react-router-dom";

function Hero() {
    const navigate = useNavigate();

    return (
        <div className="h-[90vh] flex items-center justify-center px-20">

            {/* Left Section */}
            <div className="w-1/2 space-y-8">

                <h1 className="text-6xl font-bold leading-tight">
                    <span className="text-white">RAG</span>{" "}
                    <span className="text-white">Intelligence</span>{" "}
                    <span className="text-gray-300">System</span>
                </h1>

                <p className="text-gray-400 text-xl leading-relaxed max-w-xl">
                    Search company policies, internal documents, workflows, and
                    enterprise knowledge instantly with Retrieval-Augmented Generation.
                </p>

                {/* Only Get Started */}
                <div>
                    <button
                        onClick={() => navigate("/login")}
                        className="px-8 py-4 bg-white text-black rounded-xl hover:shadow-[0_0_30px_rgba(255,255,255,0.3)] transition-all duration-300 text-lg font-medium"
                    >
                        Get Started
                    </button>
                </div>
            </div>

            {/* Right Section */}
            <div className="w-1/2 flex justify-center">
                <div className="relative flex items-center justify-center">

                    {/* Outer Ring */}
                    <div className="absolute w-80 h-80 rounded-full border border-white animate-[spin_12s_linear_infinite]"></div>

                    {/* Inner Ring */}
                    <div className="absolute w-64 h-64 rounded-full border border-gray-400 animate-[spin_8s_linear_infinite_reverse]"></div>

                    {/* Core */}
                    <div className="w-40 h-40 rounded-full bg-gradient-to-r from-white to-gray-500 blur-2xl opacity-80"></div>

                </div>
            </div>

        </div>
    );
}

export default Hero;