import os
import sys
import pytest
from unittest.mock import Mock, patch, MagicMock

# Set environment variables FIRST
os.environ['CI'] = 'true'
os.environ['MILVUS_URI'] = 'mock://localhost'

# Mock modules before any imports
sys.modules['pymilvus'] = MagicMock()
sys.modules['pymilvus.MilvusClient'] = MagicMock()

# Mock Azure config with ACTUAL STRING VALUES (not MagicMock)
mock_config = MagicMock()
mock_config.AZURE_API_KEY = 'mock-api-key'
mock_config.AZURE_ENDPOINT = 'https://mock.openai.azure.com'
mock_config.AZURE_API_VERSION = '2024-02-01'
mock_config.AZURE_EMBEDDING_DEPLOYMENT = 'mock-embedding-deployment'
mock_config.AZURE_DEPLOYMENT_NAME = 'mock-chat-deployment'  # Add this
mock_config.FASTAPI_MCP_API_KEY = 'mock-fastapi-key'  # Add this
sys.modules['app.utils.config'] = mock_config

# Mock embedding function
def mock_get_embeddings():
    mock_obj = MagicMock()
    mock_obj.embed_query.return_value = [0.1] * 1536
    return mock_obj

# Mock LLM function
def mock_get_llm():
    mock_llm = MagicMock()
    mock_llm.invoke.return_value = MagicMock(content="Mock response")
    return mock_llm

# Apply patches
with patch('app.utils.azure_embeddings.get_embeddings', side_effect=mock_get_embeddings), \
     patch('app.utils.azure_llm.get_llm', side_effect=mock_get_llm):
    from app.graph.nodes import chatbot

@pytest.fixture
def mock_chatbot():
    return chatbot