import * as assert from "assert";
import * as vscode from "vscode";
import * as sinon from "sinon";
import axios from "axios";
import { authenticate, callApiWithSelectedText } from "../extension";
import { v4 as uuidv4 } from 'uuid';

suite("Extension Test Suite", () => {
    vscode.window.showInformationMessage("Start all tests.");

    let showInformationMessageSpy: sinon.SinonSpy;
    let showErrorMessageSpy: sinon.SinonSpy;
    let postStub: sinon.SinonStub;
    let openExternalStub: sinon.SinonStub;
    let context: vscode.ExtensionContext;

    setup(() => {
        sinon.restore();
        showInformationMessageSpy = sinon.spy(vscode.window, "showInformationMessage");
        showErrorMessageSpy = sinon.spy(vscode.window, "showErrorMessage");
        postStub = sinon.stub(axios, "post");
        openExternalStub = sinon.stub(vscode.env, "openExternal");

        context = {
            secrets: {
                get: sinon.stub().resolves(null),
                store: sinon.stub().resolves(),
            },
            globalState: {
                get: sinon.stub(),
                update: sinon.stub().resolves(),
            },
            subscriptions: [],
        } as unknown as vscode.ExtensionContext;
    });

    teardown(() => {
        sinon.restore();
    });

    test("Authenticate function - success", async () => {
        const token = "fake-jwt-token";
        postStub.resolves({ data: { access_token: token } });

        // Mock state
        const storeStub = sinon.stub(context.secrets, "store");

        const actualToken = await authenticate(context);

        assert.strictEqual(actualToken, token);
        assert.strictEqual(showInformationMessageSpy.calledWith("Authenticated successfully"), true);
        sinon.assert.calledWith(storeStub, "auth_token", token);
    });

    test("Authenticate function - failure", async () => {
        postStub.rejects(new Error("Failed to authenticate"));

        await authenticate(context);

        assert.strictEqual(showErrorMessageSpy.calledWith("Failed to authenticate"), true);
        assert.strictEqual(openExternalStub.called, true);
    });

    test("Call API with selected text", async () => {
        const token = "fake-jwt-token";
        postStub.resolves({ data: { access_token: token } });

        sinon.stub(vscode.window, "activeTextEditor").value({
            selection: {
                isEmpty: false,
            },
            document: {
                getText: () => "selected text",
            },
        });

        (context.secrets.get as sinon.SinonStub).resolves(token);
        const apiResponse = { data: "API response" };
        postStub.withArgs(
            "https://api-gateway.com/protected-endpoint",
            { data: "selected text" },
            sinon.match.any
        ).resolves(apiResponse);

        await callApiWithSelectedText(context);

        assert.strictEqual(showInformationMessageSpy.calledWith("API call successful: API response"), true);
    });

    test("Call API with no selected text", async () => {
        sinon.stub(vscode.window, "activeTextEditor").value({
            selection: {
                isEmpty: true,
            },
            document: {
                getText: () => "",
            },
        });

        await callApiWithSelectedText(context);

        assert.strictEqual(showErrorMessageSpy.calledWith("No text selected"), true);
    });
});
