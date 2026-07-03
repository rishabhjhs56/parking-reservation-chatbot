from langchain_openai import AzureOpenAIEmbeddings

from app.utils.config import (
    AZURE_API_KEY,
    AZURE_API_VERSION,
    AZURE_ENDPOINT,
    AZURE_EMBEDDING_DEPLOYMENT,
)

embeddings = AzureOpenAIEmbeddings(
    api_key=AZURE_API_KEY,
    azure_endpoint=AZURE_ENDPOINT,
    api_version=AZURE_API_VERSION,
    azure_deployment=AZURE_EMBEDDING_DEPLOYMENT,
)