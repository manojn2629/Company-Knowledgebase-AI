import { useState } from "react";

function FeatureCard({ title, description, steps, icon }) {
    const [open, setOpen] = useState(false);

    return (
        <div
            onClick={() => setOpen(!open)}
            className="p-8 rounded-3xl bg-white/5 border border-white/10 cursor-pointer hover:border-white transition-all duration-300"
        >
            <div className="text-gray-300 text-4xl mb-6">
                {icon}
            </div>

            <h3 className="text-2xl font-bold mb-4">
                {title}
            </h3>

            <p className="text-gray-400 mb-4">
                {description}
            </p>

            {open && (
                <div className="mt-6 border-t border-white/10 pt-4 space-y-3 animate-fadeIn">
                    {steps.map((step, index) => (
                        <div
                            key={index}
                            className="text-sm text-gray-300"
                        >
                            {index + 1}. {step}
                        </div>
                    ))}
                </div>
            )}
        </div>
    );
}

export default FeatureCard;