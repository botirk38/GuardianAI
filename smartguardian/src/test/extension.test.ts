import * as assert from 'assert';
import * as vscode from 'vscode';
import * as sinon from 'sinon';
import axios from 'axios';
import { authenticate, callApiWithSelectedText } from '../extension';

suite('Extension Test Suite', () => {
  vscode.window.showInformationMessage('Start all tests.');

  let showInformationMessageSpy: sinon.SinonSpy;
  let showErrorMessageSpy: sinon.SinonSpy;
  let postStub: sinon.SinonStub;

  setup(() => {
    sinon.restore();
    showInformationMessageSpy = sinon.spy(vscode.window, 'showInformationMessage');
    showErrorMessageSpy = sinon.spy(vscode.window, 'showErrorMessage');
    postStub = sinon.stub(axios, 'post');
  });

  teardown(() => {
    sinon.restore();
  });
   

  test('Authenticate function - success', async () => {
    const token = 'fake-jwt-token';
    postStub.resolves({ data: { access_token: token } });

    const actualToken = await authenticate();

    assert.strictEqual(actualToken, token);
    assert.strictEqual(showInformationMessageSpy.calledWith('Authenticated successfully'), true);
  });

  test('Authenticate function - failure', async () => {
    postStub.rejects(new Error('Failed to authenticate'));
    const openExternalStub = sinon.stub(vscode.env, 'openExternal');

    await authenticate();

    assert.strictEqual(showErrorMessageSpy.calledWith('Failed to authenticate'), true);
    assert.strictEqual(openExternalStub.called, true);
  });

  test('Call API with selected text', async () => {
    const token = 'fake-jwt-token';
    postStub.resolves({ data: { access_token: token } });
    sinon.stub(vscode.window, 'activeTextEditor').value({
      selection: {
        isEmpty: false,
      },
      document: {
        getText: () => 'selected text',
      },
    });
    const apiResponse = { data: 'API response' };
    postStub.withArgs('https://api-gateway.com/protected-endpoint', { data: 'selected text' }, sinon.match.any).resolves(apiResponse);

    await callApiWithSelectedText();

    assert.strictEqual(showInformationMessageSpy.calledWith('API call successful: API response'), true);
  });

  test('Call API with no selected text', async () => {
    sinon.stub(vscode.window, 'activeTextEditor').value({
      selection: {
        isEmpty: true,
      },
      document: {
        getText: () => '',
      },
    });

    await callApiWithSelectedText();

    assert.strictEqual(showErrorMessageSpy.calledWith('No text selected'), true);
  });
});
