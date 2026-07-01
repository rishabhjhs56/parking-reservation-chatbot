from pymilvus import connections
from langchain_milvus import Milvus

from app.utils.azure_embeddings import embeddings
from app.utils.config import (
    MILVUS_COLLECTION_NAME,
    MILVUS_URI,
)

connections.connect(
    alias="default",
    uri=MILVUS_URI,
)

print("Has connection established.")

vector_store = Milvus(
    embedding_function=embeddings,
    collection_name=MILVUS_COLLECTION_NAME,
    connection_args={
        "alias": "default",
        "uri": MILVUS_URI,
    },
    auto_id=True,
)