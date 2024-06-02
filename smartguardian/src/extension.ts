import * as vscode from "vscode";
import axios from "axios";
import { v4 as uuidv4 } from "uuid";

const AUTH0_DOMAIN = "dev-az3di7fabdoc8vlz.uk.auth0.com";
const CLIENT_ID = "BBVCZqG7W4JzbFlhpZDNeRVwV4W2PdPq";
const CLIENT_SECRET = "5XtekSVFh634T-e65llkg7RcZW4jQwaPsFvC9pMo053wKB2nVtfs2PusPp3B6lKS";
const CALLBACK_URI = "vscode://smart-guardian.safeContracts/callback";

const safe_contracts_api_CLIENT_ID = "NFb8mHU35GjKHcZHahYaV5CaW66o2LAb";
const safe_contracts_api_CLIENT_SECRET = "1GmsJcQAIxCWNOGHyVMTJmZvRmMh2KfxCSKR1vpt_v_VlJZkxBYcsYG_3-HKO8Lq";

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
    console.log("Opened browser for login");

    const token = await new Promise<string | undefined>((resolve) => {
        const disposable = vscode.window.registerUriHandler({
            handleUri: (uri: vscode.Uri) => {
                console.log("Received URI", uri);
                const token = getTokenFromUri(uri, context);
                if (token) {
                    console.log("Authenticated with token", token);
                    context.secrets.store("auth_token", token);
                    resolve(token);
                } else {
                    console.log("Authentication failed");
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

    const auth_token = await authenticate(context);
    if (!auth_token) {
        console.log("Authentication failed");
        return;
    }

    const api_auth_response = await axios.post(
        'https://dev-az3di7fabdoc8vlz.uk.auth0.com/oauth/token'
        , {
            client_id: CLIENT_ID,
            client_secret: CLIENT_SECRET,
            audience: "https://safe-contracts/",
            grant_type: "client_credentials"
        }

    );

    console.log("API auth response", api_auth_response.data);

    const api_auth_token = api_auth_response.data.access_token;


    console.log("Authenticated with token", api_auth_token);

   const response = await axios.post(
    "http://localhost:8080/feature-extractor/analyze_code", 
    { code: selectedText },
    { headers: { Authorization: `Bearer ${api_auth_token}` } }

   );

    console.log("API response", response.data);
    vscode.window.showInformationMessage("API response: " + response.data);
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
