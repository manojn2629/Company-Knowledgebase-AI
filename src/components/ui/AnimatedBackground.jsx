function AnimatedBackground() {
    return (
        <div className="fixed inset-0 -z-10 overflow-hidden bg-black">

            {/* Purple Glow */}
            <div className="absolute top-20 left-20 w-96 h-96 bg-purple-600 rounded-full blur-[150px] opacity-20 animate-pulse"></div>

            {/* Cyan Glow */}
            <div className="absolute bottom-20 right-20 w-96 h-96 bg-cyan-500 rounded-full blur-[150px] opacity-20 animate-pulse"></div>

            {/* Center Glow */}
            <div className="absolute top-1/3 left-1/2 w-80 h-80 bg-fuchsia-500 rounded-full blur-[120px] opacity-10 animate-ping"></div>

            {/* Grid Overlay */}
            <div className="absolute inset-0 bg-[linear-gradient(rgba(255,255,255,0.03)_1px,transparent_1px),linear-gradient(90deg,rgba(255,255,255,0.03)_1px,transparent_1px)] bg-[size:40px_40px]"></div>

        </div>
    );
}

export default AnimatedBackground;