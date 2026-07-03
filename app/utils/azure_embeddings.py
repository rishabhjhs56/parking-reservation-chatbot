from functools import lru_cache

from langchain_openai import AzureOpenAIEmbeddings

from app.utils.config import (
    AZURE_API_KEY,
    AZURE_API_VERSION,
    AZURE_ENDPOINT,
    AZURE_EMBEDDING_DEPLOYMENT,
)


@lru_cache(maxsize=1)
def get_embeddings():
    """
    Lazily create the Azure embedding model.

    This avoids creating the client during module import,
    which allows unit tests to run without Azure credentials.
    """
    return AzureOpenAIEmbeddings(
        api_key=AZURE_API_KEY,
        azure_endpoint=AZURE_ENDPOINT,
        api_version=AZURE_API_VERSION,
        azure_deployment=AZURE_EMBEDDING_DEPLOYMENT,
    )