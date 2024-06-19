import * as vscode from "vscode";
import axios from "axios";
import { v4 as uuidv4 } from "uuid";
import { WebSocket } from "ws";
import dotenv from 'dotenv';

dotenv.config();

// Use environment variables for sensitive information
const AUTH0_DOMAIN = process.env.AUTH0_DOMAIN;
const CLIENT_ID = process.env.CLIENT_ID;
const CLIENT_SECRET = process.env.CLIENT_SECRET;
const CALLBACK_URI = process.env.CALLBACK_URI;

let statusBarItem: vscode.StatusBarItem;
let decorationsArray: vscode.DecorationOptions[] = [];
const vulnerableDecorationType = vscode.window.createTextEditorDecorationType({
  textDecoration: "underline wavy red",
});

interface VulnerableSnippet {
  code: string;
  description: string;
  fixes: string;
}

interface Vulnerabilities {

  snippets: VulnerableSnippet[];
}

interface AnalyzeResponse {
  request_id: string;
  vulnerabilities: Vulnerabilities;
}

export async function authenticate(
  context: vscode.ExtensionContext
): Promise<string | null> {
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
): Promise<void> {
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
    console.log("Domain", AUTH0_DOMAIN, "Client ID", CLIENT_ID, "Client Secret", CLIENT_SECRET);
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
  const requestId = uuidv4();


  let response;
  try {
    response = await axios.post(
      "http://localhost:8080/code-detective/analyze_code",
      { code: selectedText, request_id: requestId },
      { headers: { Authorization: `Bearer ${api_auth_token}` } }
    );
    console.log("API response", response.data);
    vscode.window.showInformationMessage("API response: " + response.data);
  } catch (error) {
    console.error("API call error", error);
    vscode.window.showErrorMessage("Failed to call API");
    return;
  }

  const ws = new WebSocket(
    `ws://localhost:8080/code-detective-model/ws/${requestId}`
  );

  ws.on("open", () => {
    console.log("Connected to server");

  });

  ws.on("message", (data: AnalyzeResponse) => {
    try {
      console.log("Received message from server:", data);
    } catch (error) {
      console.error("Failed to parse WebSocket message:", data, error);
    }

    ws.close();
  });

  ws.on("close", () => {
    console.log("Disconnected from server");
  });

  ws.on("error", (error) => {
    console.error("WebSocket error:", error);
  });
}

function handleVulnerabilityData(data: AnalyzeResponse) {
  let vulnerableSnippets: VulnerableSnippet[] = data.vulnerabilities.snippets;
  console.log("Vulnerable snippets", vulnerableSnippets);
  let activeEditor = vscode.window.activeTextEditor;
  if (activeEditor) {
    let doc = activeEditor.document;

    for (let snippet of vulnerableSnippets) {
      console.log("Snippet", snippet.code, "is vulnerable");
      let range = findRangeOfSnippetInDocument(doc, snippet.code);
      console.log(
        "Range",
        range ? range.start : null,
        range ? range.end : null
      );
      if (range) {
        decorationsArray.push({ range: range });
        console.log("Found snippet", snippet.code, "at", range);
      }
    }

    activeEditor.setDecorations(vulnerableDecorationType, decorationsArray);
    console.log("Decorated vulnerable snippets");

    registerHoverProvider(vulnerableSnippets);
    registerCodeActionsProvider(vulnerableSnippets);
  }
}

function tokenize(text: string): { tokens: string[]; positions: number[] } {
  const tokens: string[] = [];
  const positions: number[] = [];
  const regex = /\S+/g;
  let match;
  while ((match = regex.exec(text)) !== null) {
    tokens.push(match[0]);
    positions.push(match.index);
  }
  return { tokens, positions };
}

function findRangeOfSnippetInDocument(
  doc: vscode.TextDocument,
  snippet: string
): vscode.Range | null {
  const text = doc.getText();
  const docTokens = tokenize(text);
  const snippetTokens = tokenize(snippet);

  const { tokens: docTokensArray, positions: docPositions } = docTokens;
  const { tokens: snippetTokensArray } = snippetTokens;

  const cleanedDocText = docTokensArray.join(" ");
  const cleanedSnippetText = snippetTokensArray.join(" ");

  const startIndex = cleanedDocText.indexOf(cleanedSnippetText);
  if (startIndex === -1) {
    return null; // snippet not found in document
  }

  // Map cleaned indices back to original indices
  const startTokenIndex =
    cleanedDocText.substring(0, startIndex).split(" ").length - 1;
  const endTokenIndex = startTokenIndex + snippetTokensArray.length - 1;

  const startPos = doc.positionAt(docPositions[startTokenIndex]);
  const endPos = doc.positionAt(
    docPositions[endTokenIndex] +
    snippetTokensArray[snippetTokensArray.length - 1].length
  );

  return new vscode.Range(startPos, endPos);
}

function registerHoverProvider(vulnerableSnippets: VulnerableSnippet[]): void {
  vscode.languages.registerHoverProvider(
    { pattern: "**/*" },
    {
      provideHover(document, position, token) {
        let range = document.getWordRangeAtPosition(position);
        let word = document.getText(range);
        for (let snippet of vulnerableSnippets) {
          if (snippet.code.includes(word)) {
            return new vscode.Hover(
              `Vulnerability: ${snippet.description}`
            );
          }
        }
        return null;
      },
    }
  );
}

function registerCodeActionsProvider(
  vulnerableSnippets: VulnerableSnippet[]
): void {
  vscode.languages.registerCodeActionsProvider(
    { pattern: "**/*" },
    {
      provideCodeActions(document, range, context, token) {
        let codeActions: vscode.CodeAction[] = [];
        let selectedText = document.getText(range);
        for (let snippet of vulnerableSnippets) {
          if (snippet.code.includes(selectedText)) {
            let action = new vscode.CodeAction(
              `Fix vulnerability: ${snippet.description}`,
              vscode.CodeActionKind.QuickFix
            );
            action.edit = new vscode.WorkspaceEdit();
            let snippetRange = findRangeOfSnippetInDocument(
              document,
              snippet.code
            );
            if (snippetRange) {
              action.edit.replace(
                document.uri,
                snippetRange,
                snippet.fixes
              );

              action.command = {
                command: "smartguardian.fixAndFormat",
                title: "Fix and Format",
                arguments: [document.uri, snippetRange],
              };

              codeActions.push(action);
            }
          }
        }
        return codeActions;
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
  console.log(
    'Congratulations, your extension "smartguardian" is now active!'
  );

  statusBarItem = vscode.window.createStatusBarItem(
    vscode.StatusBarAlignment.Left,
    100
  );
  context.subscriptions.push(statusBarItem);

  context.subscriptions.push(
    vscode.commands.registerCommand("smartguardian.helloWorld", () => {
      vscode.window.showInformationMessage(
        "Hello World from SmartGuardian!"
      );
    })
  );

  context.subscriptions.push(
    vscode.commands.registerCommand(
      "smartguardian.detectVulnerabilities",
      async () => {
        await callApiWithSelectedText(context);
      }
    )
  );

  context.subscriptions.push(
    vscode.commands.registerCommand(
      "smartguardian.unauthenticate",
      async () => {
        await context.secrets.delete("auth_token");
        updateStatusBarItem(false);
        vscode.window.showInformationMessage(
          "Unauthenticated successfully"
        );
      }
    )
  );

  context.subscriptions.push(
    vscode.commands.registerCommand(
      "smartguardian.authenticate",
      async () => {
        await authenticate(context);
      }
    )
  );

  context.subscriptions.push(
    vscode.commands.registerCommand(
      "smartguardian.fixAndFormat",
      async (uri: vscode.Uri, range: vscode.Range) => {
        await vscode.commands.executeCommand(
          "editor.action.formatDocument",
          uri
        );
        removeDecoration(range);
      }
    )
  );

  // Initialize status bar item
  context.secrets.get("auth_token").then((token) => {
    updateStatusBarItem(!!token);
  });
}

export function deactivate(): void { }
