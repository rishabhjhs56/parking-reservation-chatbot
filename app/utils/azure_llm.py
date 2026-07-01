from langchain_openai import AzureChatOpenAI

from app.utils.config import (
    AZURE_API_KEY,
    AZURE_API_VERSION,
    AZURE_ENDPOINT,
    AZURE_DEPLOYMENT_NAME,
)

llm = AzureChatOpenAI(
    api_key=AZURE_API_KEY,
    api_version=AZURE_API_VERSION,
    azure_endpoint=AZURE_ENDPOINT,
    deployment_name=AZURE_DEPLOYMENT_NAME
)