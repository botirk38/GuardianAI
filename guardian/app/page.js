"use client";

import Head from "next/head";
import Link from "next/link";
import { useCallback, useEffect, useState, useRef } from "react";
import CodeMirror from "@uiw/react-codemirror";
import { vscodeDark } from "@uiw/codemirror-theme-vscode";
import { rust } from "@codemirror/lang-rust";
import ProgressCircle from "../components/ProgressCircle";
import { EditorView, Decoration, DecorationSet } from "@codemirror/view";
import { EditorState } from "@codemirror/state";
import { useCodeMirror } from "@uiw/react-codemirror";
const highlightStyle = Decoration.line({
    backgroundColor: "#ffcccc", // A light red background color
});
import { Range, RangeSet } from "@codemirror/rangeset";

export default function Home() {
    const languages = [
        {
            value: "rust",
            label: "Rust",
        },

        {
            value: "python",
            label: "Python",
        },
    ];

    const [showCodeVulnerability, setShowCodeVulnerability] = useState(false);

    const [rust_code, set_rust_code] = useState(`
fn main() {
    println!("Hello, world!");
}
`);

    const onVulnerabilityClick = () => {
        setShowCodeVulnerability(!showCodeVulnerability);
    };

    const onChange = useCallback((val, viewUpdate) => {
        set_rust_code(val);
    }, []);

    const [percentage, setPercentage] = useState(
        Math.floor(Math.random() * 101)
    );

    function applyDecorations(editor) {
        // Highlight line number 10
        let line = 10;
        let lineStart = editor.state.doc.line(line).from;
        let lineEnd = editor.state.doc.line(line).to;

        let decoration = EditorView.lineHighlight({
            class: "highlighted-line",
        });
        let range = new Range(lineStart, lineEnd);
        let rangeSet = RangeSet.of(range, decoration);

        return { decorations: rangeSet };
    }

    return (
        <div>
            <Head>
                <title>GuardianAI</title>
                <link rel="icon" href="/favicon.ico" />
            </Head>

      {/* Navbar with "MOTTO HERE" in the center */}
      <nav className="navbar z-50 px-6 lg:px-12 w-full" style={{ background: 'linear-gradient(to right, #0f2027, #203a43, #2c5364)', paddingTop: '30px' }}>
        <div className="flex justify-between items-center w-full">
          <div className="flex items-center">
            <Link href="/" className="btn btn-ghost normal-case text-lg lg:text-3xl font-extrabold text-white scale-200 hover:scale-125 transition-transform duration-300 ease-in-out px-0 flex items-center">
              <img alt="GuardianAI" src="lock.png" width="29" height="29" className="mr-2" />
              GuardianAI
            </Link>
          </div>
          <div className="italic" style={{ position: 'absolute', left: '50%', transform: 'translateX(-50%)' }}>
            Shielding Your Code, Safeguarding Your Future
          </div>
          <div className="flex gap-4">
          </div>
        </div>
      </nav>

      {/* Main content area with an "Analyze" button */}
      <main className="main flex justify-center items-center h-screen">
        <div className="flex w-full justify-center" style={{ padding: '20px' }}>
          {/* Left frame box */}
          <div className="bg-gray-800 rounded-lg shadow-lg" style={{ width: '550px', height: '500px', border: '10px solid black', marginRight: '30px' }}>
            {/* Left box content */}
          </div>
            {/* Main content area with an "Analyze" button */}
            <main
                className="flex justify-center items-center h-screen"
                style={{
                    background:
                        "linear-gradient(to right, #0f2027, #203a43, #2c5364)",
                }}
            >
                <div
                    className="flex w-full justify-center"
                    style={{ padding: "20px" }}
                >
                    {/* Left frame box */}
                    <div
                        className="bg-gray-800 rounded-lg shadow-lg flex flex-col justify-center items-center"
                        style={{
                            width: "550px",
                            height: "500px",
                            border: "10px solid black",
                            marginRight: "30px",
                        }}
                    >
                        {/* Left box content */}

                        <ProgressCircle percentage={percentage} />

                        <button
                            className="bg-black p-4 rounded-2xl text-white font-bold hover:bg-white hover:text-black"
                            onClick={onVulnerabilityClick}
                        >
                            Assess vulnerabilities
                        </button>
                    </div>

          {/* Analyze button centered vertically */}
          <div className="my-auto" style={{ marginLeft: '30px', marginRight: '30px' }}>
          <button className="bg-gradient-to-b from-gray-700 to-gray-900 text-blue-500 font-bold py-2 px-4 rounded-full shadow-lg hover:bg-gradient-to-b hover:from-gray-600 hover:to-gray-800 hover:border-blue-500" style={{ width: '120px', height: '120px', borderRadius: '50%', border: '5px solid black', fontSize: '18px', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
          Analyze
          </button>
          </div>
                    {/* Analyze button centered vertically */}
                    <div
                        className="my-auto"
                        style={{ marginLeft: "30px", marginRight: "30px" }}
                    >
                        <button
                            className="bg-gradient-to-b from-gray-700 to-gray-900 text-blue-500 font-bold py-2 px-4 rounded-full shadow-lg"
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
                            onClick={() => setPercentage(Math.floor(Math.random() * 101))}
                        >
                            Analyze
                        </button>
                    </div>

                    {/* Right frame box with textarea */}
                    <div
                        className="bg-gray-800 rounded-lg shadow-lg"
                        style={{
                            width: "550px",
                            height: "500px",
                            border: "10px solid black",
                            marginLeft: "30px",
                        }}
                    >
                        <CodeMirror
                            value={rust_code}
                            theme={vscodeDark}
                            extensions={[rust()]}
                            onChange={onChange}
                            basicSetup={true}
                            onUpdate={(editor) => {
                                if (showCodeVulnerability) {
                                    let update = applyDecorations(editor);
                                    editor.dispatch({
                                        effects:
                                            EditorView.updateListener.of(
                                                update
                                            ),
                                    });
                                }
                            }}
                        />
                    </div>
                </div>
            </main>
        </div>
    );
}