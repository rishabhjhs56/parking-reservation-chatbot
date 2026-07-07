from app.rag.milvus_client import MilvusVectorStore
from app.utils.azure_embeddings import get_embeddings


class ParkingRetriever:
    """
    Retrieves relevant parking information from the vector database.
    """

    def __init__(self, store=None, embedding_model=None):
        self.store = store or MilvusVectorStore()
        self.embedding_model = embedding_model or get_embeddings()

    def retrieve(self, query: str, top_k: int = 5):

        #print("1. retrieve started")

        #query_vector = embeddings.embed_query(query)
        query_vector = self.embedding_model.embed_query(query)

        #print("2. embedding done")

        results = self.store.search(
            vector=query_vector,
            limit=top_k,
        )

        #print("3. milvus search done")

        documents = []

        for item in results[0]:
            documents.append(item["entity"]["text"])

        #print("4. retrieve finished")

        return documents