import { motion } from "framer-motion";
import Navbar from "../components/landing/Navbar";
import Hero from "../components/landing/Hero";
import Features from "../components/landing/Features";
import Workflow from "../components/landing/Workflow";
import Preview from "../components/landing/Preview";

function LandingPage() {
    return (
        <motion.div
            className="bg-black text-white min-h-screen overflow-x-hidden"
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ duration: 1 }}
        >
            {/* Top Navigation */}
            <Navbar />

            {/* Hero Section */}
            <Hero />

            {/* Features Section */}
            <Features />

            {/* Workflow Section */}
            <Workflow />

            {/* Dashboard Preview Section */}
            <Preview />
        </motion.div>
    );
}

export default LandingPage;