from app.rag.milvus_client import MilvusVectorStore
from app.utils.azure_embeddings import embeddings


class ParkingRetriever:
    """
    Retrieves relevant parking information from the vector database.
    """

    def __init__(self):
        self.store = MilvusVectorStore()

    def retrieve(self, query: str, top_k: int = 5):

        query_vector = embeddings.embed_query(query)

        results = self.store.search(
            vector=query_vector,
            limit=top_k,
        )

        documents = []

        for item in results[0]:
            documents.append(item["entity"]["text"])

        return documents