import { useState } from "react";
import { motion } from "framer-motion";
import { useNavigate } from "react-router-dom";
import { login } from "../services/api";

function LoginPage() {
    const navigate = useNavigate();
    const [email, setEmail] = useState("");
    const [password, setPassword] = useState("");
    const [error, setError] = useState("");

    const handleLogin = async () => {
        setError("");
        if (!email || !password) {
            setError("Please fill all fields.");
            return;
        }

        const res = await login(email, password);
        if (res?.status === "success") {
            localStorage.setItem("userEmail", email);
            localStorage.setItem("userRole", res.role);
            navigate("/dashboard");
        } else {
            setError(res?.message || "Login failed");
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

                <div className="absolute w-[500px] h-[500px] bg-white blur-[180px] opacity-10 rounded-full"></div>

                <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 flex justify-center items-center pointer-events-none -z-10">
                    <div className="absolute w-[400px] h-[400px] rounded-full border border-white/30 animate-[spin_15s_linear_infinite]"></div>

                    <div className="absolute w-[300px] h-[300px] rounded-full border border-gray-500/30 animate-[spin_10s_linear_infinite_reverse]"></div>

                    <div className="w-48 h-48 rounded-full bg-white blur-[100px] opacity-30"></div>
                </div>

                <h1 className="text-5xl font-bold leading-tight mb-6">
                    Secure Access to Your
                    <span className="text-white"> RAG Intelligence</span>
                </h1>

                <p className="text-gray-400 text-lg max-w-lg">
                    Authenticate to access enterprise knowledge retrieval,
                    OCR systems, document intelligence, and AI workflows.
                </p>

                <div className="mt-10 flex gap-4">
                    <div className="px-4 py-2 rounded-xl bg-white/10 border border-white/30 text-gray-300">
                        FAISS
                    </div>

                    <div className="px-4 py-2 rounded-xl bg-gray-400/10 border border-gray-400/30 text-gray-300">
                        OCR
                    </div>

                    <div className="px-4 py-2 rounded-xl bg-white/10 border border-white/30 text-gray-300">
                        Memory
                    </div>
                </div>
            </div>

            {/* RIGHT SIDE */}
            <div className="w-1/2 flex items-center justify-center">

                <div className="w-[450px] p-10 rounded-3xl bg-white/5 backdrop-blur-2xl border border-white/10">

                    <h2 className="text-4xl font-bold mb-3">Login</h2>

                    <p className="text-gray-400 mb-8">
                        Access your company knowledgebase
                    </p>

                    <div className="space-y-6">
                        <input
                            type="email"
                            placeholder="Enter email"
                            value={email}
                            onChange={(e) => setEmail(e.target.value)}
                            className="w-full p-4 rounded-xl bg-black/40 border border-white/10 outline-none focus:border-white"
                        />

                        <input
                            type="password"
                            placeholder="Enter password"
                            value={password}
                            onChange={(e) => setPassword(e.target.value)}
                            className="w-full p-4 rounded-xl bg-black/40 border border-white/10 outline-none focus:border-white"
                        />

                        {error && <div className="text-white text-sm">{error}</div>}

                        <button
                            onClick={handleLogin}
                            className="w-full py-4 rounded-xl bg-white text-black hover:shadow-[0_0_30px_rgba(255,255,255,0.3)] transition-all duration-300"
                        >
                            Sign In
                        </button>
                    </div>

                    <div className="mt-6 text-sm text-center">
                        <span className="text-gray-400">Don't have an account? </span>
                        <span 
                            onClick={() => navigate("/signup")}
                            className="text-gray-300 cursor-pointer hover:underline"
                        >
                            Sign up
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

export default LoginPage;