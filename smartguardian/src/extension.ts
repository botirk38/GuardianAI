import * as vscode from "vscode";
import axios from "axios";
import { v4 as uuidv4 } from "uuid";

// Use environment variables for sensitive information
const AUTH0_DOMAIN = process.env.AUTH0_DOMAIN || "dev-az3di7fabdoc8vlz.uk.auth0.com";
const CLIENT_ID = process.env.CLIENT_ID || "BBVCZqG7W4JzbFlhpZDNeRVwV4W2PdPq";
const CLIENT_SECRET = process.env.CLIENT_SECRET || "5XtekSVFh634T-e65llkg7RcZW4jQwaPsFvC9pMo053wKB2nVtfs2PusPp3B6lKS";
const CALLBACK_URI = process.env.CALLBACK_URI || "vscode://smart-guardian.safeContracts/callback";

let statusBarItem: vscode.StatusBarItem;
let decorationsArray: vscode.DecorationOptions[] = [];
const vulnerableDecorationType = vscode.window.createTextEditorDecorationType({
  backgroundColor: "rgba(255, 0, 0, 0.5)",
});

export async function authenticate(context: vscode.ExtensionContext): Promise<string | null> {
  const existingToken = await context.secrets.get("auth_token");
  if (existingToken) {
    vscode.window.showInformationMessage("Already authenticated");
    updateStatusBarItem(true);
    return existingToken;
  }

  const state = uuidv4();
  context.workspaceState.update("auth_state", state);

  const loginUrl = `https://${AUTH0_DOMAIN}/authorize?response_type=token&client_id=${CLIENT_ID}&redirect_uri=${CALLBACK_URI}&state=${state}`;

  vscode.env.openExternal(vscode.Uri.parse(loginUrl));
  console.log("Opened browser for login");

  return new Promise<string | null>((resolve) => {
    const disposable = vscode.window.registerUriHandler({
      handleUri: (uri: vscode.Uri) => {
        console.log("Received URI", uri);
        const token = getTokenFromUri(uri, context);
        if (token) {
          console.log("Authenticated with token", token);
          context.secrets.store("auth_token", token);
          updateStatusBarItem(true);
          resolve(token);
        } else {
          console.log("Authentication failed");
          vscode.window.showErrorMessage("Authentication failed");
          resolve(null);
        }
        disposable.dispose();
      },
    });
    context.subscriptions.push(disposable);
  });
}

function getTokenFromUri(uri: vscode.Uri, context: vscode.ExtensionContext): string | null {
  const fragment = uri.fragment;
  const params = new URLSearchParams(fragment);
  const token = params.get("access_token");
  const state = params.get("state");
  const storedState = context.workspaceState.get("auth_state");

  if (state !== storedState) {
    vscode.window.showErrorMessage("State mismatch. Potential CSRF attack.");
    return null;
  }

  context.workspaceState.update("auth_state", undefined);
  return token;
}

export async function callApiWithSelectedText(context: vscode.ExtensionContext): Promise<void> {
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
    return;
  }

  let api_auth_token: string;
  try {
    const api_auth_response = await axios.post(
      `https://${AUTH0_DOMAIN}/oauth/token`,
      {
        client_id: CLIENT_ID,
        client_secret: CLIENT_SECRET,
        audience: "https://safe-contracts/",
        grant_type: "client_credentials",
      }
    );
    api_auth_token = api_auth_response.data.access_token;
    console.log("Authenticated with token", api_auth_token);
  } catch (error) {
    console.error("API auth error", error);
    vscode.window.showErrorMessage("Failed to authenticate API");
    return;
  }

  let response;
  try {
    response = await axios.post(
      "http://localhost:8080/feature-extractor/analyze_code",
      { code: selectedText },
      { headers: { Authorization: `Bearer ${api_auth_token}` } }
    );
    console.log("API response", response.data);
    vscode.window.showInformationMessage("API response: " + response.data);
  } catch (error) {
    console.error("API call error", error);
    vscode.window.showErrorMessage("Failed to call API");
    return;
  }

  let vulnerableSnippets = response.data;
  let activeEditor = vscode.window.activeTextEditor;
  if (activeEditor) {
    let doc = activeEditor.document;

    for (let snippet of vulnerableSnippets) {
      let range = findRangeOfSnippetInDocument(doc, snippet.code);
      if (range) {
        decorationsArray.push({ range: range });
      }
    }

    activeEditor.setDecorations(vulnerableDecorationType, decorationsArray);
  }

  // Register vscode hover provider
  vscode.languages.registerHoverProvider(
    { pattern: "**/*" },
    {
      provideHover(document, position, token) {
        let range = document.getWordRangeAtPosition(position);
        let word = document.getText(range);
        for (let snippet of vulnerableSnippets) {
          if (snippet.code.includes(word)) {
            return new vscode.Hover(`Vulnerability: ${snippet.vulnerability}`);
          }
        }
        return null;
      },
    }
  );

  // Register a code actions provider
  vscode.languages.registerCodeActionsProvider(
    { pattern: "**/*" },
    {
      provideCodeActions(document, range, context, token) {
        let word = document.getText(range);
        for (let snippet of vulnerableSnippets) {
          if (snippet.code.includes(word)) {
            let action = new vscode.CodeAction(
              `Fix vulnerability: ${snippet.vulnerability}`,
              vscode.CodeActionKind.QuickFix
            );
            action.edit = new vscode.WorkspaceEdit();
            action.edit.replace(document.uri, range, snippet.fix);
            action.command = {
              command: "removeDecoration",
              title: "Remove decoration",
              arguments: [range],
            };
            return [action];
          }
        }
        return [];
      },
    }
  );
}

function removeDecoration(range: vscode.Range): void {
  decorationsArray = decorationsArray.filter(
    (decoration) => !decoration.range.isEqual(range)
  );
  let activeEditor = vscode.window.activeTextEditor;
  if (activeEditor) {
    activeEditor.setDecorations(vulnerableDecorationType, decorationsArray);
  }
}

function findRangeOfSnippetInDocument(doc: vscode.TextDocument, snippet: string): vscode.Range | null {
  let text = doc.getText();
  let startIndex = text.indexOf(snippet);
  if (startIndex === -1) {
    return null; // snippet not found in document
  }

  let endIndex = startIndex + snippet.length;

  // Convert the start and end indices to Positions
  let startPos = doc.positionAt(startIndex);
  let endPos = doc.positionAt(endIndex);

  // Create and return a new Range from the Positions
  return new vscode.Range(startPos, endPos);
}

function updateStatusBarItem(isAuthenticated: boolean): void {
  if (isAuthenticated) {
    statusBarItem.text = "$(shield) Logged in";
    statusBarItem.command = "smartguardian.unauthenticate";
  } else {
    statusBarItem.text = "$(shield) Logged out";
    statusBarItem.command = "smartguardian.authenticate";
  }
  statusBarItem.show();
}

export function activate(context: vscode.ExtensionContext): void {
  console.log('Congratulations, your extension "smartguardian" is now active!');

  statusBarItem = vscode.window.createStatusBarItem(vscode.StatusBarAlignment.Left, 100);
  context.subscriptions.push(statusBarItem);

  context.subscriptions.push(
    vscode.commands.registerCommand("smartguardian.helloWorld", () => {
      vscode.window.showInformationMessage("Hello World from SmartGuardian!");
    })
  );

  context.subscriptions.push(
    vscode.commands.registerCommand("smartguardian.detectVulnerabilities", async () => {
      await callApiWithSelectedText(context);
    })
  );

  context.subscriptions.push(
    vscode.commands.registerCommand("smartguardian.unauthenticate", async () => {
      await context.secrets.delete("auth_token");
      updateStatusBarItem(false);
      vscode.window.showInformationMessage("Unauthenticated successfully");
    })
  );

  context.subscriptions.push(
    vscode.commands.registerCommand("smartguardian.authenticate", async () => {
      await authenticate(context);
    })
  );

  context.subscriptions.push(
    vscode.commands.registerCommand("removeDecoration", (range: vscode.Range) => {
      removeDecoration(range);
    })
  );

  // Initialize status bar item
  context.secrets.get("auth_token").then((token) => {
    updateStatusBarItem(!!token);
  });
}

export function deactivate(): void { }

