import os
import pytest
from unittest.mock import Mock, patch, MagicMock

# Set environment variables
os.environ['CI'] = 'true'
os.environ['MILVUS_URI'] = 'mock://localhost'

# Create proper mock for Milvus search results
def mock_search(*args, **kwargs):
    # Return mock search results with correct structure
    return [[
        {
            'id': 1,
            'distance': 0.5,
            'entity': {
                'text': 'Parking charges for SUV in Delhi: Rs. 50/hour',  # Changed from 'content' to 'text'
                'metadata': {'source': 'test'}
            }
        },
        {
            'id': 2,
            'distance': 0.7,
            'entity': {
                'text': 'Additional parking information for Delhi',
                'metadata': {'source': 'test2'}
            }
        }
    ]]

# Mock Milvus before any imports
with patch('pymilvus.MilvusClient') as mock_milvus:
    mock_client = MagicMock()
    mock_client.search.side_effect = mock_search
    mock_milvus.return_value = mock_client
    
    from app.graph.nodes import chatbot

@pytest.fixture
def mock_chatbot():
    return chatbot