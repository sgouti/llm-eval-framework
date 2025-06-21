import pytest
import boto3
from src.models.ollama_handler import OllamaHandler
from src.models.bedrock_handler import BedrockHandler

@pytest.mark.skipif(not hasattr(OllamaHandler, 'client'), reason="Ollama server not running")
def test_ollama_handler(mocker):
    # Mock ollama client to avoid actual server call
    mock_client = mocker.patch("ollama.Client")
    mock_client_instance = mock_client.return_value
    mock_client_instance.chat.return_value = {"message": {"content": "Test response"}}
    
    model = OllamaHandler("llama3:8b")
    response = model.generate_response("Test input")
    
    assert response == "Test response"

def test_ollama_handler_error(mocker):
    # Mock ollama client to raise an error
    mock_client = mocker.patch("ollama.Client")
    mock_client_instance = mock_client.return_value
    mock_client_instance.chat.side_effect = Exception("Connection failed")
    
    model = OllamaHandler("llama3:8b")
    response = model.generate_response("Test input")
    
    assert "Error generating response" in response

@pytest.mark.skipif(not boto3.Session().get_credentials(), reason="AWS credentials not configured")
def test_bedrock_handler(mocker):
    # Mock boto3 client to avoid actual AWS call
    mock_client = mocker.patch("boto3.client")
    mock_client_instance = mock_client.return_value
    mock_client_instance.invoke_model.return_value = {
        "body": mocker.Mock(read=mocker.Mock(return_value=b'{"results": [{"outputText": "Test response"}]}'))
    }
    
    model = BedrockHandler("anthropic.claude-v2")
    response = model.generate_response("Test input")
    
    assert response == "Test response"

def test_bedrock_handler_error(mocker):
    # Mock boto3 client to raise an error
    mock_client = mocker.patch("boto3.client")
    mock_client_instance = mock_client.return_value
    mock_client_instance.invoke_model.side_effect = Exception("AWS error")
    
    model = BedrockHandler("anthropic.claude-v2")
    response = model.generate_response("Test input")
    
    assert "Error generating response" in response