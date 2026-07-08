import pytest

# Simple conftest for real testing - no mocking
@pytest.fixture
def sample_fixture():
    return "real_test"

# Add any other real fixtures if needed
@pytest.fixture
def test_data():
    return {
        "test_query": "What are parking charges in Delhi?",
        "test_location": "Delhi",
        "test_vehicle": "SUV"
    }