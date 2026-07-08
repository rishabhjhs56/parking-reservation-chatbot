from app.rag.document_loader import load_documents
from app.rag.text_splitter import split_documents
from app.rag.milvus_client import MilvusVectorStore
from app.utils.azure_embeddings import get_embeddings


def index_documents():

    embedding_model = get_embeddings()

    print("Loading documents...")
    documents = load_documents()

    print("Splitting documents...")
    chunks = split_documents(documents)

    print(f"Total Chunks: {len(chunks)}")

    data = []

    for i, chunk in enumerate(chunks):

        vector = embedding_model.embed_query(chunk.page_content)

        data.append(
            {
                "id": i,
                "text": chunk.page_content,
                "vector": vector,
            }
        )

    store = MilvusVectorStore()

    print("Creating Collection...")
    store.drop_collection()
    store.create_collection(len(data[0]["vector"]))

    print("Inserting Data...")
    store.insert(data)

    print("✅ Indexing Completed")


if __name__ == "__main__":
    index_documents()