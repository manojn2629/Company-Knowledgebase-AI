import { Link } from "react-router-dom";

function Navbar() {
    return (
        <div className="w-full h-20 flex items-center justify-between px-14 fixed top-0 z-50 backdrop-blur-md bg-black/20 border-b border-white/10">
            <h1 className="text-xl font-bold text-white">
                Company Knowledgebase AI
            </h1>

            <div className="flex gap-8 text-gray-300 text-lg">
                <a
                    href="#features"
                    className="hover:text-purple-400 cursor-pointer transition-all duration-300"
                >
                    Features
                </a>

                <a
                    href="#workflow"
                    className="hover:text-purple-400 cursor-pointer transition-all duration-300"
                >
                    Workflow
                </a>

                <a
                    href="#preview"
                    className="hover:text-purple-400 cursor-pointer transition-all duration-300"
                >
                    Preview
                </a>

                <Link
                    to="/login"
                    className="hover:text-purple-400 cursor-pointer transition-all duration-300"
                >
                    Login
                </Link>
            </div>
        </div>
    );
}

export default Navbar;