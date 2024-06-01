import * as vscode from "vscode";
import axios from "axios";
import { v4 as uuidv4 } from "uuid";

const AUTH0_DOMAIN = "dev-az3di7fabdoc8vlz.uk.auth0.com";
const CLIENT_ID = "BBVCZqG7W4JzbFlhpZDNeRVwV4W2PdPq";
const CALLBACK_URI = "vscode://your-extension-id/callback";

export async function authenticate(context: vscode.ExtensionContext) {
    const existingToken = await context.secrets.get("auth_token");
    if (existingToken) {
        vscode.window.showInformationMessage("Already authenticated");
        return existingToken;
    }

    const state = uuidv4();
    context.workspaceState.update("auth_state", state);

    const loginUrl = `https://${AUTH0_DOMAIN}/authorize?response_type=token&client_id=${CLIENT_ID}&redirect_uri=${CALLBACK_URI}&state=${state}`;

    vscode.env.openExternal(vscode.Uri.parse(loginUrl));

    const token = await new Promise<string | undefined>((resolve) => {
        const disposable = vscode.window.registerUriHandler({
            handleUri: (uri: vscode.Uri) => {
                const token = getTokenFromUri(uri, context);
                if (token) {
                    context.secrets.store("auth_token", token);
                    resolve(token);
                } else {
                    resolve(undefined);
                }
                disposable.dispose();
            },
        });
        context.subscriptions.push(disposable);
    });

    if (!token) {
        vscode.window.showErrorMessage("Authentication failed");
        return null;
    }

    return token;
}

function getTokenFromUri(
    uri: vscode.Uri,
    context: vscode.ExtensionContext
): string | null {
    const fragment = uri.fragment;
    const params = new URLSearchParams(fragment);
    const token = params.get("access_token");
    const state = params.get("state");
    const storedState = context.workspaceState.get("auth_state");

    if (state !== storedState) {
        vscode.window.showErrorMessage(
            "State mismatch. Potential CSRF attack."
        );
        return null;
    }

    context.workspaceState.update("auth_state", undefined);
    return token;
}

export async function callApiWithSelectedText(
    context: vscode.ExtensionContext
) {
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

    const token = await authenticate(context);
    if (!token) {
        return;
    }

    try {
        const response = await axios.post(
            "https://api-gateway.com/protected-endpoint",
            { data: selectedText },
            { headers: { Authorization: `Bearer ${token}` } }
        );

        vscode.window.showInformationMessage(
            "API call successful: " + response.data
        );
    } catch (error) {
        vscode.window.showErrorMessage("API call failed: " + error);
    }
}

// This method is called when your extension is activated
export function activate(context: vscode.ExtensionContext) {
    console.log(
        'Congratulations, your extension "smartguardian" is now active!'
    );

    let disposableHelloWorld = vscode.commands.registerCommand(
        "smartguardian.helloWorld",
        () => {
            vscode.window.showInformationMessage(
                "Hello World from SmartGuardian!"
            );
        }
    );

    let disposableCallApi = vscode.commands.registerCommand(
        "smartguardian.detectVulnerabilities",
        async () => {
            await callApiWithSelectedText(context);
        }
    );

    context.subscriptions.push(disposableHelloWorld);
    context.subscriptions.push(disposableCallApi);
}

// This method is called when your extension is deactivated
export function deactivate() {}
