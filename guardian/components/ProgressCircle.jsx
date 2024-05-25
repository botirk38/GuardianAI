import React from "react";

const ProgressCircle = ({ percentage }) => {
    const radius = 70;
    const circumference = 2 * Math.PI * radius;
    const strokeDashoffset = ((100 - percentage) * circumference) / 100;

    const getColour = (percentage) => {
        if (percentage >= 80) return "green";
        if (percentage > 65 && percentage < 80) return "yellow";
        return "red";
    };

    return (
        <div className="relative">
            <svg
                width="300"
                height="300"
                viewBox="0 0 200 200"
                className=""
            >
                <circle // Base circle
                    r={radius}
                    cx="100"
                    cy="100"
                    fill=""
                    stroke={getColour(percentage) !== "red" ? "red" : "grey"}
                    strokeWidth="20"
                />
                <circle // Progress circle
                    r={radius}
                    cx="100"
                    cy="100"
                    fill="transparent"
                    stroke={
                        percentage > 0 ? getColour(percentage) : "transparent"
                    }
                    strokeWidth="20"
                    strokeDasharray={percentage < 100 ? circumference : 0}
                    strokeDashoffset={strokeDashoffset}
                    className="transition-all duration-300 ease-linear" // Add Tailwind CSS classes
                />
            </svg>

            <label className="text-white absolute top-32 left-28 text-center">
                {percentage}%<br />
                <span className="text-sm text-blue-500 font-bold">Invulnerable</span>
            </label>
        </div>
    );
};

export default ProgressCircle;
