"use client";

import Head from "next/head";
import Link from "next/link";
import { useCallback, useState, useEffect } from "react";
import { useCodeMirror } from "@uiw/react-codemirror";
import CodeMirror from "@uiw/react-codemirror";
import { rust } from "@codemirror/lang-rust";
import { vscodeDark } from "@uiw/codemirror-theme-vscode";
import ProgressCircle from "../components/ProgressCircle";
import { EditorView } from "@codemirror/view";

export default function Home() {
    const [showCodeVulnerability, setShowCodeVulnerability] = useState(false);
    const placeholder = `fn main() {
    println!("Hello, world!");
}
`;
    const [percentage, setPercentage] = useState(
        Math.floor(Math.random() * 101)
    );

    const [formState, setFormState] = useState({
        repo_name: "test",
        path: "test",
        code: placeholder,
        license: "MIT",
        size: placeholder.length,
    });

    const onVulnerabilityClick = () => {
        setShowCodeVulnerability(!showCodeVulnerability);
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
            } else {
                const error = await response.text();
                console.error(error);
            }
        } catch (error) {
            console.error(error);
        }
    };

    const vulnerabilities = [
        "Unsafe block",
        "Overflow",
        "Integer division by zero",
    ];

    return (
        <>
            <Head>
                <title>GuardianAI</title>
                <link rel="icon" href="/favicon.ico" />
            </Head>

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

            <main className="main flex justify-center  mt-10 p-10">
                <div className="bg-gray-800 rounded-xl shadow-lg flex flex-col justify-center  gap-10 min-h-96 p-6">
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
                    className="my-auto"
                    style={{ marginLeft: "30px", marginRight: "30px" }}
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

                <div className="bg-gray-800 flex flex-col rounded-xl shadow-lg border-8 border-black w-ful min-h-96">
                    <CodeMirror
                        value={formState.code}
                        onChange={onChange}
                        extensions={[rust(), vscodeDark]}
                        theme={vscodeDark}
                        className="h-full"
                    />
                </div>
            </main>
        </>
    );
}
