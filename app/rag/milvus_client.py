from pymilvus import MilvusClient

from app.utils.config import (
    MILVUS_URI,
    MILVUS_COLLECTION_NAME,
)


class MilvusVectorStore:

    def __init__(self):
        self.client = MilvusClient(uri=MILVUS_URI)

    def create_collection(self, dimension: int):

        collections = self.client.list_collections()

        if MILVUS_COLLECTION_NAME in collections:
            print("Collection already exists.")
            return

        self.client.create_collection(
            collection_name=MILVUS_COLLECTION_NAME,
            dimension=dimension,
        )

        print("Collection Created.")

    def drop_collection(self):

        collections = self.client.list_collections()

        if MILVUS_COLLECTION_NAME in collections:
            self.client.drop_collection(MILVUS_COLLECTION_NAME)
            print("Collection Deleted.")

    def insert(self, data):

        self.client.insert(
            collection_name=MILVUS_COLLECTION_NAME,
            data=data,
        )

    def search(self, vector, limit=3):

        return self.client.search(
            collection_name=MILVUS_COLLECTION_NAME,
            data=[vector],
            limit=limit,
            output_fields=["text"],
        )