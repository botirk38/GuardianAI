// The module 'vscode' contains the VS Code extensibility API
// Import the module and reference it with the alias vscode in your code below
import * as vscode from "vscode";
import axios from "axios";

export async function authenticate() {
    try {
        const response = await axios.post(
            "https://dev-az3di7fabdoc8vlz.uk.auth0.com/oauth/token",
            {
                grant_type: "client_credentials",
                client_id: "9zGwJmZxqizhEIzIlGLYlC81kMusclKN",
                client_secret:
                    "6sksG7huhI1Tv1IrFiE6pWOAmJyBlLhSJ1d7xJnNT7xT1unD0cSXGN71fGnxOn3h",
                audience: "https://safe-contracts/",
            }
        );

        const token = response.data.access_token;

        if (!token) {
            vscode.window.showErrorMessage("Failed to authenticate");
            await redirectToLogin();
            return;
        }

        vscode.window.showInformationMessage("Authenticated successfully");
        return token;
    } catch (error) {
        vscode.window.showErrorMessage("Failed to authenticate");
        await redirectToLogin();
    }
}
export async function redirectToLogin() {
    const loginUrl = "https://dev-az3di7fabdoc8vlz.uk.auth0.com/login";
    vscode.env.openExternal(vscode.Uri.parse(loginUrl));
}

export async function callApiWithSelectedText() {
    const editor = vscode.window.activeTextEditor;
    if (!editor) {
        vscode.window.showErrorMessage("No editor is active");
        return;
    }

    const selection = editor.selection;
    const selectedText = editor.document.getText(selection);

    if (!selectedText) {
        vscode.window.showErrorMessage("No text selected");
        return;
    }

    const token = await authenticate();
    if (!token) {
        return;
    }

    try {
        const response = await axios.post(
            "https://api-gateway.com/protected-endpoint",
            {
                data: selectedText,
            },
            {
                headers: {
                    Authorization: `Bearer ${token}`,
                },
            }
        );

        vscode.window.showInformationMessage(
            "API call successful: " + response.data
        );
    } catch (error) {
        vscode.window.showErrorMessage("API call failed: " + error);
    }
}

// This method is called when your extension is activated
// Your extension is activated the very first time the command is executed
export function activate(context: vscode.ExtensionContext) {
    // Use the console to output diagnostic information (console.log) and errors (console.error)
    // This line of code will only be executed once when your extension is activated
    console.log(
        'Congratulations, your extension "smartguardian" is now active!'
    );

    // The command has been defined in the package.json file
    // Now provide the implementation of the command with registerCommand
    // The commandId parameter must match the command field in package.json
    let disposableHelloWorld = vscode.commands.registerCommand(
        "smartguardian.helloWorld",
        () => {
            // The code you place here will be executed every time your command is executed
            // Display a message box to the user
            vscode.window.showInformationMessage(
                "Hello World from SmartGuardian!"
            );
        }
    );

    let disposableCallApi = vscode.commands.registerCommand(
        "smartguardian.detectVulnerabilities",
        async () => {
            // Call the API with the selected text
            await callApiWithSelectedText();
        }
    );

    context.subscriptions.push(disposableHelloWorld);
    context.subscriptions.push(disposableCallApi);
}

// This method is called when your extension is deactivated
export function deactivate() {}
