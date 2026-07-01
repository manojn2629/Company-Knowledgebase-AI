import { useState, useEffect } from "react";
import { motion } from "framer-motion";
import { useNavigate } from "react-router-dom";
import DashboardNavbar from "../components/layout/DashboardNavbar";
import AnimatedBackground from "../components/ui/AnimatedBackground";

function AdminDashboard() {
    const [metrics, setMetrics] = useState({ total_users: 0, total_sessions: 0, total_messages: 0 });
    const [loading, setLoading] = useState(true);
    const navigate = useNavigate();

    useEffect(() => {
        const fetchMetrics = async () => {
            try {
                const response = await fetch("http://127.0.0.1:8000/metrics");
                const data = await response.json();
                if (data.status === "success") {
                    setMetrics(data.metrics);
                }
            } catch (err) {
                console.error("Failed to fetch metrics", err);
            }
            setLoading(false);
        };
        fetchMetrics();
    }, []);

    return (
        <motion.div
            className="min-h-screen bg-black text-white relative flex flex-col"
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ duration: 0.8 }}
        >
            <AnimatedBackground />
            <DashboardNavbar />
            
            <div className="flex-1 p-10 max-w-6xl mx-auto w-full">
                <div className="flex items-center justify-between mb-8">
                    <h1 className="text-4xl font-bold">System Analytics</h1>
                    <button 
                        onClick={() => navigate("/dashboard")}
                        className="px-6 py-3 rounded-xl bg-white text-black hover:bg-gray-200 transition-all font-medium"
                    >
                        Back to Chat
                    </button>
                </div>
                
                {loading ? (
                    <div className="text-center text-gray-400 mt-20">Loading metrics...</div>
                ) : (
                    <div className="grid grid-cols-3 gap-8">
                        <div className="p-8 rounded-2xl bg-white/5 border border-white/10 flex flex-col items-center justify-center shadow-lg">
                            <span className="text-gray-400 text-lg mb-2">Total Users</span>
                            <span className="text-6xl font-bold">{metrics.total_users}</span>
                        </div>
                        <div className="p-8 rounded-2xl bg-white/5 border border-white/10 flex flex-col items-center justify-center shadow-lg">
                            <span className="text-gray-400 text-lg mb-2">Total Sessions</span>
                            <span className="text-6xl font-bold">{metrics.total_sessions}</span>
                        </div>
                        <div className="p-8 rounded-2xl bg-white/5 border border-white/10 flex flex-col items-center justify-center shadow-lg">
                            <span className="text-gray-400 text-lg mb-2">Total Messages</span>
                            <span className="text-6xl font-bold">{metrics.total_messages}</span>
                        </div>
                    </div>
                )}
            </div>
        </motion.div>
    );
}

export default AdminDashboard;
