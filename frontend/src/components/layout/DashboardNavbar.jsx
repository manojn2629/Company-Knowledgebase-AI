import { useNavigate } from "react-router-dom";

function DashboardNavbar() {
    const role = localStorage.getItem("userRole");
    const navigate = useNavigate();
    return (
        <div className="w-full h-20 px-8 flex items-center justify-between border-b border-white/10 backdrop-blur-md bg-black/20">
            <h1 className="text-xl font-bold text-white">
                Company Knowledgebase AI
            </h1>

            <div className="flex gap-4">
                {role === "admin" && (
                    <button 
                        onClick={() => navigate("/admin")}
                        className="px-4 py-2 rounded-xl bg-white text-black hover:bg-gray-200 transition-all font-medium text-sm">
                        Admin Dashboard
                    </button>
                )}
                <div className="px-4 py-2 rounded-xl bg-white/10 border border-white/30 text-gray-300 text-sm">
                    AI Active
                </div>
            </div>
        </div>
    );
}

export default DashboardNavbar;