import { useState } from "react";
import { motion } from "framer-motion";
import { useNavigate } from "react-router-dom";
import { signup } from "../services/api";

function SignupPage() {
    const navigate = useNavigate();
    const [email, setEmail] = useState("");
    const [password, setPassword] = useState("");
    const [error, setError] = useState("");

    const handleSignup = async () => {
        setError("");
        if (!email || !password) {
            setError("Please fill all fields.");
            return;
        }

        const res = await signup(email, password);
        if (res?.status === "success") {
            localStorage.setItem("userEmail", email);
            navigate("/login");
        } else {
            setError(res?.message || "Signup failed");
        }
    };

    return (
        <motion.div
            className="min-h-screen bg-black text-white flex overflow-hidden"
            initial={{ opacity: 0, y: 40 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8 }}
        >
            {/* LEFT SIDE */}
            <div className="w-1/2 flex flex-col justify-center px-20 relative">

                <div className="absolute w-[500px] h-[500px] bg-purple-500 blur-[180px] opacity-20 rounded-full"></div>

                <div className="relative flex justify-center items-center mb-12">
                    <div className="absolute w-72 h-72 rounded-full border border-purple-500 animate-[spin_15s_linear_infinite]"></div>

                    <div className="absolute w-56 h-56 rounded-full border border-cyan-500 animate-[spin_10s_linear_infinite_reverse]"></div>

                    <div className="w-32 h-32 rounded-full bg-gradient-to-r from-purple-500 to-cyan-500 blur-2xl opacity-80"></div>
                </div>

                <h1 className="text-5xl font-bold leading-tight mb-6">
                    Secure Access to Your
                    <span className="text-purple-500"> RAG Intelligence</span>
                </h1>

                <p className="text-gray-400 text-lg max-w-lg">
                    Authenticate to access enterprise knowledge retrieval,
                    OCR systems, document intelligence, and AI workflows.
                </p>

                <div className="mt-10 flex gap-4">
                    <div className="px-4 py-2 rounded-xl bg-purple-500/10 border border-purple-500/30 text-purple-400">
                        FAISS
                    </div>

                    <div className="px-4 py-2 rounded-xl bg-cyan-500/10 border border-cyan-500/30 text-cyan-400">
                        OCR
                    </div>

                    <div className="px-4 py-2 rounded-xl bg-green-500/10 border border-green-500/30 text-green-400">
                        Memory
                    </div>
                </div>
            </div>

            {/* RIGHT SIDE */}
            <div className="w-1/2 flex items-center justify-center">

                <div className="w-[450px] p-10 rounded-3xl bg-white/5 backdrop-blur-2xl border border-white/10">

                    <h2 className="text-4xl font-bold mb-3">Sign Up</h2>

                    <p className="text-gray-400 mb-8">
                        Create your company knowledgebase account
                    </p>

                    <div className="space-y-6">
                        <input
                            type="email"
                            placeholder="Enter email"
                            value={email}
                            onChange={(e) => setEmail(e.target.value)}
                            className="w-full p-4 rounded-xl bg-black/40 border border-white/10 outline-none focus:border-purple-500"
                        />

                        <input
                            type="password"
                            placeholder="Enter password"
                            value={password}
                            onChange={(e) => setPassword(e.target.value)}
                            className="w-full p-4 rounded-xl bg-black/40 border border-white/10 outline-none focus:border-purple-500"
                        />

                        {error && <div className="text-red-500 text-sm">{error}</div>}

                        <button
                            onClick={handleSignup}
                            className="w-full py-4 rounded-xl bg-purple-600 hover:shadow-[0_0_30px_rgba(168,85,247,0.5)] transition-all duration-300"
                        >
                            Sign Up
                        </button>
                    </div>

                    <div className="mt-6 text-sm text-center">
                        <span className="text-gray-400">Already have an account? </span>
                        <span 
                            onClick={() => navigate("/login")}
                            className="text-purple-400 cursor-pointer hover:underline"
                        >
                            Log in
                        </span>
                    </div>

                    <div className="mt-8 text-sm text-gray-500 text-center">
                        Enterprise Authentication System
                    </div>

                </div>
            </div>
        </motion.div>
    );
}

export default SignupPage;
