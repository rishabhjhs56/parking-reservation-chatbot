import os
import pytest
from unittest.mock import Mock, patch, MagicMock

# Set CI environment
os.environ['CI'] = 'true'

# Mock Azure OpenAI Embeddings
class MockEmbeddings:
    def embed_query(self, text):
        # Return realistic embedding vector (1536 dimensions)
        return [0.1] * 1536
    
    def embed_documents(self, texts):
        return [[0.1] * 1536 for _ in texts]

# Mock Azure LLM
class MockLLM:
    def invoke(self, messages):
        # Return realistic chat response
        mock_response = Mock()
        mock_response.content = f"Mock response for: {messages}"
        return mock_response

# Mock Milvus Vector Store
class MockMilvusStore:
    def __init__(self):
        self.mock_data = [
            {
                'id': 1,
                'distance': 0.5,
                'entity': {
                    'text': 'Parking charges for SUV in Delhi: Rs. 50/hour for first 2 hours, Rs. 25/hour thereafter.',
                    'metadata': {'source': 'parking_rules.pdf'}
                }
            },
            {
                'id': 2,
                'distance': 0.7,
                'entity': {
                    'text': 'Available parking slots in Delhi: Connaught Place (50 slots), India Gate (30 slots).',
                    'metadata': {'source': 'parking_availability.json'}
                }
            }
        ]
    
    def search(self, vector, limit=5):
        # Return mock search results
        return [self.mock_data[:limit]]

# Mock FastAPI MCP functions
def mock_mcp_sync():
    return {"status": "success", "synced_reservations": 5}

def mock_mcp_approved():
    return {"status": "success", "approved_reservations": 3}

# Apply mocks before imports
with patch('app.utils.azure_embeddings.get_embeddings', return_value=MockEmbeddings()), \
     patch('app.utils.azure_llm.get_llm', return_value=MockLLM()), \
     patch('app.rag.milvus_client.MilvusVectorStore', MockMilvusStore), \
     patch('pymilvus.MilvusClient', return_value=Mock()):
    
    from app.graph.nodes import chatbot

@pytest.fixture
def mock_chatbot():
    return chatbot

@pytest.fixture
def mock_fastapi_responses():
    return {
        "sync_success": mock_mcp_sync(),
        "approved_success": mock_mcp_approved()
    }