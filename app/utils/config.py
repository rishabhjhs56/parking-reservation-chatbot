import os
from dotenv import load_dotenv

# Load variables from .env (project root)
load_dotenv()

AZURE_API_KEY = os.getenv("AZURE_API_KEY")
AZURE_API_VERSION = os.getenv("AZURE_API_VERSION")
AZURE_ENDPOINT = os.getenv("AZURE_ENDPOINT")
AZURE_DEPLOYMENT_NAME = os.getenv("AZURE_DEPLOYMENT_NAME")
AZURE_EMBEDDING_DEPLOYMENT = os.getenv("AZURE_EMBEDDING_DEPLOYMENT")
MILVUS_URI = os.getenv("MILVUS_URI")
MILVUS_COLLECTION_NAME = os.getenv("MILVUS_COLLECTION_NAME")