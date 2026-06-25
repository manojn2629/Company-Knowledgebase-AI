function DashboardNavbar() {
    return (
        <div className="w-full h-20 px-8 flex items-center justify-between border-b border-white/10 backdrop-blur-md bg-black/20">
            <h1 className="text-xl font-bold text-white">
                Company Knowledgebase AI
            </h1>

            <div className="flex gap-4">
                <div className="px-4 py-2 rounded-xl bg-purple-500/10 border border-purple-500/30 text-purple-400 text-sm">
                    AI Active
                </div>
            </div>
        </div>
    );
}

export default DashboardNavbar;