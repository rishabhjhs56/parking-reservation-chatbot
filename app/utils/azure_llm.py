from functools import lru_cache
from langchain_openai import AzureChatOpenAI
from app.utils.config import (
    AZURE_ENDPOINT,
    AZURE_API_KEY,
    AZURE_API_VERSION,
    AZURE_DEPLOYMENT_NAME,
)

@lru_cache
def get_llm():
    return AzureChatOpenAI(
        azure_endpoint=AZURE_ENDPOINT,
        api_key=AZURE_API_KEY,
        api_version=AZURE_API_VERSION,
        azure_deployment=AZURE_DEPLOYMENT_NAME,
        temperature=0,
    )