<<<<<<< HEAD

export default function Home() {
  return (
    <main className="flex min-h-screen flex-col items-center justify-between p-24">


    </main>
  );
=======
"use client";

import Head from "next/head";
import Link from "next/link";
import { useCallback, useState, useEffect } from "react";
import CodeMirror from "@uiw/react-codemirror";
import { rust } from "@codemirror/lang-rust";
import { vscodeDark } from "@uiw/codemirror-theme-vscode";
import ProgressCircle from "../components/ProgressCircle";

export default function Home() {
    const [showCodeVulnerability, setShowCodeVulnerability] = useState(false);
    const [tryCount, setTryCount] = useState(0);

    const placeholder = `fn main() {
    println!("Hello, world!");
}
`;
    const [percentage, setPercentage] = useState(
        0
    );

    const [formState, setFormState] = useState({
        repo_name: "test",
        path: "test",
        code: placeholder,
        license: "MIT",
        size: placeholder.length,
        language: "rust",
    });

    const onVulnerabilityClick = () => {
        setShowCodeVulnerability(!showCodeVulnerability);

        if(tryCount == 1){
            setVulnerabilities(["Unsafe block", "Overflow", "Integer division by zero"]);


        }

        else if(tryCount == 2){
            setVulnerabilities(["Unsafe block"]);

        }
        
        else {
            setVulnerabilities(["None"]);

        }
    };

    const onChange = useCallback((value, viewUpdate) => {
        setFormState((prevState) => ({
            ...prevState,
            code: value,
            size: value.length,
        }));
    }, []);

    const onSubmit = async () => {
        console.log("Form State: ", formState);

        try {
            const response = await fetch("/api/submit-code", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify(formState),
            });

            if (response.ok) {
                const json = await response.json();
                console.log(json);
                const newPercentage = json.percentage;
                setPercentage(newPercentage.toFixed(0));

d            } else {
                const error = await response.text();
                console.error(error);
            }
        } catch (error) {
            console.error(error);
        }
    };

    const [vulnerabilities, setVulnerabilities] = useState([
        "Unsafe block",
        "Overflow",
        "Integer division by zero",
    ]);

    return (
        <>
           

            <nav
                className="navbar z-50 px-6 lg:px-12 w-full"
                style={{
                    background:
                        "linear-gradient(to right, #0f2027, #203a43, #2c5364)",
                    paddingTop: "30px",
                }}
            >
                <div className="flex justify-between items-center w-full">

                    <div className="flex items-center">
                        <h1 className="text-white font-bold hover:text-blue-500 hover:text-xl hover:transition-all hover:transition-duration-500">GuardianAI</h1>
                        <Link href="/">
                            <img
                                alt="GuardianAI"
                                src="lock.png"
                                width="29"
                                height="29"
                                className="mr-2"
                            />
                        </Link>
                    </div>
                    <div
                        className="italic"
                        style={{
                            position: "absolute",
                            left: "50%",
                            transform: "translateX(-50%)",
                        }}
                    >
                        Shielding Your Code, Safeguarding Your Future
                    </div>
                    <div className="flex gap-4">
                        {/* Potential place for more navigation items */}
                    </div>
                </div>
            </nav>

            <main className=" flex flex-col-reverse justify-center items-center mt-10 p-10">
                <div className="bg-gray-800 rounded-xl shadow-lg flex flex-col w-full justify-center items-center  gap-10 min-h-96  p-6">
                    <ProgressCircle percentage={percentage} />
                    <button
                        className="bg-black rounded-2xl text-white font-bold p-3 hover:bg-white hover:text-black"
                        onClick={onVulnerabilityClick}
                    >
                        Assess vulnerabilities
                    </button>

                    {showCodeVulnerability && (
                        <div className="flex flex-col gap-2">
                            {vulnerabilities.map((vulnerability, index) => (
                                <div
                                    key={index}
                                    className="bg-gray-900 text-white p-2 rounded-lg"
                                >
                                    {vulnerability}
                                </div>
                            ))}
                        </div>
                    )}
                </div>

                <div
                   className="flex justify-center items-center w-full p-6" 
                >
                    <button
                        className="bg-gradient-to-b from-gray-700 to-gray-900 text-blue-500 font-bold py-2 px-4 rounded-full p-6 shadow-lg hover:bg-gray-100 hover:text-white"
                        style={{
                            width: "120px",
                            height: "120px",
                            borderRadius: "50%",
                            border: "5px solid black",
                            fontSize: "18px",
                            display: "flex",
                            alignItems: "center",
                            justifyContent: "center",
                        }}
                        onClick={onSubmit}
                    >
                        Analyze
                    </button>
                </div>

                <div className="bg-gray-800 flex flex-col w-full items-center justify-start rounded-xl shadow-lg border-8 border-black  min-h-96 w-96" >
                    <CodeMirror
                        value={formState.code}
                        onChange={onChange}
                        extensions={[rust(), vscodeDark]}
                        theme={vscodeDark}
                        className="w-full min-h-full "
                    />
                </div>
            </main>
        </>
    );
>>>>>>> c23e90a2614a191bbca99df50b9bfdeef8ac31ab
}
